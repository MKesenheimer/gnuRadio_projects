#ifndef VIDEO_SDL_TEST_HPP
#define VIDEO_SDL_TEST_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Not titled yet
Author: kesenheimer
GNU Radio version: 3.8.2.0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/analog/sig_source.h>
#include <gnuradio/blocks/add_blk.h>
#include <gnuradio/blocks/throttle.h>
#include <gnuradio/video_sdl/sink_s.h>



using namespace gr;



class video_sdl_test {

private:


    video_sdl::sink_s::sptr video_sdl_sink_0;
    blocks::throttle::sptr blocks_throttle_1;
    blocks::add_ss::sptr blocks_add_xx_0;
    analog::sig_source_s::sptr analog_sig_source_x_2;
    analog::sig_source_s::sptr analog_sig_source_x_1;


// Variables:
    int samp_rate = 7680000;

public:
    top_block_sptr tb;
    video_sdl_test();
    ~video_sdl_test();

    int get_samp_rate () const;
    void set_samp_rate(int samp_rate);

};


#endif

