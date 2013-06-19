#!/usr/bin/env bash
set -e

# Where to build targets.
build_root=$1

# Where to install targets.
install_prefix=$2

# What build type to build.
build_type=$3

cmake="cmake"

devenv_sources="$DEVENV"
raster_format_sources="$RASTERFORMAT"
xsd_sources="$XSD"
dal_sources="$DAL"
aguila_sources="$AGUILA"
pcrtree2_sources="$PCRTREE2"
data_assimilation_sources="$DATA_ASSIMILATION"
pcraster_sources="$PCRASTER"

external_prefix="$PCRTEAM_EXTERN"

# Make sure we don't use lingering stuff by accident.
# TODO
# unset OBJECTS

source $DEVENV/scripts/make_package.sh

native_path $build_root native_build_root
native_path $install_prefix native_install_prefix
native_path $external_prefix native_external_prefix


function build_or_rebuild_project() {
    # Call build_project only when debugging.
    rebuild_project "$@"  # *Always* commit with this line uncommented!
    # build_project "$@"  # *Never* commit with this line uncommented!
}


function build_projects() {
    build_or_rebuild_project devenv ""
    build_or_rebuild_project raster_format ""
    build_or_rebuild_project xsd "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
    "
    build_or_rebuild_project dal "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DRASTERFORMAT_ROOT=$native_build_root/raster_format_$build_type
    "
    build_or_rebuild_project aguila "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DXSD_ROOT=$native_build_root/xsd_$build_type
        -DDAL_ROOT=$native_build_root/dal_$build_type
    "

    if [ $os != "Cygwin" ]; then
        configure_dll_path pcrtree2
        configure_python_path pcrtree2
    fi
    build_or_rebuild_project pcrtree2 "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DXSD_ROOT=$native_build_root/xsd_$build_type
        -DDAL_ROOT=$native_build_root/dal_$build_type
        -DRASTERFORMAT_ROOT=$native_build_root/raster_format_$build_type
    "
    if [ $os != "Cygwin" ]; then
        reset_dll_path
        reset_python_path
    fi

    if [ $os != "Cygwin" ]; then
        configure_python_path pcrtree2
    fi
    build_or_rebuild_project data_assimilation "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DPCRTREE2_ROOT=$native_build_root/pcrtree2_$build_type
    "
    if [ $os != "Cygwin" ]; then
        reset_python_path
    fi
    build_or_rebuild_project pcraster ""
}


function install_projects() {
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
    local install_base_name=`basename $install_prefix`
    local install_dir_name=`dirname $install_prefix`

    cd $install_dir_name

    if [ $os == "Cygwin" ]; then
        install_zip_name=$install_base_name.zip
        zip -q -r $install_zip_name $install_base_name
    else
        install_zip_name=$install_base_name.tar.gz
        tar zcf $install_zip_name $install_base_name
    fi

    rm -fr $install_base_name

    native_path $install_dir_name/$install_zip_name $2
}


build_projects
install_projects
if [ $os == "Cygwin" ]; then
    configure_dll_path dal
    configure_dll_path pcrtree2
fi
fixup.py $native_install_prefix $native_external_prefix
if [ $os == "Cygwin" ] ;then
    reset_dll_path
fi
verify_pcraster_installation.py $install_prefix
make_package $install_prefix install_zip_path_name
ls -lh $install_zip_path_name
