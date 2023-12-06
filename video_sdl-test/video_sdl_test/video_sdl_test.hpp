#ifndef VIDEO_SDL_TEST_HPP
#define VIDEO_SDL_TEST_HPP
/********************
GNU Radio C++ Flow Graph Header File

Title: Not titled yet
Author: kesenheimer
GNU Radio version: 3.10.8.0
********************/

/********************
** Create includes
********************/
#include <gnuradio/top_block.h>
#include <gnuradio/analog/sig_source.h>
#include <gnuradio/blocks/add_blk.h>
#include <gnuradio/blocks/throttle.h>
#include <string_view>
#include <algorithm>
#include <gnuradio/video_sdl/sink_s.h>

#include <QVBoxLayout>
#include <QScrollArea>
#include <QWidget>
#include <QGridLayout>
#include <QSettings>
#include <QApplication>


using namespace gr;



class video_sdl_test : public QWidget {
    Q_OBJECT

private:
    QVBoxLayout *top_scroll_layout;
    QScrollArea *top_scroll;
    QWidget *top_widget;
    QVBoxLayout *top_layout;
    QGridLayout *top_grid_layout;
    QSettings *settings;


    video_sdl::sink_s::sptr video_sdl_sink_0;
    constexpr unsigned int blocks_throttle2_0_limit(float value) {
      const std::string_view limited("auto");
      if(limited == "time") {
        return std::max(static_cast<unsigned int>(value * samp_rate), 1U);
      } else if (limited == "items") {
        return std::max(static_cast<unsigned int>(value), 1U);
      }
      return 0;
    }
    blocks::throttle::sptr blocks_throttle2_0;
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

