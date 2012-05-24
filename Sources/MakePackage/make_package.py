#!/usr/bin/env python
import devenv



# Rebuild all projects that are part of PCRaster, in the current build type.
# $DEVENV_PROJECTS
build_type = devenv.build_type()
project_names = devenv.project_names()
devenv.rebuild_projects(project_names, build_type)

# For each relevant project, create a package using an archive generator.
# -> Aguila, PcrTree2
packagable_projects = ["Aguila", "PcrTree2"]
archive_generator = "ZIP"
devenv.buildPackage(packagable_projects, archive_generator)

# Unzip the archives in different directories.
package_path_names = [devenv.package_path_name(project) for project in \
    packageable_projects]
binary_directory_path_name = devenv.binary_directory_path_name()
for package_path_name in package_path_names:
    devenv.unpack(package_path_name, binary_directory_path_name)

# Merge the contents in a new directory.
# TODO Add version.
pcraster_package_path_name = os.path.join(binary_directory_path_name,
    "PCRaster")
devenv.recreate_directory(pcraster_package_path_name)
devenv.merge_packages(package_path_names, pcraster_package_path_name)

# Create a CMake project containing the install rules for the merged archives.

# Create a package based on the merged archives.

