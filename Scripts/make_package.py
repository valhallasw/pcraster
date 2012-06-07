#!/usr/bin/env pythonwrapper
# -*- coding: utf-8 -*-
import argparse
import os
import multiprocessing
import shutil
import sys
import traceback
import devenv
import verify_pcraster_installation



def cpack_archive_generator_name():
    return "ZIP" if sys.platform == "win32" else "TGZ"

def make_package(
        build,
        rebuild,
        build_packages):
    result = 0

    try:
        # (Re)build all projects that are part of PCRaster, in the current build
        # type.
        build_type = devenv.build_type()
        project_names = devenv.project_names()
        if build:
            if rebuild:
                devenv.rebuild_projects(project_names, build_type)
            else:
                devenv.build_projects(project_names, build_type)

        # For each relevant project, create a package using an archive
        # generator.
        packageable_project_names = ["Aguila", "PcrTree2", "DataAssimilation"]
        cpack_generator_name = cpack_archive_generator_name()
        if build_packages:
            devenv.build_packages(packageable_project_names,
                cpack_generator_name, build_type)

        # Unzip the archives in different directories.
        package_path_names = devenv.package_path_names(
            packageable_project_names, cpack_generator_name)
        binary_directory_path_name = devenv.project_binary_directory_path_name(
            "PCRaster")
        assert os.path.isdir(binary_directory_path_name)
        devenv.unpack_packages(package_path_names, binary_directory_path_name)

        # Merge the contents in a new directory.
        package_base_names = devenv.package_base_names(
            packageable_project_names)
        package_directory_path_names = [os.path.join(
            binary_directory_path_name, package_base_name) for \
                package_base_name in package_base_names]
        pcraster_package_source_directory_path_name = os.path.join(
            binary_directory_path_name, "PCRasterPackage")
        if os.path.isdir(pcraster_package_source_directory_path_name):
            shutil.rmtree(pcraster_package_source_directory_path_name)
        devenv.merge_packages(package_directory_path_names,
            pcraster_package_source_directory_path_name)

        # Create a CMake project containing the install rules for the merged
        # archives.
        file(os.path.join(pcraster_package_source_directory_path_name,
            "CMakeLists.txt"), "w").write("""\
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
PROJECT(PCRasterPackage)

SET(PCRASTERPACKAGE_MAJOR_VERSION 4)
SET(PCRASTERPACKAGE_MINOR_VERSION 0)
SET(PCRASTERPACKAGE_PATCH_VERSION 0)

SET(CMAKE_MODULE_PATH $ENV{CMAKE_MODULE_PATH})
INCLUDE(Site)

FILE(GLOB FILE_NAMES *)
FOREACH(FILE_NAME IN ITEMS ${FILE_NAMES})
  GET_FILENAME_COMPONENT(NAME ${FILE_NAME} NAME)
  MESSAGE(${NAME})
  IF(${NAME} STREQUAL "CMakeLists.txt")
    LIST(REMOVE_ITEM FILE_NAMES ${FILE_NAME})
  ENDIF()
ENDFOREACH()

SET(DIRECTORY_PATH_NAMES)
SET(REGULAR_FILE_PATH_NAMES)

FOREACH(FILE_NAME IN ITEMS ${FILE_NAMES})
  IF(IS_DIRECTORY ${FILE_NAME})
    LIST(APPEND DIRECTORY_PATH_NAMES ${FILE_NAME})
  ELSE()
    LIST(APPEND REGULAR_FILE_PATH_NAMES ${FILE_NAME})
  ENDIF()
ENDFOREACH()

INSTALL(DIRECTORY ${DIRECTORY_PATH_NAMES} DESTINATION .)
INSTALL(FILES ${REGULAR_FILE_PATH_NAMES} DESTINATION .)

SET(CPACK_PACKAGE_NAME PCRaster)
SET(CPACK_PACKAGE_VERSION_MAJOR ${PCRASTERPACKAGE_MAJOR_VERSION})
SET(CPACK_PACKAGE_VERSION_MINOR ${PCRASTERPACKAGE_MINOR_VERSION})
SET(CPACK_PACKAGE_VERSION_PATCH ${PCRASTERPACKAGE_PATCH_VERSION})

INCLUDE(CPack)
""")

        os.environ["PCRASTERPACKAGE"] = \
            pcraster_package_source_directory_path_name

        # Create a package based on the merged archives.
        devenv.rebuild_project("PCRasterPackage", build_type)
        devenv.build_package("PCRasterPackage", cpack_generator_name,
            build_type)

        # Unpack package.
        package_path_name = devenv.package_path_name("PCRasterPackage",
            cpack_generator_name)
        binary_directory_path_name = devenv.project_binary_directory_path_name(
            "PCRasterPackage")
        assert os.path.isdir(binary_directory_path_name)
        devenv.unpack_package(package_path_name, binary_directory_path_name)

        # Verify final package.
        package_base_name = devenv.package_base_name("PCRasterPackage")
        package_directory_path_name = os.path.join(binary_directory_path_name,
            package_base_name)
        verify_pcraster_installation.verify_installation(
            package_directory_path_name)

        del os.environ["PCRASTERPACKAGE"]
    except:
        traceback.print_exc(file=sys.stderr)
        result = 1
    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make PCRaster package")
    parser.add_argument("--skip_build", dest="build", action="store_const",
        const=False, default=True,
        help="skip build of targets")
    parser.add_argument("--no_rebuild", dest="rebuild", action="store_const",
        const=False, default=True, help="build targets instead of rebuild")
    parser.add_argument("--skip_build_packages", dest="build_packages",
        action="store_const", const=False, default=True,
        help="skip build of packages")
    arguments = parser.parse_args()
    sys.exit(make_package(build=arguments.build, rebuild=arguments.rebuild,
        build_packages=arguments.build_packages))

