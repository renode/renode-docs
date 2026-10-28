#!/usr/bin/env bash

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

SPHINX_SOURCES="$(realpath source)"
BUILD_DIR="$(realpath build)"

python3 build/renode/tools/peripherals_scanner.py --dir build/renode -H > "${SPHINX_SOURCES}/introduction/renode_supported_peripherals.html"

build_api() (
    local doxygen_dir=$1
    local moxygen_output="${BUILD_DIR}/api-description/${2}"
    local anchor_prefix=$3

    echo "Building API docs: ${moxygen_output}"
    cd "${doxygen_dir}"

    doxygen && npx moxygen \
        --nogenerated-by --use-typedef-definitions --prepend-anchor-with-parent \
        --flavor myst \
        --output "${moxygen_output}" \
        --anchors "${anchor_prefix}" \
        --templates "${SPHINX_SOURCES}/../templates/moxygen" \
        output/xml
)

# Build External Control API
build_api build/renode/tools/external_control_client external-control-api.md external-control-
