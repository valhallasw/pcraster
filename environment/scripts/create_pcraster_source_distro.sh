#!/usr/bin/env bash
set -e

target_root_directory=$(readlink -f $1)
sourceforge_username=$2
pcrserver_username=$3
target_basename="pcraster-`date +%Y%m%d`"
zip_name=$target_basename.tar.gz

# All commands are run from the target_root_directory passed in.
cd $target_root_directory

# Create target directory. It must not already exist. Remove lingering zip.
mkdir $target_basename
rm -f $zip_name

# Clone sources and get rid of the repository stuff. Careful with the rm!
clone_pcraster_sources.sh $target_basename $sourceforge_username $pcrserver_username
find $target_basename -type d -name \.git -print | xargs rm -fr
find $target_basename -type f -name \.gitignore -print | xargs rm -f

# Copy license and build info to root of sources.
cp $target_basename/devenv/documentation/licenses/pcraster.txt $target_basename/COPYING.TXT
cp $target_basename/pcraster/documentation/pcraster/build.rst $target_basename/INSTALL.TXT
cp $target_basename/pcraster/documentation/pcraster/changes.rst $target_basename/CHANGES.TXT

# Zip sources and clean up.
tar zcf $zip_name $target_basename
rm -fr $target_basename

ls -l $zip_name
