#!/usr/bin/env bash
set -e

export LSBCC_SHAREDLIBS=gdal

make_pcraster_package_linux.sh
