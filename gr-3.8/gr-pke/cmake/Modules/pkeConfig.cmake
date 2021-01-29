INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_PKE pke)

FIND_PATH(
    PKE_INCLUDE_DIRS
    NAMES pke/api.h
    HINTS $ENV{PKE_DIR}/include
        ${PC_PKE_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    PKE_LIBRARIES
    NAMES gnuradio-pke
    HINTS $ENV{PKE_DIR}/lib
        ${PC_PKE_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/pkeTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(PKE DEFAULT_MSG PKE_LIBRARIES PKE_INCLUDE_DIRS)
MARK_AS_ADVANCED(PKE_LIBRARIES PKE_INCLUDE_DIRS)
