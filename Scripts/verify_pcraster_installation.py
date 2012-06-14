#!/usr/bin/env pythonwrapper
# -*- coding: utf-8 -*-
"""
Verify that a PCRaster installation is likely to be correct.
"""
import argparse
import os
import subprocess
import sys
import traceback
import devenv


def check_existance_of_files_and_directories(
        prefix):
    assert(os.path.isabs(prefix))

    if not os.path.isdir(prefix):
        raise ValueError(
            "Path to installation directory does not exist or is not "
            "a directory")

    root_directory_names, root_file_names = \
        devenv.file_names_in_root_of_directory(prefix)
    devenv.check_existance_of_root_directories(root_directory_names,
        required_directory_names=["bin", "doc", "lib", "plugins", "Python",
            "share"])
    # required_file_names = ["INSTALL_LINUX.TXT", "LICENSE.TXT"]
    devenv.check_existance_of_root_files(root_file_names,
        required_file_names=[])

    directory_names = [
        # "doc/aguila"
        # "doc/demo"
        # "doc/manual"
        # "doc/modflow"
        # "doc/python/pcraster"
        # "doc/python/pcraster/framework"
        # Developer  manual  PCRasterModflow  PCRasterPython  PCRasterPythonFramework
        "Python",
        "Python/PCRaster",
        "Python/PCRaster/Framework"
    ]
    devenv.check_existance_of_directories(prefix, directory_names)

    # [ "doc/{}/index.html".format(name) for name in ["aguila", "demo", "manual", "modflow"] +
    # "doc/python/pcraster/index.html",
    # "doc/python/pcraster/framework/index.html",

    file_names = \
        ["bin/{}".format(name) for name in [
            "aguila", "asc2map", "col2map", "legend", "map2asc", "map2col",
            "mapattr", "oldcalc", "pcrcalc", "pcrseal", "resample", "table"]
        ] + \
        ["Python/PCRaster/__init__.py", "Python/PCRaster/Framework/__init__.py" ]
    devenv.check_existance_of_files(prefix, file_names)


def verify_python_package(
        prefix):
    subprocess.check_call(["python", "-c", "import PCRaster"])
    subprocess.check_call(["python", "-c", "import PCRaster.Framework"])


def verify_installation(
        prefix):
    result = 0

    try:
        check_existance_of_files_and_directories(prefix)
        verify_python_package(prefix)
        devenv.check_shared_libraries(target_path_names=[
            os.path.join(prefix, "bin", "aguila"),
            os.path.join(prefix, "bin", "pcrcalc"),
            os.path.join(prefix, "bin", "oldcalc")])
        sys.stdout.write("installation seems fine!\n")
    except:
        traceback.print_exc(file=sys.stderr)
        result = 1

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Verify that an installation is likely to be correct")
    parser.add_argument("prefix", help="Path to installation")
    arguments = parser.parse_args()
    prefix = os.path.abspath(arguments.prefix)
    sys.exit(verify_installation(prefix))
