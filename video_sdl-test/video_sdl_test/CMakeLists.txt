# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Not titled yet
# Author: kesenheimer
# GNU Radio version: 3.10.8.0


cmake_minimum_required(VERSION 3.8)
set(CMAKE_CXX_STANDARD 14)

project(video_sdl_test)

find_package(Gnuradio "3.10" COMPONENTS
    blocks
    fec
    fft
    filter
    analog
    digital
    dtv
    audio
    channels
    pdu
    iio
    qtgui
    trellis
    uhd
    uhd UHD 4.0 RFNoC
    video-sdl
    vocoder
    wavelet
    zeromq
    network
    soapy
)

find_package(Qt5Widgets REQUIRED)
set(CMAKE_AUTOMOC TRUE)



add_executable(video_sdl_test video_sdl_test.cpp)
target_link_libraries(video_sdl_test
    gnuradio::gnuradio-blocks
    gnuradio::gnuradio-qtgui
    gnuradio::gnuradio-video_sdl
    gnuradio::gnuradio-analog
)

