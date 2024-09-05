#    __  __           _                   _____
#   |  \/  |         | |                 |_   _|
#   | \  / | __ _  __| | __ _ _ __ __ _    | |  _ __ ___   __ _  __ _  ___
#   | |\/| |/ _` |/ _` |/ _` | '__/ _` |   | | | '_ ` _ \ / _` |/ _` |/ _ \
#   | |  | | (_| | (_| | (_| | | | (_| |  _| |_| | | | | | (_| | (_| |  __/
#   |_|  |_|\__,_|\__,_|\__,_|_|  \__,_| |_____|_| |_| |_|\__,_|\__, |\___|
#                      ____        _ _     _                     __/ |
#                     |  _ \      (_) |   | |                   |___/
#                     | |_) |_   _ _| | __| | ___ _ __
#                     |  _ <| | | | | |/ _` |/ _ \ '__|
#                     | |_) | |_| | | | (_| |  __/ |
#                     |____/ \__,_|_|_|\__,_|\___|_|
#
# ---
# Builder which generates the Madara Node docker image for use in benchmarking. 
# Run with `nix-build`. This will generate an installation script as
# `./result/bin/copyto` which can then be executed to bring the generate docker 
# image `.tar.gz` into the current directory. This can then be loaded into
# docker using `docker load -i image.tar.gz`.
# ---

with import <nixpkgs>
{
  overlays = [
    (import (fetchTarball "https://github.com/oxalica/rust-overlay/archive/master.tar.gz"))
  ];
};
let
  rustPlatform = makeRustPlatform {
    cargo = rust-bin.stable."1.78.0".minimal;
    rustc = rust-bin.stable."1.78.0".minimal;
  };

  # The version of Madara being used
  # Updating this might also cause other nix hashes to need to be re-specified.
  madaraSrc = fetchFromGitHub {
    owner = "madara-alliance";
    repo = "madara";
    rev = "25f03eeb50dd3d92110d269547e499d9810e6bff";
    sha256 = "sha256-zbQaw9d8X4/sYgdXiVq981eDGWO3muscqD3Q6F44xi0=";
  };

  # Building madara with nix
  # https://ryantm.github.io/nixpkgs/languages-frameworks/rust/
  madara = rustPlatform.buildRustPackage rec {
    pname = "madara";
    version = "latest";

    src = madaraSrc;

    cargoLock = {
      lockFile = madaraSrc + "/Cargo.lock";

      # Crates specified as git dependencies need to have a unique hash 
      # associated to them to guarantee reproduceability
      #
      # For new dependencies, set this to `lib.fakeSha256` and copy the correct 
      # hash once the build fails
      outputHashes = {
          "bonsai-trie-0.1.0" = "sha256-7yyCI7y/2g7QfyyHHBWKu+c/kHR+ktqTyLazPeq6xP0=";
          "cairo-lang-casm-1.0.0-alpha.6" = "sha256-U4kTAAktXK7bFEkQAISQK3954hDkyxdsJU9c5hXmzpU=";
          "cairo-lang-casm-1.0.0-rc0" = "sha256-T+1o1H/NfJ19bwg3Lrqf11ocnpRyZw9R+y9uc3YDcgE=";
          "starknet-core-0.11.0" = "sha256-bzTFGZ9JnFf2n+Hk0/7pcWSTH/Vm8RITpKwLbV9p+4A=";
          "starknet-types-core-0.1.5" = "sha256-m20/wEcJMPMVDneVnWqlTI0ich/tn4UFUwIEO+0MUw0=";
        };
    };

    nativeBuildInputs = with pkgs; [
      pkg-config
      protobuf
      openssl
      clang
    ];

    buildInputs = with pkgs; [
      openssl
    ];

    buildType = "production";

    # Tests are disabled as we assume we are already using a working version
    doCheck = false;

    # clang does not correctly update its path in nix and so we need to patch it
    # manually
    preBuild = ''
      export LIBCLANG_PATH=${llvmPackages.libclang.lib}/lib
    '';
  };

  # Generates docker image using nix. This is equivalent to using `FROM scratch`.
  # https://ryantm.github.io/nixpkgs/builders/images/dockertools/
  image = dockerTools.buildImage {
    name = "madara";
    tag = "latest";

    created = "now";

    copyToRoot = buildEnv {
      name = "madara";
      paths = [ madara ];
    };

    config = {
      Cmd = [ "ls" "/" ]; # Leave this for configuration
    };
  };

# Calling `nix-build` on this file will create an artifact in `/nix/store/`.
# Crucially, nix uses the default unix time as date of last modification. This
# poses an issue since it means Make will always flag this output as
# out-of-date.
#
# To avoid this, we create a script which copies the generated docker image to 
# a given directory, updating its date to the current time. We cannot do this 
# otherwise as only root has ownership of artifacts generated in `/nix/store/`.
#
# This way, we are able to guarantee that docker images will not be rebuilt by 
# Make on each run, along with any other command associated to their generation 
# such as `docker load -i`.
in writeScriptBin "copyto" ''
  #!${pkgs.stdenv.shell}
  cp ${image} $1
  touch -m $1
''
