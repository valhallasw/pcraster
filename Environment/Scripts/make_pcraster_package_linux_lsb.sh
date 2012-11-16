#!/usr/bin/env bash
set -e

export LSBCC_SHAREDLIBS=gdal
export MAKEFLAGS="-j4"

build_type="Release"
base_name="pcraster-lsb-`date +%Y%m%d`"
build_root=`pwd`
install_prefix=`pwd`/$base_name

make_pcraster_package.sh "$build_root" "$install_prefix" $build_type
tar zcf $base_name.tar.gz $base_name
ls -lh $base_name.tar.gz
