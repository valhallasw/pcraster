#!/usr/bin/env pythonwrapper
# -*- coding: utf-8 -*-
import argparse
import os
import sys
import traceback
import devenv



def cpack_archive_generator_name():
    return "ZIP" if sys.platform == "win32" else "TGZ"

def make_package():
    result = 0

    try:
      # Rebuild all projects that are part of PCRaster, in the current build
      # type.
      build_type = devenv.build_type()
      project_names = devenv.project_names()
      ### devenv.build_projects(project_names, build_type)
      ### devenv.rebuild_projects(project_names, build_type)

      # For each relevant project, create a package using an archive generator.
      ### packageable_project_names = ["Aguila", "PcrTree2"]
      packageable_project_names = ["Aguila"]
      cpack_generator_name = cpack_archive_generator_name()
      ### devenv.build_packages(packageable_project_names, cpack_generator_name,
      ###     build_type)

      # Unzip the archives in different directories.
      package_path_names = devenv.package_path_names(packageable_project_names,
          cpack_generator_name)
      binary_directory_path_name = devenv.project_binary_directory_path_name(
          "PCRaster")
      assert os.path.isdir(binary_directory_path_name)
      devenv.unpack_packages(package_path_names, binary_directory_path_name)

      # Merge the contents in a new directory.
      package_directory_names = devenv.package_directory_names(
          packageable_project_names)
      package_directory_names
      package_directory_path_names = [os.path.join(
          binary_directory_path_name, package_directory_name) for \
              package_directory_name in package_directory_names]
      pcraster_package_path_name = os.path.join(binary_directory_path_name,
          "PCRaster")
      devenv.recreate_directory(pcraster_package_path_name)
      devenv.merge_packages(package_directory_path_names,
          pcraster_package_path_name)

      # Create a CMake project containing the install rules for the merged
      # archives.

      # Create a package based on the merged archives.

    except:
        traceback.print_exc(file=sys.stderr)
        result = 1
    return result



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make PCRaster package")
    arguments = parser.parse_args()
    sys.exit(make_package())

