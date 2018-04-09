#!/usr/bin/env bash
sphinx-apidoc -f -e -o $PWD/docs/ src/friendlypins
mkdir docs/_static
pushd docs
make html
popd
open docs/_build/html/index.html