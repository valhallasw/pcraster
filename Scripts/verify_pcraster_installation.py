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



def check_existance_of_root_directories(
        directory_names):
    required_directory_names = ["bin", "doc", "lib", "plugins", "Python",
        "share"]

    for directory_name in required_directory_names:
        if not directory_name in directory_names:
            raise RuntimeError(
                "Directory {0} missing from installation".format(
                    directory_name))

    if len(required_directory_names) < len(directory_names):
        raise RuntimeError(
            "Too many directories in root of installation: {0}".format(
                ", ".join(set(directory_names) -
                    set(required_directory_names))))



def check_existance_of_root_files(
        file_names):
    ### required_file_names = ["INSTALL_LINUX.TXT", "LICENSE.TXT"]
    required_file_names = []

    ### if sys.platform == "win32":
    ###     required_file_names += ["Uninstall.exe"]

    for file_name in required_file_names:
        if not file_name in file_names:
            raise RuntimeError(
                "File {0} missing from installation".format(file_name))

    if len(required_file_names) < len(file_names):
        raise RuntimeError(
            "Too many files in root of installation: {0}".format(
                ", ".join(set(file_names) -
                    set(required_file_names))))



def check_existance_of_directories(
        prefix,
        path_names):
    for path_name in path_names:
        if not os.path.isdir(os.path.join(prefix, path_name)):
            raise RuntimeError(
                "Directory {0} missing from installation".format(path_name))



def check_existance_of_files(
        prefix,
        path_names):
    for path_name in path_names:
        if not os.path.isfile(os.path.join(prefix, path_name)):
            raise RuntimeError(
                "File {0} missing from installation".format(path_name))



def check_existance_of_files_and_directories(
        prefix):
    assert(os.path.isabs(prefix))

    if not os.path.isdir(prefix):
        raise ValueError(
            "Path to PCRaster installation directory does not exist or is not "
            "a directory")

    root_directory_names = []
    root_file_names = []

    for triple in os.walk(prefix, topdown=True):
        path_name = triple[0]
        relative_path_name = os.path.relpath(path_name, prefix)

        if not os.path.dirname(relative_path_name):
          if relative_path_name == ".":
              root_file_names = triple[2]
          else:
              root_directory_names.append(relative_path_name)

    check_existance_of_root_directories(root_directory_names)
    check_existance_of_root_files(root_file_names)

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
    check_existance_of_directories(prefix, directory_names)

    # [ "doc/{}/index.html".format(name) for name in ["aguila", "demo", "manual", "modflow"] +
    # "doc/python/pcraster/index.html",
    # "doc/python/pcraster/framework/index.html",

    file_names = \
        ["bin/{}".format(name) for name in [
            "aguila", "asc2map", "col2map", "legend", "map2asc", "map2col",
            "mapattr", "oldcalc", "pcrcalc", "pcrseal", "resample", "table"]
        ] + \
        ["Python/PCRaster/__init__.py", "Python/PCRaster/Framework/__init__.py" ]
    check_existance_of_files(prefix, file_names)



def verify_python_package(
        prefix):
    subprocess.check_call(["python", "-c", "import PCRaster"])
    subprocess.check_call(["python", "-c", "import PCRaster.Framework"])


def check_shared_libraries(
        prefix):
    shared_library_path_names, missing_shared_library_names = \
        devenv.shared_library_dependencies([
            os.path.join(prefix, "bin", "aguila"),
            os.path.join(prefix, "bin", "pcrcalc"),
            os.path.join(prefix, "bin", "oldcalc")])
    system_shared_library_path_names, external_shared_library_path_names, \
        package_shared_library_path_names = \
            devenv.split_shared_library_path_names(shared_library_path_names)
    if external_shared_library_path_names:
        raise RuntimeError(
            "The folowing 3rd party libraries are missing from the package:\n"
            "{}".format("\n".join(external_shared_library_path_names)))

def verify_installation(
        prefix):
    result = 0

    try:
        check_existance_of_files_and_directories(prefix)
        verify_python_package(prefix)
        check_shared_libraries(prefix)
        sys.stdout.write("installation seems fine!\n")
    # except Exception, exception:
    #     sys.stderr.write("installation is not OK!\n")
    #     sys.stderr.write("error: {0}\n".format(str(exception)))
    #     result = 1
    except:
        traceback.print_exc(file=sys.stderr)
        result = 1

    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Verify that a PCRaster installation is likely to be correct")
    parser.add_argument("prefix", help="Path to PCRaster installation")

    arguments = parser.parse_args()
    prefix = os.path.abspath(arguments.prefix)
    sys.exit(verify_installation(prefix))

