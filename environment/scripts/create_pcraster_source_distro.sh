#!/usr/bin/env bash
set -e

sourceforge_username=$1
pcrserver_username=$2
target_directory="pcraster-`date +%Y%m%d`"
zip_name=$target_directory.tar.gz

rm -f $zip_name

# Create target directory. It must not already exist.
mkdir $target_directory

# Clone sources.
clone_pcraster_sources.sh $target_directory $sourceforge_username $pcrserver_username

# Copy license and build info to root of sources.
cp $target_directory/devenv/documentation/licenses/pcraster.txt $target_directory/COPYING.TXT
cp $target_directory/pcraster/documentation/pcraster/build.rst $target_directory/INSTALL.TXT
cp $target_directory/pcraster/documentation/pcraster/changes.rst $target_directory/CHANGES.TXT

# Zip sources.
tar zcf $zip_name $target_directory
