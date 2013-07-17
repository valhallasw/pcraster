#!/usr/bin/env bash
set -e
set -x

if [ $# != 1 ] || [$# != 2]; then
    echo "Wrong number of arguments"
    echo "`basename $0` <target_directory> [username]"
    echo ""
    echo "target_directory  Path to root of directory to place projects in."
    echo "username          Sourceforge user name."
    echo ""
    echo "If username is not provided, then the clone is readonly."
    exit 1
fi

target_directory=$1

clone_readonly=1
if [ $# == 2 ]; then
    username=$2
    clone_readonly=0
fi

cd $target_directory

project_names="devenv rasterformat xsd dal aguila pcrtree2 data_assimilation pcraster"
for project_name in $project_names; do
    if (( clone_readonly == 1 )); then
        git clone git://git.code.sf.net/p/pcraster/$project_name
    else
        git clone ssh://$username@git.code.sf.net/p/pcraster/$project_name
    fi
done
