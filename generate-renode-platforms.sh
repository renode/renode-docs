#!/bin/bash

mkdir -p build/html/introduction

cd build
if [ ! -d renode ]; then
    git clone --depth=1 --shallow-submodules https://github.com/renode/renode
fi
(cd renode && git submodule update --init --recursive)
cd ..

python3 tools/peripherals_scanner.py --dir build/renode -H > source/introduction/renode_supported_peripherals.html
