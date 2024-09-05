{ pkgs ? import <nixpkgs> {} }:

let
  madara = pkgs.rustPlatform.buildRustPackage rec {
    pname = "madara";
    version = "latest";

    src = pkgs.fetchFromGitHub {
      owner = "madara-alliance";
      repo = "madara";
      rev = "main";
      sha256 = "sha256-XeuPPWARW+qrfFatyb9UmthMI+20bqSkMeifvpmNI1E=";
    };

    cargoLock = {
      lockFile = ./Cargo.lock;
      outputHashes = {
          "blockifier-0.8.0-rc.0" = "sha256-Is+Y6miPfUAZEmE/g6Z7pC5MS64imXd8nfo8xu7KxyY=";
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

    buildType = "release";
  };

  madaraEnv = pkgs.buildEnv {
    name = "madara-env";
    paths = [ madara ];
  };

in pkgs.dockerTools.buildImage {
  name = "madara";
  tag = "latest";

  copyToRoot = madaraEnv;

  config = {
    Cmd = []; # Leave this for configuration
  };
}
