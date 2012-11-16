#!/usr/bin/env bash
set -e

export MAKEFLAGS="-j4"

build_type="Release"
base_name="pcraster-`date +\"%Y%m%d\"`"
base_name="pcraster-20121115"
build_root=`pwd`
install_prefix=`pwd`/$base_name

make_pcraster_package.sh "$build_root" "$install_prefix" $build_type
