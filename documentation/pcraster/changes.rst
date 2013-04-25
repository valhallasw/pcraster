Changes
=======

PCRaster 4.0.0 (in development)
-------------------------------
General
^^^^^^^
* The installation process of PCRaster has been symplified. On all platforms we distribute a zip file which can be unzipped at a preferred location. After setting two environment variables, PCRaster is ready to be used. The goal is to make it possible to have install multiple versions of PCRaster at the same time. This has the advantage that older models can still be run with older installed versions of PCRaster. And it allows us to keep improving PCRaster, even if we brake backwards compatibility (we prefer not to, but sometimes there is a good reason).
* Removed support for reading Hdf4 formatted rasters. Maintaining support for this format proved to be much of a hassle.

PCRaster Python package
^^^^^^^^^^^^^^^^^^^^^^^
* Updated the code to prevent that the memory used by the PCRaster Python extension increases during a model run.
* PCRaster Python package now depends on Python 2.7.
* PCRaster Python package uses lower case names for package names. Update all PCRaster related imports and change them to lower case. See also the `Style Guide for Python Code <http://www.python.org/dev/peps/pep-0008/>`_.
* Removed ``pcraster.numpy`` sub-package. Numpy functionality is merged in the ``pcraster`` main package and available without an explicit import of the ``numpy`` sub-package. Remove any import of ``pcraster.numpy`` and rename any calls of ``pcraster.numpy.pcr2numpy`` and ``pcraster.numpy.numpy2pcr`` to ``pcraster.pcr2numpy`` and ``pcraster.numpy2pcr``.
* Removed ``pcr2numarray`` and ``numarray2pcr`` which were already deprecated. Use ``pcr2numpy`` and ``numpy2pcr``.
