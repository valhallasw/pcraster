#!/usr/bin/env pythonwrapper
# -*- coding: utf-8 -*-
"""
Verify that a PCRaster installation is likely to be correct.
"""
import argparse
import os
import subprocess
import sys



def check_existance_of_root_directories(
        directory_names):
    required_directory_names = ["doc", "Python", "share"]
    ### if sys.platform == "win32":
    ###     required_directory_names += ["apps"]
    ### else:
    required_directory_names += ["bin", "lib"] # , "PCRasterWorkspace"]

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
        "Python",
        "Python/PCRaster",
        "Python/PCRaster/Framework"
    ]
    check_existance_of_directories(prefix, directory_names)

    file_names = [
        "Python/PCRaster/__init__.py",
        "Python/PCRaster/Framework/__init__.py"
    ]
    check_existance_of_files(prefix, file_names)



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
        sys.stdout.write("installation seems fine!\n")
    except Exception, exception:
        sys.stderr.write("installation is not OK!\n")
        sys.stderr.write("error: {0}\n".format(str(exception)))
        result = 1

    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Verify that a PCRaster installation is likely to be correct")
    parser.add_argument("prefix", help="Path to PCRaster installation")

    arguments = parser.parse_args()
    prefix = os.path.abspath(arguments.prefix)
    sys.exit(verify_installation(prefix))

