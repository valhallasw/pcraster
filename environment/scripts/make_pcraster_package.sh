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
data_assimilation_sources="$DATAASSIMILATION"
pcraster_sources="$PCRASTER"

external_prefix="$PCRTEAM_EXTERN"

source $DEVENV/scripts/make_package.sh

native_path $build_root native_build_root
native_path $install_prefix native_install_prefix
native_path $external_prefix native_external_prefix


function remove_projects() {
    remove_project devenv
    remove_project dal
    remove_project aguila
    remove_project pcrtree2
    remove_project pcraster
    remove_project data_assimilation
}


function build_projects() {
    build_project devenv ""
    build_project raster_format ""
    build_project xsd "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
    "
    build_project dal "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DRASTERFORMAT_ROOT=$native_build_root/raster_format_$build_type
    "
    build_project aguila "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DXSD_ROOT=$native_build_root/xsd_$build_type
        -DDAL_ROOT=$native_build_root/dal_$build_type
    "

    if [ $os != "Cygwin" ]; then
        configure_dll_path pcrtree2
        configure_python_path pcrtree2
    fi
    build_project pcrtree2 "
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
    build_project data_assimilation "
        -DDEVENV_ROOT=$native_build_root/devenv_$build_type
        -DPCRTREE2_ROOT=$native_build_root/pcrtree2_$build_type
    "
    if [ $os != "Cygwin" ]; then
        reset_python_path
    fi
    build_project pcraster ""
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


remove_projects
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
verify_pcraster_installation.py $native_install_prefix
