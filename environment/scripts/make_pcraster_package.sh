#!/usr/bin/env bash
set -e

if [ $# != 2 ]; then
    echo "Not enough arguments"
    echo "`basename $0` <pcrteam_extern> <project_root>"
    echo ""
    echo "pcrteam_extern  Path to root of external stuff."
    echo "project_root    Path to root of devenv projects."
    exit 1
fi

# Where to find external stuff.
pcrteam_extern=$1

# Where to find the projects.
project_root=$2

# Where to build targets.
build_root=`pwd`


function path_name_to_project() {
    local project_root=$1
    local project_name=$2
    eval $3="$project_root/`\ls $project_root | \grep -i \"^$project_name$\"`"
}

path_name_to_project $project_root devenv devenv_sources
path_name_to_project $project_root rasterformat rasterformat_sources
path_name_to_project $project_root xsd xsd_sources
path_name_to_project $project_root dal dal_sources
path_name_to_project $project_root aguila aguila_sources
path_name_to_project $project_root pcrtree2 pcrtree2_sources
path_name_to_project $project_root data_assimilation data_assimilation_sources
path_name_to_project $project_root pcraster pcraster_sources


source $devenv_sources/scripts/make_package.sh

native_path $devenv_sources native_devenv_sources

export CMAKE_MODULE_PATH="$native_devenv_sources/templates/cmake;$CMAKE_MODULE_PATH"

# determine_platform compiler_ architecture_ address_model_
# platform_as_string platform
# external_platform_prefix=$external_prefix/$platform
# unset platform

build_type="Release"
external_prefix="$pcrteam_extern"

cmake="cmake"
cmake_generator generator
native_path $build_root native_build_root
native_path $external_prefix native_external_prefix


function build_or_rebuild_project() {
    local project_name=$1
    local install_prefix=$2
    local generator=$3
    shift 3
    local cmake_options=$*

    # *ALWAYS* commit with this line uncommented!!!
    rebuild_project $project_name "$install_prefix" "$generator" $cmake_options

    # *NEVER* commit with this line uncommented!!!
    # build_project $project_name "$install_prefix" "$generator" $cmake_options
}


function build_projects() {
    local install_prefix=$1
    local generator=$2

    build_or_rebuild_project devenv "$install_prefix" "$generator" ""
    build_or_rebuild_project rasterformat "$install_prefix" "$generator" ""
    build_or_rebuild_project xsd "$install_prefix" "$generator" \
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
    build_or_rebuild_project dal "$install_prefix" "$generator" \
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type \
        -DRASTERFORMAT_ROOT=$native_build_root/rasterformat_$build_type
    build_or_rebuild_project aguila "$install_prefix" "$generator" \
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type \
        -DXSD_ROOT=$native_build_root/xsd_$build_type \
        -DDAL_ROOT=$native_build_root/dal_$build_type

    if [ $os != "Cygwin" ]; then
        configure_dll_path pcrtree2
        configure_python_path pcrtree2
    fi
    build_or_rebuild_project pcrtree2 "$install_prefix" "$generator" \
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type \
        -DXSD_ROOT=$native_build_root/xsd_$build_type \
        -DDAL_ROOT=$native_build_root/dal_$build_type \
        -DRASTERFORMAT_ROOT=$native_build_root/rasterformat_$build_type
    if [ $os != "Cygwin" ]; then
        reset_dll_path
        reset_python_path
    fi

    if [ $os != "Cygwin" ]; then
        configure_python_path pcrtree2
    fi
    build_or_rebuild_project data_assimilation "$install_prefix" "$generator" \
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type \
        -DPCRTREE2_ROOT=$native_build_root/pcrtree2_$build_type
    if [ $os != "Cygwin" ]; then
        reset_python_path
    fi

    build_or_rebuild_project pcraster "$install_prefix" "$generator" ""
}


function install_projects() {
    local install_prefix=$1

    rm -fr $install_prefix

    install_project devenv
    install_project dal
    install_project aguila
    configure_dll_path pcrtree2
    configure_python_path pcrtree2
    install_project pcrtree2
    reset_dll_path
    reset_python_path
    install_project pcraster

    configure_python_path pcrtree2
    install_project data_assimilation
    reset_python_path
}


function make_package() {
    local install_prefix=$1
    local install_basename=`basename $install_prefix`
    local install_dir_name=`dirname $install_prefix`

    cd $install_dir_name

    if [ $os == "Cygwin" ]; then
        install_zip_name=$install_basename.zip
        zip -q -r $install_zip_name $install_basename
    else
        install_zip_name=$install_basename.tar.gz
        tar zcf $install_zip_name $install_basename
    fi

    rm -fr $install_basename

    native_path $install_dir_name/$install_zip_name $2

    cd -
}


if [ $OSTYPE == "linux_gnu" ]; then
    if [[ $CC == *lsb* ]]; then
        export LSBCC_SHAREDLIBS=gdal
    fi

    # export LD_LIBRARY_PATH="$external_platform_prefix/python-*/lib"
fi


cd $build_root

# Determine name of install directory, package file, etc. Grep this information
# from the generated CMakeCache.txt. Otherwise we have to duplicate the
# string formatting logic here.
# Generate PCRaster's CMakeCache.txt by configuring the project.
remove_project "pcraster"
configure_project pcraster "whatever" "$generator" ""
basename=`grep BASENAME pcraster_$build_type/CMakeCache.txt | python -c "import sys; lines = sys.stdin.readlines(); assert(len(lines) == 1); sys.stdout.write(lines[0].strip().split(\"=\")[1])"`
install_prefix=`pwd`/$basename
native_path $install_prefix native_install_prefix

build_projects "$install_prefix" "$generator"

install_projects $install_prefix
if [ $os == "Cygwin" ]; then
    configure_dll_path dal
    configure_dll_path pcrtree2
fi
python $native_devenv_sources/scripts/fixup.py $native_install_prefix $native_external_prefix
if [ $os == "Cygwin" ] ;then
    reset_dll_path
fi

# TODO Verifying the package must be done from a shell with user settings,
#      not from the current shell! Current shell has dev PATH, PYTHONPATH, ...
#      Update verify script?
export AGUILA=$aguila_sources
export PCRTEAM_EXTERN=$pcrteam_extern
export PYTHONPATH="$native_devenv_sources/sources;$PYTHONPATH"
_cwd=$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)
native_path $_cwd _native_cwd
python $_native_cwd/verify_pcraster_installation.py $native_install_prefix

make_package $install_prefix install_zip_path_name
ls -lh $install_zip_path_name
