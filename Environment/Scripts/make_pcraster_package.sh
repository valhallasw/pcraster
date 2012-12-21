#!/usr/bin/env bash
set -e
set -x

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

source $DEVENV/Scripts/make_package.sh


function build_projects() {
    build_project devenv ""
    build_project raster_format ""
    build_project xsd "
        -DDEVENV_ROOT=$build_root/devenv_$build_type
    "
    build_project dal "
        -DDEVENV_ROOT=$build_root/devenv_$build_type
        -DRASTERFORMAT_ROOT=$build_root/raster_format_$build_type
    "
    build_project aguila "
        -DDEVENV_ROOT=$build_root/devenv_$build_type
        -DXSD_ROOT=$build_root/xsd_$build_type
        -DDAL_ROOT=$build_root/dal_$build_type
    "
    configure_dll_path pcrtree2
    configure_python_path pcrtree2
    build_project pcrtree2 "
        -DDEVENV_ROOT=$build_root/devenv_$build_type
        -DXSD_ROOT=$build_root/xsd_$build_type
        -DDAL_ROOT=$build_root/dal_$build_type
        -DRASTERFORMAT_ROOT=$build_root/raster_format_$build_type
    "
    reset_dll_path
    reset_python_path
    configure_python_path pcrtree2
    build_project data_assimilation "
        -DDEVENV_ROOT=$build_root/devenv_$build_type
    "
    build_project pcraster ""
}


function install_projects() {
    rm -fr $install_prefix

    install_project dal
    install_project aguila
    configure_dll_path pcrtree2
    configure_python_path pcrtree2
    install_project pcrtree2
    reset_dll_path
    reset_python_path
    install_project data_assimilation
}


# build_projects
install_projects
fixup.py $install_prefix $external_prefix
verify_pcraster_installation.py $install_prefix
