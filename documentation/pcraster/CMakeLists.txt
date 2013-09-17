SET(SPHINX_SOURCES
    build.rst
    changes.rst
    develop.rst
    index.rst
    install.rst
)
SET(SPHINX_TARGET pcraster)
INCLUDE(SphinxDoc)

INSTALL(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/_build/html/
    DESTINATION doc/pcraster
)
