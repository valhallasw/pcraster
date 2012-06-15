#!/usr/bin/env pythonwrapper
# -*- coding: utf-8 -*-
"""
Verify that a PCRaster installation is likely to be correct.
"""
import argparse
import os
import sys
import traceback
import devenv


def verify_installation(
        prefix):
    devenv.verify_package(prefix=prefix,
        required_root_directory_names=["bin", "doc", "lib", "Python", "share"],
        # required_file_names = ["INSTALL_LINUX.TXT", "LICENSE.TXT"]
        required_root_file_names=[],
        required_directory_path_names=[
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
            "share/gdal"
        ],
        required_file_path_names=
            # [ "doc/{}/index.html".format(name) for name in ["aguila", "demo", "manual", "modflow"] +
            # "doc/python/pcraster/index.html",
            # "doc/python/pcraster/framework/index.html",
            ["bin/{}".format(name) for name in [
                "aguila", "asc2map", "col2map", "legend", "map2asc", "map2col",
                "mapattr", "oldcalc", "pcrcalc", "pcrseal", "resample", "table"]
            ] + \
            ["Python/PCRaster/__init__.py",
                "Python/PCRaster/Framework/__init__.py" ],
        executable_path_names=[
            os.path.join(prefix, "bin", "aguila"),
            os.path.join(prefix, "bin", "pcrcalc"),
            os.path.join(prefix, "bin", "oldcalc")],
        python_package_directory_name="Python",
        python_package_names=["PCRaster", "PCRaster.Framework"])
    result = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Verify that an installation is likely to be correct")
    parser.add_argument("prefix", help="Path to installation")
    arguments = parser.parse_args()
    prefix = os.path.abspath(arguments.prefix)

    try:
        verify_installation(prefix)
    except:
        traceback.print_exc(file=sys.stderr)
        result = 1
    sys.exit(result)
