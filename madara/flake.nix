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
      in
      {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          # Rust
          pkg-config
          protobuf
          openssl
          clang
        ];

        RUST_BACKTRACE = 1;
      };
    }
  );
}
