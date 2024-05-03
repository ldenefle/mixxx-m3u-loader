{ python3, stdenv, lib, ... }:

stdenv.mkDerivation {
  pname = "mixx-m3u-loader";
  version = "0.0.1";

  propagatedBuildInputs = [ python3 ];

  dontUnpack = true;

  installPhase =
    "install -Dm755 ${./mixxx-m3u-loader} $out/bin/mixx-m3u-loader";

  meta = with lib; {
    description = "Small package that loads m3u files as mixxx playlist";
    maintainers = with maintainers; [ ldenefle ];
  };
}

