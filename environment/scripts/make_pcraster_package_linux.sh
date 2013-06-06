#!/usr/bin/env bash
set -e

if [[ $CC == *lsb* ]]; then
    export LSBCC_SHAREDLIBS=gdal
fi

export LD_LIBRARY_PATH="$PYTHON_ROOT/lib"

source make_pcraster_package_common.sh
