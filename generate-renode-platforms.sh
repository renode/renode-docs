#!/bin/bash

mkdir -p build/html/introduction

cd build
if [ ! -d renode ]; then
    if [ -n "$GET_CUSTOM_RENODE_REVISION" ]; then
        # Allow running external commands to fetch a custom revision of Renode for use in CI during development
        eval "$GET_CUSTOM_RENODE_REVISION"
    else
        # Otherwise, just get the latest source from GitHub
        git clone --depth=1 --recursive --shallow-submodules https://github.com/renode/renode
    fi
fi
cd ..

python3 build/renode/tools/peripherals_scanner.py --dir build/renode -H > source/introduction/renode_supported_peripherals.html
