# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Not titled yet
# Author: kesenheimer
# GNU Radio version: 3.8.2.0


cmake_minimum_required(VERSION 3.8)


include_directories(
    ${GNURADIO_ALL_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    $ENV{HOME}/.grc_gnuradio
)




set(GR_LIBRARIES
    boost_system
    gnuradio-blocks
    gnuradio-runtime
    gnuradio-pmt
    log4cpp
    gnuradio-video_sdl
    gnuradio-analog
)

add_executable(video_sdl_test video_sdl_test.cpp)
target_link_libraries(video_sdl_test ${GR_LIBRARIES})
