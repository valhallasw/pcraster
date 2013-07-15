#!/usr/bin/env bash
set -e

if [ $# != 1 ]; then
    echo "Not enough arguments"
    echo "`basename $0` <target_directory>"
    echo ""
    echo "target_directory  Path to directory to create. The zip will be named"
    echo "                  after this directory. It must not already exist."
    exit 1
fi

# This directory will be created. It should not already exist.
# The package will be named after the target directory's basename.
target_directory=$1
target_directory_basename=`basename $target_directory`

# Create and cd to the new directory.
mkdir $target_directory
cd $target_directory

# workspace/demo.
mkdir -p workspace/demo/{data,doc}
cp $PCRTREE2/data/demo/*.{bat,map,mod,py,sh,tbl,tss} workspace/demo/data
cp $PCRTREE2/data/demo/*.{html,png} workspace/demo/doc

# workspace/modflow.
mkdir -p workspace/modflow
cp $PCRTREE2/sources/modflow/demo/* workspace/modflow

# Examples.
mkdir -p example/{vector,muskingum}
cp $PCRTREE2/data/samples/vector/* example/vector
cp -r $PCRTREE2/data/samples/muskingum/* example/muskingum


cd ..


os=`uname -o`

if [ $os == "Cygwin" ]; then
    package_filename=$target_directory_basename.zip
    zip -q -r $package_filename $target_directory_basename
else
    package_filename=$target_directory_basename.tar.gz
    tar zcf $package_filename $target_directory_basename
fi

rm -fr $target_directory_basename
pwd
ls -hl $package_filename
