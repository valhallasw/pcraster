Build PCRaster from scratch
===========================

Check out all PCRaster projects
-------------------------------
This step is not necessary if you already have the source code. Obtain the ``clone_pcraster_sources.sh`` script.

.. code-block:: bash

   cd $HOME
   mkdir -p Development/{projects,objects}
   clone_pcraster_sources.sh Development/projects <sourceforge username> <pcrserver username>

Build and install 3rd party stuff
---------------------------------
Determine where to put the 3rd party stuff. Create this directory. This is the root directory of the directory that will be created when building the 3rd party stuff. Examples are: ``/home/pcrteam_extern``, ``$HOME/pcrteam_extern``, ``/mnt/pcrteam_extern``, ``C:\PcrTeamExtern``.

Before executing the ``build_pcrteam_extern.sh`` script mentioned below, you may want to set ``CC``/``CXX`` to point to the correct compilers.

The ``build_pcrteam_extern.sh`` script depends on certain tools to be installed. On Debian based systems you can run ``.../devenv/scripts/machine_status.py`` to tell you what you need to install, if anything.

.. code-block:: bash

   # Create a temp location with lots of disk space.
   mkdir $HOME/tmp/3rd

   # Create a location where to install 3rd party software.
   mkdir $HOME/pcrteam_extern

   # Download/build/install 3rd party software.
   $HOME/Development/projects/devenv/scripts/build_pcrteam_extern.sh $HOME/tmp/3rd $HOME/pcrteam_extern/master-`date +"%Y%m%d"`

   # Create a symbolic link that can be updated should a new version of
   # pcrteam_extern be installed.
   cd $HOME/pcrteam_extern
   ln -s master-`date +"%Y%m%d"` master

Build PCRaster
--------------
Before building the PCRaster projects, you need to set some environment variables.

.. code-block:: bash

   unset OBJECTS

   export DEVELOPMENT_ROOT=$HOME/Development
   export PROJECTS=$DEVELOPMENT_ROOT/projects
   export PCRTEAM_EXTERN_ROOT=$HOME/pcrteam_extern

   source "$PROJECTS/devenv/configuration/profiles/Utils.sh"

Now, your environment is setup to build any of the projects that comprise PCRaster. Next you need to configure your environment for the specific project you want to build. There are bash scripts that can be sourced that do that for you. You can configure aliases to make sourcing these scripts easy:

.. code-block:: bash

   alias PCRaster-master="source $PROJECTS/pcraster/environment/configuration/PCRaster-master"

Now you can just type the name of the project (CamelCased) appended by the branch name, and optionally folowed by the build type (release or debug, default is debug): ``<project_name>-<branch_name> <build_type>?``.

To build everything, choose the PCRaster project. If you need to set ``CC``/``CXX`` explicitly, then do that *before* configuring the environment for the project.

.. code-block:: bash

   PCRaster-master
   rebuild_projects.py

Create PCRaster package
-----------------------
To create a PCRaster package for distribution you can use one of the ``make_pcraster_package_<operating system>.sh` shell scripts from ``$PCRASTER/environment/scripts``. These build the software in the current directory and create a PCRaster package that can be copied to other locations. On Linux:

.. code-block:: bash

   cd $HOME/tmp
   make_pcraster_package_linux.sh
