/********************
GNU Radio C++ Flow Graph Source File

Title: Not titled yet
Author: kesenheimer
GNU Radio version: 3.8.2.0
********************/

#include "video_sdl_test.hpp"
using namespace gr;


video_sdl_test::video_sdl_test () {



    this->tb = gr::make_top_block("Not titled yet");


// Blocks:
    {
        this->video_sdl_sink_0 = video_sdl::sink_s::make(0, 640, 480, 0, 640, 480);
    }
    {
        this->blocks_throttle_1 = blocks::throttle::make(sizeof(short)*1, samp_rate, true);
    }
    {
        this->blocks_add_xx_0 = blocks::add_ss::make(1);
    }
    {
        this->analog_sig_source_x_2 = analog::sig_source_s::make(samp_rate, analog::GR_TRI_WAVE, 1234.5, 255, 0,0);
    }
    {
        this->analog_sig_source_x_1 = analog::sig_source_s::make(samp_rate, analog::GR_COS_WAVE, 10000, 255, 0,0);
    }

// Connections:
    this->tb->hier_block2::connect(this->analog_sig_source_x_1, 0, this->blocks_add_xx_0, 0);
    this->tb->hier_block2::connect(this->analog_sig_source_x_2, 0, this->blocks_add_xx_0, 1);
    this->tb->hier_block2::connect(this->blocks_add_xx_0, 0, this->blocks_throttle_1, 0);
    this->tb->hier_block2::connect(this->blocks_throttle_1, 0, this->video_sdl_sink_0, 0);
}

video_sdl_test::~video_sdl_test () {
}

// Callbacks:
int video_sdl_test::get_samp_rate () const {
    return this->samp_rate;
}

void video_sdl_test::set_samp_rate (int samp_rate) {
    this->samp_rate = samp_rate;
    this->analog_sig_source_x_1->set_sampling_freq(this->samp_rate);
    this->analog_sig_source_x_2->set_sampling_freq(this->samp_rate);
    this->blocks_throttle_1->set_sample_rate(this->samp_rate);
}


int main (int argc, char **argv) {
    if (enable_realtime_scheduling() != RT_OK) {
        std::cout << "Error: failed to enable real-time scheduling." << std::endl;
    }

    video_sdl_test* top_block = new video_sdl_test();
    top_block->tb->start();
    std::cout << "Press Enter to quit: ";
    std::cin.ignore();
    top_block->tb->stop();
    top_block->tb->wait();

    return 0;
}
