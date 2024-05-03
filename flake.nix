{
  description = "Flake utils demo";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        mixxx-m3u-loader = pkgs.callPackage ./. { };
      in {
        formatter = pkgs.nixfmt;

        packages = {
          mixxx-m3u-loader = mixxx-m3u-loader;
          default = mixxx-m3u-loader;
        };
      });
}
