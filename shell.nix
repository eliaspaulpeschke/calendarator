{ pkgs, lib, stdenv, ... }:

let
  pythonPackages = pkgs.python3Packages;
in
pkgs.mkShell {
  packages = with pkgs; [
    rmapi
    wkhtmltopdf
  ];
  buildInputs = [
    pythonPackages.python
    pythonPackages.venvShellHook
    pythonPackages.wheel
    pythonPackages.setuptools
    pythonPackages.rmscene
    pythonPackages.rmcl
    pythonPackages.icalendar
    pythonPackages.pdfkit
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
}
