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

    executable_path_names=[
        "aguila",
        "asc2map",
        "col2map",
        "legend",
        "map2asc",
        "map2col",
        "mapattr",
        "oldcalc",
        "pcrcalc",
        # TODO "pcrmf2k",
        "resample",
        "table"
    ]

    if sys.platform == "win32":
        executable_path_names = ["{}.exe".format(path_name) for path_name in
            executable_path_names]

    devenv.verify_package(prefix=prefix,
        required_root_directory_names=["bin", "doc", "lib", "python", "share"],
        # required_file_path_names = ["INSTALL_LINUX.TXT", "LICENSE.TXT"]
        # required_file_path_names = ["LICENSE.TXT"],


        # LICENSE.TXT
        # 
        # doc/Aguila/COPYING
        # doc/Aguila/Gpl-2.txt
        # 
        # doc/version.txt

        required_root_file_names=[],
        required_directory_path_names=[
            # "doc/aguila"
            # "doc/demo"
            # "doc/manual"
            # "doc/modflow"
            # "doc/python/pcraster"
            # "doc/python/pcraster/framework"
            # Developer  manual  PCRasterModflow  PCRasterPython  PCRasterPythonFramework
            "bin",
            "doc",
            "doc/developer",
            "doc/developer/c",
            "doc/developer/c/include",
            "doc/developer/linkout",
            "doc/developer/linkout/csharp",
            "doc/developer/xsd",
            "lib",
            "python",
            "python/PCRaster",
            "python/PCRaster/Collection",
            "python/PCRaster/Framework",
            "python/PCRaster/Moc",
            "python/PCRaster/Mldd",
            "python/PCRaster/NumPy",
            "share",
            "share/gdal"
        ],
        required_file_path_names=
            [os.path.join("doc", name, "index.html") for name in [
                "aguila",
                "manual",
                "modflow"
            ] if sys.platform != "win32"] + \
            [
                "doc/developer/c/include/pcrcalc.h",
                "doc/developer/c/include/pcrdll.h",
                # "doc/developer/linkout/deployment.txt",
                "doc/developer/linkout/LinkOutAPIUserManual.pdf",
                "doc/developer/linkout/html/index.html",
                "doc/developer/xsd/PCRaster.xsd",
                "doc/developer/xsd/commonTypes.xsd",
                "doc/python/manual/index.html",
                # "doc/python/framework/index.html"
                # "doc/python/arrayed_variables/index.html"
            ] + \
            [
                os.path.join("bin", name) for name in executable_path_names
            ] + \
            [
                os.path.join("python", "pcraster.py")
            ] + \
            [os.path.join("python", "PCRaster", name) for name in [
                "__init__.py",
                "Framework/__init__.py"
            ]] + \
            [
                # "LICENSE.TXT",
                # TODO "lib/PCRasterModflow.xml",
                "share/gdal/LICENSE.TXT"
            ],
        executable_path_names=[
            os.path.join(prefix, "bin", name) for name in
                executable_path_names
            ],
        python_package_directory_name="python",
        python_package_names=[
            "PCRaster",
            "PCRaster.Collection",
            "PCRaster.Framework",
            "PCRaster.Mldd",
            "PCRaster.Moc",
            "PCRaster.NumPy"
        ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Verify that an installation is likely to be correct")
    parser.add_argument("prefix", help="Path to installation")
    arguments = parser.parse_args()
    prefix = os.path.abspath(arguments.prefix)

    try:
        verify_installation(prefix)
        result = 0
    except:
        traceback.print_exc(file=sys.stderr)
        result = 1
    sys.exit(result)