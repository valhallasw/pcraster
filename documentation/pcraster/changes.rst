Changes
=======

PCRaster 4.0.0 (in development)
-------------------------------
General
^^^^^^^
* Changed the license of all PCRaster source code to the `GPLv3 <http://www.gnu.org/licenses/gpl-3.0.html>`_ open source license. Moved all sourcecode to the `PCRaster Open Source Tools site <https://sourceforge.net/projects/pcraster/>`_ at SourceForge.
* The installation process of PCRaster has been symplified. On all platforms we distribute a zip file which can be unzipped at a preferred location. After setting two environment variables, PCRaster is ready to be used. The goal is to make it possible to install multiple versions of PCRaster at the same time. This has the advantage that older models can still be run with older installed versions of PCRaster. And it allows us to keep improving PCRaster, even if we break backwards compatibility (we prefer not to, but sometimes there is a good reason).
* Removed support for reading HDF4 formatted rasters. Maintaining support for this format proved to be too much of a hassle.

pcrcalc
^^^^^^^
* Removed support for encrypting models.
* Removed support for license specific functionality (like missing value compression). All features that used to require a commercial license are available for everybody now.

PCRaster Python package
^^^^^^^^^^^^^^^^^^^^^^^
* Updated the code to allow the garbage collector to reclaim memory used by some of the framework class instanceѕ, after the last reference goes out of scope.
* Updated the code to prevent that the memory used by the PCRaster Python extension increases during a model run.
* PCRaster Python package now depends on Python 2.7.
* PCRaster Python package uses lower case names for package names. Update all PCRaster related imports and change them to lower case. See also the `Style Guide for Python Code <http://www.python.org/dev/peps/pep-0008/>`_.
* Removed ``pcraster.numpy`` sub-package. Numpy functionality is merged in the ``pcraster`` main package and available without an explicit import of the ``numpy`` sub-package. Remove any import of ``pcraster.numpy`` and rename any calls of ``pcraster.numpy.pcr2numpy`` and ``pcraster.numpy.numpy2pcr`` to ``pcraster.pcr2numpy`` and ``pcraster.numpy2pcr``.
* Removed ``pcr2numarray`` and ``numarray2pcr`` which were already deprecated. Use ``pcr2numpy`` and ``numpy2pcr``.
* Reimplemented ``numpy2pcr``. It is faster now.
* Added a `setclone` overload taking `nrRows`, `nrCols`, `cellSize`, `west`, `north`. No need to pass the name of an existing raster anymore.

MODFLOW extension
^^^^^^^^^^^^^^^^^
* Fixed a crash.
* Renamed extention from ``PCRasterModflow`` to ``pcraster_modflow``.
