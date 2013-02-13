#!/usr/bin/env bash
set -e

# Clone the PCRaster sources.
target_directory=$1
sourceforge_username=$2
pcrserver_username=$3

project_names="PcrTree2 DataAssimilation PCRaster"
for project_name in $project_names; do
    project_name_lower=`awk "BEGIN { print tolower(\"$project_name\") }"`
    git clone ssh://$pcrserver_username@pcrserver.geo.uu.nl:222/home/git/$project_name $project_name_lower
done

project_names="devenv rasterformat xsd dal aguila"
for project_name in $project_names; do
    git clone ssh://$sourceforge_username@git.code.sf.net/p/pcraster/$project_name
done
