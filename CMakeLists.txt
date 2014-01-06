CMAKE_MINIMUM_REQUIRED(VERSION 2.8.9)
PROJECT(PCRASTER)

SET(CMAKE_MODULE_PATH $ENV{CMAKE_MODULE_PATH})
INCLUDE(Site)
PCR_SET_PROJECT_VERSIONS("4" "1" "0")

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
