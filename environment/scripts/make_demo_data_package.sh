#!/usr/bin/env bash
set -e

# This directory will be created. It should not already exist.
# The package will be named after the target directory's basename.
target_directory=$1
target_directory_basename=`basename $target_directory`

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


package_filename=$target_directory_basename.tar.gz

cd ..
tar zcf $package_filename $target_directory_basename
rm -fr $target_directory_basename
pwd
ls -hl $package_filename
