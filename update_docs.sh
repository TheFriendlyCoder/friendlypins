#!/usr/bin/env bash
sphinx-apidoc -f -e -o $PWD/docs/ src/friendlypins
pushd docs
make html
popd
open docs/_build/html/index.html