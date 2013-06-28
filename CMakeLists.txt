CMAKE_MINIMUM_REQUIRED(VERSION 2.8.9)
PROJECT(PCRASTER)

SET(${CMAKE_PROJECT}_MAJOR_VERSION 4)
SET(${CMAKE_PROJECT}_MINOR_VERSION 0)
SET(${CMAKE_PROJECT}_PATCH_VERSION 0)
SET(${CMAKE_PROJECT}_PRE_RELEASE_VERSION "-rc.1")

SET(CMAKE_MODULE_PATH $ENV{CMAKE_MODULE_PATH})
INCLUDE(Site)

ADD_CUSTOM_TARGET(tests ALL)
ADD_SUBDIRECTORY(documentation)

INSTALL(
    FILES
        ${PROJECT_SOURCE_DIR}/documentation/pcraster/changes.rst
    DESTINATION
        share/pcraster
    RENAME
        CHANGES.TXT
)
INSTALL(
    FILES
        ${PROJECT_SOURCE_DIR}/documentation/pcraster/install.rst
    DESTINATION
        share/pcraster
    RENAME
        INSTALL.TXT
)
INSTALL(
    FILES
        ${DEVENV}/documentation/licenses/pcraster.txt
    DESTINATION
        share/pcraster
    RENAME
        COPYING.TXT
)
