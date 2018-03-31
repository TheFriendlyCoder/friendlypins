#!/usr/bin/env bash
echo $TRAVIS_PYTHON_VERSION
[ $TRAVIS_PYTHON_VERSION == "pypy" ] && export TOXENV=pypy
[ $TRAVIS_PYTHON_VERSION == "pypy3" ] && export TOXENV=pypy3
[ -z $TOKENENV ] && export TOXENV=py`echo $TRAVIS_PYTHON_VERSION | tr "." "\n" | head -n 1`