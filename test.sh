#!/usr/bin/env bash

# install wcosa
python setup.py -q install

# Test Case 1
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create widgets
wqt build
wqt clean
wqt update
wqt build
cd ..

# Test Case 2
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create quick
wqt build
wqt clean
wqt update
wqt build
cd ..

# Test Case 3
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create console
wqt build
wqt clean
wqt update
wqt build
cd ..
