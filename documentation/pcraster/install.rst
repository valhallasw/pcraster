Install PCRaster
================

Requirements
------------
The PCRaster Python package depends on Python and Numpy:

* Python: Version 2.7 is required (http://www.python.org/download/).
* Numpy: Version 1.6 or later is fine (https://sourceforge.net/projects/numpy/files/NumPy/).

Linux
-----
Installing PCRaster on Linux involves these steps:

* Unzip the zip file containing the software
* Configure two environment variables so the PCRaster executables and PCRaster Python package are found.

PCRaster can be installed anywhere you want. Typical locations are ``$HOME``, ``/opt`` and ``/usr/local``.

.. code-block:: bash

   cd  /opt
   tar zxf /tmp/pcraster-lsbcc-4_x86-64.tar.gz

In order for the PCRaster executables and the Python package to be found, two environment variables must be updated with the paths to the executables and Python package, respectively. The next example assumes the use of the bash shell. When using other shells the commands may be different.

.. code-block:: bash

   export PATH=/opt/pcraster-lsbcc-4_86-64/bin:$PATH
   export PYTHONPATH=/opt/pcraster-lsbcc-4_86-64/python:$PYTHONPATH

These lines can be put in $HOME/.bash_profile to have them executed each time you login.

PCRaster is now installed and ready to be used.

.. note::

   In case the software doesn't work, verify that the Linux Standard Base (LSB) 4 package is installed.

Windows
-------
TODO

Mac OS X
--------
TODO
