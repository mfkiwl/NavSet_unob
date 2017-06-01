#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Rtl Fm
# Generated: Tue Nov 15 23:57:26 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_RTL_FM(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Rtl Fm")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.5e6
        self.gain_rf = gain_rf = 40
        self.gain_if = gain_if = 10
        self.gain_bb = gain_bb = 10
        self.freq = freq = 93.1e6

        ##################################################
        # Blocks
        ##################################################
        _gain_rf_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_rf_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_rf_sizer,
        	value=self.gain_rf,
        	callback=self.set_gain_rf,
        	label='RF Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_rf_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_rf_sizer,
        	value=self.gain_rf,
        	callback=self.set_gain_rf,
        	minimum=0,
        	maximum=40,
        	num_steps=80,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_rf_sizer)
        _gain_if_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_if_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_if_sizer,
        	value=self.gain_if,
        	callback=self.set_gain_if,
        	label='IF Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_if_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_if_sizer,
        	value=self.gain_if,
        	callback=self.set_gain_if,
        	minimum=1,
        	maximum=48,
        	num_steps=80,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_if_sizer)
        _gain_bb_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_bb_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_bb_sizer,
        	value=self.gain_bb,
        	callback=self.set_gain_bb,
        	label='BB Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_bb_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_bb_sizer,
        	value=self.gain_bb,
        	callback=self.set_gain_bb,
        	minimum=0,
        	maximum=20,
        	num_steps=40,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_bb_sizer)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Carrier Freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=80e6,
        	maximum=120e6,
        	num_steps=400,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(gain_rf, 0)
        self.rtlsdr_source_0.set_if_gain(gain_if, 0)
        self.rtlsdr_source_0.set_bb_gain(gain_bb, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=500,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=500e3,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.wxgui_fftsink2_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 1e6, firdes.WIN_HAMMING, 6.76))

    def get_gain_rf(self):
        return self.gain_rf

    def set_gain_rf(self, gain_rf):
        self.gain_rf = gain_rf
        self._gain_rf_slider.set_value(self.gain_rf)
        self._gain_rf_text_box.set_value(self.gain_rf)
        self.rtlsdr_source_0.set_gain(self.gain_rf, 0)

    def get_gain_if(self):
        return self.gain_if

    def set_gain_if(self, gain_if):
        self.gain_if = gain_if
        self._gain_if_slider.set_value(self.gain_if)
        self._gain_if_text_box.set_value(self.gain_if)
        self.rtlsdr_source_0.set_if_gain(self.gain_if, 0)

    def get_gain_bb(self):
        return self.gain_bb

    def set_gain_bb(self, gain_bb):
        self.gain_bb = gain_bb
        self._gain_bb_slider.set_value(self.gain_bb)
        self._gain_bb_text_box.set_value(self.gain_bb)
        self.rtlsdr_source_0.set_bb_gain(self.gain_bb, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)


def main(top_block_cls=top_RTL_FM, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
