setlocal
sphinx-apidoc -f -e -o .\docs\ src\friendlypins
mkdir docs\_static
pushd docs
call make html
popd
start docs\_build\html\index.html