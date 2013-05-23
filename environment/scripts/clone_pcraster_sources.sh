#!/usr/bin/env bash
set -e

target_directory=$1
username=$2

cd $target_directory

project_names="devenv rasterformat xsd dal aguila pcrtree2 data_assimilation pcraster"
for project_name in $project_names; do
    git clone ssh://$username@git.code.sf.net/p/pcraster/$project_name
done
