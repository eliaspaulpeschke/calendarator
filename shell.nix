{ pkgs, lib, stdenv, ... }:

let
  pythonPackages = pkgs.python3Packages;
  nodePackages = pkgs.nodePackages;
in
pkgs.mkShell {
  packages = with pkgs; [
    rmapi
  ];
  buildInputs = [
    nodePackages.nodejs
    nodePackages.npm
    pythonPackages.python
    pythonPackages.venvShellHook
    pythonPackages.wheel
    pythonPackages.setuptools
    pythonPackages.rmscene
    pythonPackages.rmcl
    pythonPackages.icalendar
    pythonPackages.dominate
   ];
  venvDir = "./.venv";
  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
  '';
  postShellHook = ''
    unset SOURCE_DATE_EPOCH
    export LD_LIBRARY_PATH=${lib.makeLibraryPath [stdenv.cc.cc]}
  '';
  env = {
      PUPPETEER_SKIP_DOWNLOAD = true;
      PYPPETEER_SKIP_DOWNLOAD = true;
  };
}
