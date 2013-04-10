#!/usr/bin/env bash
set -e

if [[ $CC == *lsb* ]]; then
    export LSBCC_SHAREDLIBS=gdal
fi

export LD_LIBRARY_PATH="$PYTHON_ROOT/lib"

build_type="Release"
base_name="pcraster-${PCRTEAM_PLATFORM##*/}-`date +%Y%m%d`"
build_root=`pwd`
install_prefix=`pwd`/$base_name

make_pcraster_package.sh "$build_root" "$install_prefix" $build_type
tar zcf $base_name.tar.gz $base_name
rm -fr $base_name
ls -lh $base_name.tar.gz
