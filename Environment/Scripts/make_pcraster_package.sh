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

os=`uname -o`

if [ $os == "GNU/Linux" ]; then
    ld_library_path=$LD_LIBRARY_PATH
    python_path=$PYTHONPATH
fi


function configure_dll_path() {
    local project_name=$1
    if [ $os == "GNU/Linux" ]; then
        export LD_LIBRARY_PATH="$build_root/${project_name}_$build_type/bin:$LD_LIBRARY_PATH"
    fi
    # TODO Darwin
    # TODO Cygwin
}


function reset_dll_path() {
    if [ $os == "GNU/Linux" ]; then
        export LD_LIBRARY_PATH=$ld_library_path
    fi
    # TODO Darwin
    # TODO Cygwin
}


function configure_python_path() {
    local project_name=$1
    if [ $os == "GNU/Linux" ]; then
        export PYTHONPATH="$build_root/${project_name}_$build_type/bin:$PYTHONPATH"
    fi
    # TODO Darwin
    # TODO Cygwin
}


function reset_python_path() {
    if [ $os == "GNU/Linux" ]; then
        export PYTHONPATH=$python_path
    fi
    # TODO Darwin
    # TODO Cygwin
}


function build_project() {
    local project_name=$1
    local cmake_options=$2
    # local rpath="$3"
    local project_base=${project_name}_$build_type

    cd $build_root
    rm -fr $project_base; mkdir $project_base; cd $project_base
    eval project_sources=\$${project_name}_sources

    $cmake \
        -DCMAKE_BUILD_TYPE=$build_type \
        -DCMAKE_INSTALL_PREFIX="$install_prefix" \
        -DPCRTEAM_EXTERN="$PCRTEAM_EXTERN" \
        $cmake_options \
        $project_sources
    $cmake --build . --config $build_type
    # PATH="$rpath:$PATH" $cmake --build . --config $build_type --target run_tests
}


function install_project() {
    local project_name=$1
    local project_base=${project_name}_$build_type

    cd $build_root/$project_base
    $cmake --build . --target install --config $build_type
}


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


build_projects
install_projects
fixup.py $install_prefix $external_prefix
verify_pcraster_installation.py $install_prefix
