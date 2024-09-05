{
  description = "Madara build environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, rust-overlay, flake-utils }: 
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs {
          inherit system overlays;
        };

        rustVersion = (pkgs.rust-bin.stable.latest.default.override {
          extensions = [ "rust-src" ];
          targets = [ "wasm32-unknown-unknown" ];
        });

        madara = pkgs.rustPlatform.buildRustPackage {
          pname = "madara";
          version = "0.7.0";

          src = pkgs.fetchFromGitHub {
            owner = "madara-alliance";
            repo = "madara";
            rev = "0.7,0";
            hash = "sha256-+s5RBC3XSgb8omTbUNLywZnP6jSxZBKSS1BmXOjRF8M=";
          };

          cargoLock = {
            lockFile = ./Cargo.lock;
          };

          buildInputs = with pkgs; [
            pkg-config
            protobuf
            openssl
            clang
          ];
        };
      in
      { 
      packages.dockerImage = pkgs.dockerTools.buildImage {
        name = "madara";
        tag = "latest";

        copyToRoot = pkgs.buildEnv {
          name = "image-root";
          paths = [ madara ];
          pathsToLink = [ "/bin" ];
        };

        config = {
          Cmd = [ "bin/madara --help" ];
        };
      };

      # devShell = pkgs.mkShell {
      #   buildInputs = with pkgs; [
      #     # Rust
      #     pkg-config
      #     protobuf
      #     openssl
      #     clang
      #   ];
      #
      #   RUST_BACKTRACE = 1;
      # };
    }
  );
}
