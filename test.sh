#!/usr/bin/env bash

# install wcosa
python setup.py -q install

# Test Case 1
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create widgets
wqt clean
wqt update
cd ..

# Test Case 2
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create quick
wqt clean
wqt update
cd ..

# Test Case 3
rm -rf test-wqt
mkdir test-wqt
cd test-wqt
wqt create console
wqt clean
wqt update
cd ..
