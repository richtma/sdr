#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Simple FM (Stereo) Receiver
# Author: Marcus Leech
# Generated: Mon May 21 22:55:26 2012
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import baz
import math
import simple_fm_helper
import threading
import time
import wx

class simple_fm_rcv(grc_wxgui.top_block_gui):

	def __init__(self, devid="type=b100", rdsfile="rds_fifo", gain=35.0, freq=101.1e6, xmlport=13777, arate=int(48e3), mute=-15.0, ftune=0, ant="J1", subdev="A:0", ahw="pulse", deemph=75.0e-6, prenames='["UWRF","89.3","950","WEVR"]', prefreqs="[88.715e6,89.3e6,950.735e6,106.317e6]", volume=1.0):
		grc_wxgui.top_block_gui.__init__(self, title="Simple FM (Stereo) Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Parameters
		##################################################
		self.devid = devid
		self.rdsfile = rdsfile
		self.gain = gain
		self.freq = freq
		self.xmlport = xmlport
		self.arate = arate
		self.mute = mute
		self.ftune = ftune
		self.ant = ant
		self.subdev = subdev
		self.ahw = ahw
		self.deemph = deemph
		self.prenames = prenames
		self.prefreqs = prefreqs
		self.volume = volume

		##################################################
		# Variables
		##################################################
		self.pthresh = pthresh = 350
		self.preselect = preselect = eval(prefreqs)[0]
		self.pilot_level = pilot_level = 0
		self.ifreq = ifreq = freq
		self.stpilotdet = stpilotdet = True if (pilot_level > pthresh) else False
		self.stereo = stereo = True
		self.rf_pwr_lvl = rf_pwr_lvl = 0
		self.cur_freq = cur_freq = simple_fm_helper.freq_select(ifreq,preselect)
		self.vol = vol = volume
		self.variable_static_text_0 = variable_static_text_0 = 10.0*math.log(rf_pwr_lvl+1.0e-11)/math.log(10)
		self.tone_med = tone_med = 5
		self.tone_low = tone_low = 5
		self.tone_high = tone_high = 5
		self.stereo_0 = stereo_0 = stpilotdet
		self.st_enabled = st_enabled = 1 if (stereo == True and pilot_level > pthresh) else 0
		self.squelch_probe = squelch_probe = 0
		self.sq_thresh = sq_thresh = mute
		self.samp_rate = samp_rate = 250e3
		self.rtext_0 = rtext_0 = cur_freq
		self.record = record = False
		self.rdsrate = rdsrate = 25e3
		self.osmo_taps = osmo_taps = firdes.low_pass(1.0,1.00e6,95e3,20e3,firdes.WIN_HAMMING,6.76)
		self.mod_reset = mod_reset = 0
		self.igain = igain = gain
		self.fine = fine = ftune
		self.farate = farate = arate
		self.dm = dm = deemph
		self.discrim_dc = discrim_dc = 0
		self.capture_file = capture_file = "capture.wav"
		self.asrate = asrate = 125e3

		##################################################
		# Blocks
		##################################################
		_sq_thresh_sizer = wx.BoxSizer(wx.VERTICAL)
		self._sq_thresh_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_sq_thresh_sizer,
			value=self.sq_thresh,
			callback=self.set_sq_thresh,
			label="Mute Level",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._sq_thresh_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_sq_thresh_sizer,
			value=self.sq_thresh,
			callback=self.set_sq_thresh,
			minimum=-30.0,
			maximum=-5.0,
			num_steps=40,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_sq_thresh_sizer, 1, 5, 1, 1)
		self.input_power = gr.probe_avg_mag_sqrd_c(sq_thresh, 1.0/(samp_rate/10))
		self.dc_level = gr.probe_signal_f()
		_vol_sizer = wx.BoxSizer(wx.VERTICAL)
		self._vol_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_vol_sizer,
			value=self.vol,
			callback=self.set_vol,
			label="Volume",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._vol_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_vol_sizer,
			value=self.vol,
			callback=self.set_vol,
			minimum=0,
			maximum=11,
			num_steps=110,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_vol_sizer, 0, 3, 1, 1)
		_tone_med_sizer = wx.BoxSizer(wx.VERTICAL)
		self._tone_med_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_tone_med_sizer,
			value=self.tone_med,
			callback=self.set_tone_med,
			label="1Khz-4Khz",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._tone_med_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_tone_med_sizer,
			value=self.tone_med,
			callback=self.set_tone_med,
			minimum=0,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_tone_med_sizer, 1, 3, 1, 1)
		_tone_low_sizer = wx.BoxSizer(wx.VERTICAL)
		self._tone_low_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_tone_low_sizer,
			value=self.tone_low,
			callback=self.set_tone_low,
			label="0-1Khz",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._tone_low_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_tone_low_sizer,
			value=self.tone_low,
			callback=self.set_tone_low,
			minimum=0,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_tone_low_sizer, 1, 2, 1, 1)
		_tone_high_sizer = wx.BoxSizer(wx.VERTICAL)
		self._tone_high_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_tone_high_sizer,
			value=self.tone_high,
			callback=self.set_tone_high,
			label="4Khz-15Khz",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._tone_high_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_tone_high_sizer,
			value=self.tone_high,
			callback=self.set_tone_high,
			minimum=0,
			maximum=10,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_tone_high_sizer, 1, 4, 1, 1)
		def _squelch_probe_probe():
			while True:
				val = self.input_power.unmuted()
				try: self.set_squelch_probe(val)
				except AttributeError, e: pass
				time.sleep(1.0/(10))
		_squelch_probe_thread = threading.Thread(target=_squelch_probe_probe)
		_squelch_probe_thread.daemon = True
		_squelch_probe_thread.start()
		self._record_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.record,
			callback=self.set_record,
			label="Record Audio",
			true=True,
			false=False,
		)
		self.GridAdd(self._record_check_box, 2, 2, 1, 1)
		self.pilot_probe = gr.probe_signal_f()
		_fine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._fine_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_fine_sizer,
			value=self.fine,
			callback=self.set_fine,
			label="Fine Tuning",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._fine_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_fine_sizer,
			value=self.fine,
			callback=self.set_fine,
			minimum=-50.0e3,
			maximum=50.e03,
			num_steps=400,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_fine_sizer, 1, 0, 1, 1)
		def _discrim_dc_probe():
			while True:
				val = self.dc_level.level()
				try: self.set_discrim_dc(val)
				except AttributeError, e: pass
				time.sleep(1.0/(2.5))
		_discrim_dc_thread = threading.Thread(target=_discrim_dc_probe)
		_discrim_dc_thread.daemon = True
		_discrim_dc_thread.start()
		self._capture_file_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.capture_file,
			callback=self.set_capture_file,
			label="Record Filename",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._capture_file_text_box, 2, 0, 1, 2)
		self.Main = self.Main = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.Main.AddPage(grc_wxgui.Panel(self.Main), "L/R")
		self.Main.AddPage(grc_wxgui.Panel(self.Main), "FM Demod Spectrum")
		self.Add(self.Main)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.GetWin(),
			baseband_freq=0,
			dynamic_range=100,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
		)
		self.Add(self.wxgui_waterfallsink2_0.win)
		self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
			self.Main.GetPage(0).GetWin(),
			title="Audio Channels (L and R)",
			sample_rate=farate,
			v_scale=0,
			v_offset=0,
			t_scale=0,
			ac_couple=False,
			xy_mode=False,
			num_inputs=2,
			trig_mode=gr.gr_TRIG_MODE_AUTO,
			y_axis_label="Rel. Audio Level",
		)
		self.Main.GetPage(0).Add(self.wxgui_scopesink2_0.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
			self.Main.GetPage(1).GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=asrate,
			fft_size=1024,
			fft_rate=6,
			average=True,
			avg_alpha=0.1,
			title="FM Demod Spectrum",
			peak_hold=False,
		)
		self.Main.GetPage(1).Add(self.wxgui_fftsink2_0.win)
		self._variable_static_text_0_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.variable_static_text_0,
			callback=self.set_variable_static_text_0,
			label="RF Power ",
			converter=forms.float_converter(formatter=lambda x: "%4.1f" % x),
		)
		self.GridAdd(self._variable_static_text_0_static_text, 0, 2, 1, 1)
		self._stereo_0_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.stereo_0,
			callback=self.set_stereo_0,
			label="Stereo Detect",
			true=True,
			false=False,
		)
		self.GridAdd(self._stereo_0_check_box, 2, 5, 1, 1)
		self._stereo_check_box = forms.check_box(
			parent=self.GetWin(),
			value=self.stereo,
			callback=self.set_stereo,
			label="Stereo",
			true=True,
			false=False,
		)
		self.GridAdd(self._stereo_check_box, 2, 4, 1, 1)
		self.rtl2832_source_0 = baz.rtl_source_c(defer_creation=True)
		self.rtl2832_source_0.set_verbose(True)
		self.rtl2832_source_0.set_vid(0x0)
		self.rtl2832_source_0.set_pid(0x0)
		self.rtl2832_source_0.set_tuner_name("")
		self.rtl2832_source_0.set_default_timeout(0)
		self.rtl2832_source_0.set_use_buffer(True)
		self.rtl2832_source_0.set_fir_coefficients(([]))
		
		
		
		
		
		if self.rtl2832_source_0.create() == False: raise Exception("Failed to create RTL2832 Source: rtl2832_source_0")
		
		
		self.rtl2832_source_0.set_sample_rate(1.0e6)
		
		self.rtl2832_source_0.set_frequency(cur_freq+200e3)
		
		
		self.rtl2832_source_0.set_auto_gain_mode(False)
		self.rtl2832_source_0.set_relative_gain(True)
		self.rtl2832_source_0.set_gain(gain)
		  
		self._rtext_0_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.rtext_0,
			callback=self.set_rtext_0,
			label="CURRENT FREQUENCY>>",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._rtext_0_static_text, 0, 1, 1, 1)
		def _rf_pwr_lvl_probe():
			while True:
				val = self.input_power.level()
				try: self.set_rf_pwr_lvl(val)
				except AttributeError, e: pass
				time.sleep(1.0/(2))
		_rf_pwr_lvl_thread = threading.Thread(target=_rf_pwr_lvl_probe)
		_rf_pwr_lvl_thread.daemon = True
		_rf_pwr_lvl_thread.start()
		self._preselect_chooser = forms.radio_buttons(
			parent=self.GetWin(),
			value=self.preselect,
			callback=self.set_preselect,
			label='preselect',
			choices=eval(prefreqs),
			labels=eval(prenames),
			style=wx.RA_HORIZONTAL,
		)
		self.GridAdd(self._preselect_chooser, 0, 4, 1, 1)
		def _pilot_level_probe():
			while True:
				val = self.pilot_probe.level()
				try: self.set_pilot_level(val)
				except AttributeError, e: pass
				time.sleep(1.0/(5))
		_pilot_level_thread = threading.Thread(target=_pilot_level_probe)
		_pilot_level_thread.daemon = True
		_pilot_level_thread.start()
		self.low_pass_filter_3 = gr.fir_filter_fff(1, firdes.low_pass(
			3, asrate/500, 10, 3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_2 = gr.fir_filter_fff(10, firdes.low_pass(
			3, asrate/50, 100, 30, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1 = gr.fir_filter_fff(10, firdes.low_pass(
			3, asrate/5, 1e3, 200, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0 = gr.fir_filter_fff(5, firdes.low_pass(
			3, asrate, 10e3, 2e3, firdes.WIN_HAMMING, 6.76))
		_igain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._igain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_igain_sizer,
			value=self.igain,
			callback=self.set_igain,
			label="RF Gain",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._igain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_igain_sizer,
			value=self.igain,
			callback=self.set_igain,
			minimum=0,
			maximum=50,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_igain_sizer, 1, 1, 1, 1)
		_ifreq_sizer = wx.BoxSizer(wx.VERTICAL)
		self._ifreq_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_ifreq_sizer,
			value=self.ifreq,
			callback=self.set_ifreq,
			label="Center Frequency",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._ifreq_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_ifreq_sizer,
			value=self.ifreq,
			callback=self.set_ifreq,
			minimum=88.1e6,
			maximum=108.1e6,
			num_steps=200,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_ifreq_sizer, 0, 0, 1, 1)
		self.gr_wavfile_sink_0 = gr.wavfile_sink("/dev/null" if record == False else capture_file, 2, int(farate), 16)
		self.gr_sub_xx_0 = gr.sub_ff(1)
		self.gr_single_pole_iir_filter_xx_1 = gr.single_pole_iir_filter_ff(2.5/(asrate/500), 1)
		self.gr_single_pole_iir_filter_xx_0 = gr.single_pole_iir_filter_ff(1.0/(asrate/3), 1)
		self.gr_multiply_xx_1 = gr.multiply_vff(1)
		self.gr_multiply_xx_0_0 = gr.multiply_vff(1)
		self.gr_multiply_xx_0 = gr.multiply_vff(1)
		self.gr_multiply_const_vxx_3 = gr.multiply_const_vff((3.16e3 if st_enabled else 0, ))
		self.gr_multiply_const_vxx_2 = gr.multiply_const_vff((1.0 if st_enabled else 1.414, ))
		self.gr_multiply_const_vxx_1_0 = gr.multiply_const_vff((0 if st_enabled else 1, ))
		self.gr_multiply_const_vxx_1 = gr.multiply_const_vff((0 if squelch_probe == 0 else 1.0, ))
		self.gr_multiply_const_vxx_0_0 = gr.multiply_const_vff((vol*1.5*10.0, ))
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vff((vol*1.5*10.0 if st_enabled else 0, ))
		self.gr_keep_one_in_n_0 = gr.keep_one_in_n(gr.sizeof_float*1, int(asrate/3))
		self.gr_freq_xlating_fir_filter_xxx_0 = gr.freq_xlating_fir_filter_ccc(4, (osmo_taps), 200e3+fine+(-12e3*discrim_dc), 1.0e6)
		self.gr_fractional_interpolator_xx_0_0 = gr.fractional_interpolator_ff(0, asrate/farate)
		self.gr_fractional_interpolator_xx_0 = gr.fractional_interpolator_ff(0, asrate/farate)
		self.gr_fft_filter_xxx_1_0_0 = gr.fft_filter_fff(1, (firdes.band_pass(tone_high/10.0,asrate,3.5e3,15.0e3,5.0e3,firdes.WIN_HAMMING)), 1)
		self.gr_fft_filter_xxx_1_0 = gr.fft_filter_fff(1, (firdes.band_pass(tone_med/10.0,asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)), 1)
		self.gr_fft_filter_xxx_1 = gr.fft_filter_fff(1, (firdes.low_pass(tone_low/10.0,asrate,1.2e3,500,firdes.WIN_HAMMING)), 1)
		self.gr_fft_filter_xxx_0_0_0 = gr.fft_filter_fff(1, (firdes.band_pass(tone_high/10.0,asrate,3.5e3,13.5e3,3.5e3,firdes.WIN_HAMMING)), 1)
		self.gr_fft_filter_xxx_0_0 = gr.fft_filter_fff(1, (firdes.band_pass(tone_med/10.0,asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)), 1)
		self.gr_fft_filter_xxx_0 = gr.fft_filter_fff(1, (firdes.low_pass(tone_low/10.0,asrate,1.2e3,500,firdes.WIN_HAMMING)), 1)
		self.gr_divide_xx_0 = gr.divide_ff(1)
		self.gr_agc_xx_1 = gr.agc_cc(1e-2, 0.35, 1.0, 5000)
		self.gr_add_xx_2_0 = gr.add_vff(1)
		self.gr_add_xx_2 = gr.add_vff(1)
		self.gr_add_xx_1 = gr.add_vff(1)
		self.gr_add_xx_0 = gr.add_vff(1)
		self.gr_add_const_vxx_0 = gr.add_const_vff((1.0e-7, ))
		self._dm_chooser = forms.radio_buttons(
			parent=self.GetWin(),
			value=self.dm,
			callback=self.set_dm,
			label="FM Deemphasis",
			choices=[75.0e-6, 50.0e-6],
			labels=["NA", "EU"],
			style=wx.RA_HORIZONTAL,
		)
		self.GridAdd(self._dm_chooser, 0, 5, 1, 1)
		self.blks2_wfm_rcv_0 = blks2.wfm_rcv(
			quad_rate=samp_rate,
			audio_decimation=2,
		)
		self.blks2_fm_deemph_0_0 = blks2.fm_deemph(fs=farate, tau=deemph)
		self.blks2_fm_deemph_0 = blks2.fm_deemph(fs=farate, tau=deemph)
		self.band_pass_filter_2_0 = gr.fir_filter_fff(1, firdes.band_pass(
			20, asrate, 17.5e3, 17.9e3, 250, firdes.WIN_HAMMING, 6.76))
		self.band_pass_filter_2 = gr.fir_filter_fff(1, firdes.band_pass(
			10, asrate, 18.8e3, 19.2e3, 350, firdes.WIN_HAMMING, 6.76))
		self.band_pass_filter_0_0 = gr.fir_filter_fff(1, firdes.band_pass(
			1, asrate, 38e3-(15e3), 38e3+(15e3), 4.0e3, firdes.WIN_HAMMING, 6.76))
		self.audio_sink_0 = audio.sink(int(farate), "" if ahw == "Default" else ahw, True)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_add_xx_1, 0), (self.gr_fractional_interpolator_xx_0, 0))
		self.connect((self.gr_sub_xx_0, 0), (self.gr_fractional_interpolator_xx_0_0, 0))
		self.connect((self.band_pass_filter_0_0, 0), (self.gr_multiply_xx_1, 0))
		self.connect((self.gr_multiply_const_vxx_1_0, 0), (self.gr_add_xx_0, 0))
		self.connect((self.band_pass_filter_2_0, 0), (self.gr_multiply_xx_0, 0))
		self.connect((self.band_pass_filter_2_0, 0), (self.gr_multiply_xx_0, 1))
		self.connect((self.gr_multiply_xx_0_0, 0), (self.gr_divide_xx_0, 0))
		self.connect((self.gr_divide_xx_0, 0), (self.gr_single_pole_iir_filter_xx_0, 0))
		self.connect((self.gr_multiply_xx_0, 0), (self.gr_add_const_vxx_0, 0))
		self.connect((self.gr_add_const_vxx_0, 0), (self.gr_divide_xx_0, 1))
		self.connect((self.gr_single_pole_iir_filter_xx_0, 0), (self.gr_keep_one_in_n_0, 0))
		self.connect((self.gr_keep_one_in_n_0, 0), (self.pilot_probe, 0))
		self.connect((self.band_pass_filter_2, 0), (self.gr_multiply_xx_1, 2))
		self.connect((self.band_pass_filter_2, 0), (self.gr_multiply_xx_0_0, 0))
		self.connect((self.gr_multiply_const_vxx_2, 0), (self.gr_add_xx_1, 0))
		self.connect((self.gr_multiply_const_vxx_2, 0), (self.gr_sub_xx_0, 0))
		self.connect((self.gr_multiply_const_vxx_3, 0), (self.gr_sub_xx_0, 1))
		self.connect((self.gr_multiply_const_vxx_3, 0), (self.gr_add_xx_1, 1))
		self.connect((self.gr_fractional_interpolator_xx_0, 0), (self.gr_multiply_const_vxx_0_0, 0))
		self.connect((self.gr_fractional_interpolator_xx_0_0, 0), (self.gr_multiply_const_vxx_0, 0))
		self.connect((self.band_pass_filter_2, 0), (self.gr_multiply_xx_1, 1))
		self.connect((self.gr_multiply_xx_1, 0), (self.gr_fft_filter_xxx_0, 0))
		self.connect((self.gr_fft_filter_xxx_1, 0), (self.gr_add_xx_2, 0))
		self.connect((self.gr_fft_filter_xxx_1_0, 0), (self.gr_add_xx_2, 1))
		self.connect((self.gr_fft_filter_xxx_1_0_0, 0), (self.gr_add_xx_2, 2))
		self.connect((self.gr_add_xx_2, 0), (self.gr_multiply_const_vxx_2, 0))
		self.connect((self.gr_add_xx_2_0, 0), (self.gr_multiply_const_vxx_3, 0))
		self.connect((self.gr_fft_filter_xxx_0, 0), (self.gr_add_xx_2_0, 0))
		self.connect((self.gr_fft_filter_xxx_0_0, 0), (self.gr_add_xx_2_0, 1))
		self.connect((self.gr_multiply_xx_1, 0), (self.gr_fft_filter_xxx_0_0, 0))
		self.connect((self.gr_fft_filter_xxx_0_0_0, 0), (self.gr_add_xx_2_0, 2))
		self.connect((self.gr_multiply_xx_1, 0), (self.gr_fft_filter_xxx_0_0_0, 0))
		self.connect((self.blks2_fm_deemph_0, 0), (self.gr_multiply_const_vxx_1_0, 0))
		self.connect((self.blks2_fm_deemph_0, 0), (self.gr_wavfile_sink_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.gr_fft_filter_xxx_1, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.gr_fft_filter_xxx_1_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.gr_fft_filter_xxx_1_0_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_multiply_const_vxx_0_0, 0), (self.blks2_fm_deemph_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.audio_sink_0, 1))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.blks2_fm_deemph_0_0, 0))
		self.connect((self.blks2_fm_deemph_0_0, 0), (self.gr_add_xx_0, 1))
		self.connect((self.band_pass_filter_2, 0), (self.gr_multiply_xx_0_0, 1))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.band_pass_filter_2, 0))
		self.connect((self.blks2_fm_deemph_0, 0), (self.audio_sink_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.band_pass_filter_2_0, 0))
		self.connect((self.gr_multiply_const_vxx_1, 0), (self.band_pass_filter_0_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.gr_wavfile_sink_0, 1))
		self.connect((self.blks2_fm_deemph_0, 0), (self.wxgui_scopesink2_0, 0))
		self.connect((self.gr_add_xx_0, 0), (self.wxgui_scopesink2_0, 1))
		self.connect((self.blks2_wfm_rcv_0, 0), (self.gr_multiply_const_vxx_1, 0))
		self.connect((self.gr_agc_xx_1, 0), (self.blks2_wfm_rcv_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.gr_agc_xx_1, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.input_power, 0))
		self.connect((self.blks2_wfm_rcv_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.low_pass_filter_1, 0))
		self.connect((self.low_pass_filter_1, 0), (self.low_pass_filter_2, 0))
		self.connect((self.low_pass_filter_2, 0), (self.low_pass_filter_3, 0))
		self.connect((self.gr_single_pole_iir_filter_xx_1, 0), (self.dc_level, 0))
		self.connect((self.low_pass_filter_3, 0), (self.gr_single_pole_iir_filter_xx_1, 0))
		self.connect((self.rtl2832_source_0, 0), (self.gr_freq_xlating_fir_filter_xxx_0, 0))
		self.connect((self.gr_freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_0, 0))

	def get_devid(self):
		return self.devid

	def set_devid(self, devid):
		self.devid = devid

	def get_rdsfile(self):
		return self.rdsfile

	def set_rdsfile(self, rdsfile):
		self.rdsfile = rdsfile

	def get_gain(self):
		return self.gain

	def set_gain(self, gain):
		self.gain = gain
		self.set_igain(self.gain)
		self.rtl2832_source_0.set_gain(self.gain)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_ifreq(self.freq)

	def get_xmlport(self):
		return self.xmlport

	def set_xmlport(self, xmlport):
		self.xmlport = xmlport

	def get_arate(self):
		return self.arate

	def set_arate(self, arate):
		self.arate = arate
		self.set_farate(self.arate)

	def get_mute(self):
		return self.mute

	def set_mute(self, mute):
		self.mute = mute
		self.set_sq_thresh(self.mute)

	def get_ftune(self):
		return self.ftune

	def set_ftune(self, ftune):
		self.ftune = ftune
		self.set_fine(self.ftune)

	def get_ant(self):
		return self.ant

	def set_ant(self, ant):
		self.ant = ant

	def get_subdev(self):
		return self.subdev

	def set_subdev(self, subdev):
		self.subdev = subdev

	def get_ahw(self):
		return self.ahw

	def set_ahw(self, ahw):
		self.ahw = ahw

	def get_deemph(self):
		return self.deemph

	def set_deemph(self, deemph):
		self.deemph = deemph
		self.set_dm(self.deemph)

	def get_prenames(self):
		return self.prenames

	def set_prenames(self, prenames):
		self.prenames = prenames

	def get_prefreqs(self):
		return self.prefreqs

	def set_prefreqs(self, prefreqs):
		self.prefreqs = prefreqs
		self.set_preselect(eval(self.prefreqs)[0])

	def get_volume(self):
		return self.volume

	def set_volume(self, volume):
		self.volume = volume
		self.set_vol(self.volume)

	def get_pthresh(self):
		return self.pthresh

	def set_pthresh(self, pthresh):
		self.pthresh = pthresh
		self.set_stpilotdet(True if (self.pilot_level > self.pthresh) else False)
		self.set_st_enabled(1 if (self.stereo == True and self.pilot_level > self.pthresh) else 0)

	def get_preselect(self):
		return self.preselect

	def set_preselect(self, preselect):
		self.preselect = preselect
		self.set_cur_freq(simple_fm_helper.freq_select(self.ifreq,self.preselect))
		self._preselect_chooser.set_value(self.preselect)

	def get_pilot_level(self):
		return self.pilot_level

	def set_pilot_level(self, pilot_level):
		self.pilot_level = pilot_level
		self.set_stpilotdet(True if (self.pilot_level > self.pthresh) else False)
		self.set_st_enabled(1 if (self.stereo == True and self.pilot_level > self.pthresh) else 0)

	def get_ifreq(self):
		return self.ifreq

	def set_ifreq(self, ifreq):
		self.ifreq = ifreq
		self.set_cur_freq(simple_fm_helper.freq_select(self.ifreq,self.preselect))
		self._ifreq_slider.set_value(self.ifreq)
		self._ifreq_text_box.set_value(self.ifreq)

	def get_stpilotdet(self):
		return self.stpilotdet

	def set_stpilotdet(self, stpilotdet):
		self.stpilotdet = stpilotdet
		self.set_stereo_0(self.stpilotdet)

	def get_stereo(self):
		return self.stereo

	def set_stereo(self, stereo):
		self.stereo = stereo
		self.set_st_enabled(1 if (self.stereo == True and self.pilot_level > self.pthresh) else 0)
		self._stereo_check_box.set_value(self.stereo)

	def get_rf_pwr_lvl(self):
		return self.rf_pwr_lvl

	def set_rf_pwr_lvl(self, rf_pwr_lvl):
		self.rf_pwr_lvl = rf_pwr_lvl
		self.set_variable_static_text_0(10.0*math.log(self.rf_pwr_lvl+1.0e-11)/math.log(10))

	def get_cur_freq(self):
		return self.cur_freq

	def set_cur_freq(self, cur_freq):
		self.cur_freq = cur_freq
		self.set_rtext_0(self.cur_freq)
		self.rtl2832_source_0.set_frequency(self.cur_freq+200e3)

	def get_vol(self):
		return self.vol

	def set_vol(self, vol):
		self.vol = vol
		self._vol_slider.set_value(self.vol)
		self._vol_text_box.set_value(self.vol)
		self.gr_multiply_const_vxx_0_0.set_k((self.vol*1.5*10.0, ))
		self.gr_multiply_const_vxx_0.set_k((self.vol*1.5*10.0 if self.st_enabled else 0, ))

	def get_variable_static_text_0(self):
		return self.variable_static_text_0

	def set_variable_static_text_0(self, variable_static_text_0):
		self.variable_static_text_0 = variable_static_text_0
		self._variable_static_text_0_static_text.set_value(self.variable_static_text_0)

	def get_tone_med(self):
		return self.tone_med

	def set_tone_med(self, tone_med):
		self.tone_med = tone_med
		self.gr_fft_filter_xxx_1_0.set_taps((firdes.band_pass(self.tone_med/10.0,self.asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)))
		self._tone_med_slider.set_value(self.tone_med)
		self._tone_med_text_box.set_value(self.tone_med)
		self.gr_fft_filter_xxx_0_0.set_taps((firdes.band_pass(self.tone_med/10.0,self.asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)))

	def get_tone_low(self):
		return self.tone_low

	def set_tone_low(self, tone_low):
		self.tone_low = tone_low
		self.gr_fft_filter_xxx_1.set_taps((firdes.low_pass(self.tone_low/10.0,self.asrate,1.2e3,500,firdes.WIN_HAMMING)))
		self._tone_low_slider.set_value(self.tone_low)
		self._tone_low_text_box.set_value(self.tone_low)
		self.gr_fft_filter_xxx_0.set_taps((firdes.low_pass(self.tone_low/10.0,self.asrate,1.2e3,500,firdes.WIN_HAMMING)))

	def get_tone_high(self):
		return self.tone_high

	def set_tone_high(self, tone_high):
		self.tone_high = tone_high
		self.gr_fft_filter_xxx_1_0_0.set_taps((firdes.band_pass(self.tone_high/10.0,self.asrate,3.5e3,15.0e3,5.0e3,firdes.WIN_HAMMING)))
		self._tone_high_slider.set_value(self.tone_high)
		self._tone_high_text_box.set_value(self.tone_high)
		self.gr_fft_filter_xxx_0_0_0.set_taps((firdes.band_pass(self.tone_high/10.0,self.asrate,3.5e3,13.5e3,3.5e3,firdes.WIN_HAMMING)))

	def get_stereo_0(self):
		return self.stereo_0

	def set_stereo_0(self, stereo_0):
		self.stereo_0 = stereo_0
		self._stereo_0_check_box.set_value(self.stereo_0)

	def get_st_enabled(self):
		return self.st_enabled

	def set_st_enabled(self, st_enabled):
		self.st_enabled = st_enabled
		self.gr_multiply_const_vxx_2.set_k((1.0 if self.st_enabled else 1.414, ))
		self.gr_multiply_const_vxx_3.set_k((3.16e3 if self.st_enabled else 0, ))
		self.gr_multiply_const_vxx_1_0.set_k((0 if self.st_enabled else 1, ))
		self.gr_multiply_const_vxx_0.set_k((self.vol*1.5*10.0 if self.st_enabled else 0, ))

	def get_squelch_probe(self):
		return self.squelch_probe

	def set_squelch_probe(self, squelch_probe):
		self.squelch_probe = squelch_probe
		self.gr_multiply_const_vxx_1.set_k((0 if self.squelch_probe == 0 else 1.0, ))

	def get_sq_thresh(self):
		return self.sq_thresh

	def set_sq_thresh(self, sq_thresh):
		self.sq_thresh = sq_thresh
		self._sq_thresh_slider.set_value(self.sq_thresh)
		self._sq_thresh_text_box.set_value(self.sq_thresh)
		self.input_power.set_threshold(self.sq_thresh)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.input_power.set_alpha(1.0/(self.samp_rate/10))
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

	def get_rtext_0(self):
		return self.rtext_0

	def set_rtext_0(self, rtext_0):
		self.rtext_0 = rtext_0
		self._rtext_0_static_text.set_value(self.rtext_0)

	def get_record(self):
		return self.record

	def set_record(self, record):
		self.record = record
		self.gr_wavfile_sink_0.open("/dev/null" if self.record == False else self.capture_file)
		self._record_check_box.set_value(self.record)

	def get_rdsrate(self):
		return self.rdsrate

	def set_rdsrate(self, rdsrate):
		self.rdsrate = rdsrate

	def get_osmo_taps(self):
		return self.osmo_taps

	def set_osmo_taps(self, osmo_taps):
		self.osmo_taps = osmo_taps
		self.gr_freq_xlating_fir_filter_xxx_0.set_taps((self.osmo_taps))

	def get_mod_reset(self):
		return self.mod_reset

	def set_mod_reset(self, mod_reset):
		self.mod_reset = mod_reset

	def get_igain(self):
		return self.igain

	def set_igain(self, igain):
		self.igain = igain
		self._igain_slider.set_value(self.igain)
		self._igain_text_box.set_value(self.igain)

	def get_fine(self):
		return self.fine

	def set_fine(self, fine):
		self.fine = fine
		self._fine_slider.set_value(self.fine)
		self._fine_text_box.set_value(self.fine)
		self.gr_freq_xlating_fir_filter_xxx_0.set_center_freq(200e3+self.fine+(-12e3*self.discrim_dc))

	def get_farate(self):
		return self.farate

	def set_farate(self, farate):
		self.farate = farate
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.asrate/self.farate)
		self.gr_fractional_interpolator_xx_0_0.set_interp_ratio(self.asrate/self.farate)
		self.wxgui_scopesink2_0.set_sample_rate(self.farate)

	def get_dm(self):
		return self.dm

	def set_dm(self, dm):
		self.dm = dm
		self._dm_chooser.set_value(self.dm)

	def get_discrim_dc(self):
		return self.discrim_dc

	def set_discrim_dc(self, discrim_dc):
		self.discrim_dc = discrim_dc
		self.gr_freq_xlating_fir_filter_xxx_0.set_center_freq(200e3+self.fine+(-12e3*self.discrim_dc))

	def get_capture_file(self):
		return self.capture_file

	def set_capture_file(self, capture_file):
		self.capture_file = capture_file
		self.gr_wavfile_sink_0.open("/dev/null" if self.record == False else self.capture_file)
		self._capture_file_text_box.set_value(self.capture_file)

	def get_asrate(self):
		return self.asrate

	def set_asrate(self, asrate):
		self.asrate = asrate
		self.gr_single_pole_iir_filter_xx_0.set_taps(1.0/(self.asrate/3))
		self.gr_keep_one_in_n_0.set_n(int(self.asrate/3))
		self.gr_fractional_interpolator_xx_0.set_interp_ratio(self.asrate/self.farate)
		self.gr_fft_filter_xxx_1.set_taps((firdes.low_pass(self.tone_low/10.0,self.asrate,1.2e3,500,firdes.WIN_HAMMING)))
		self.gr_fft_filter_xxx_1_0.set_taps((firdes.band_pass(self.tone_med/10.0,self.asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)))
		self.gr_fft_filter_xxx_1_0_0.set_taps((firdes.band_pass(self.tone_high/10.0,self.asrate,3.5e3,15.0e3,5.0e3,firdes.WIN_HAMMING)))
		self.band_pass_filter_2_0.set_taps(firdes.band_pass(20, self.asrate, 17.5e3, 17.9e3, 250, firdes.WIN_HAMMING, 6.76))
		self.gr_fractional_interpolator_xx_0_0.set_interp_ratio(self.asrate/self.farate)
		self.band_pass_filter_2.set_taps(firdes.band_pass(10, self.asrate, 18.8e3, 19.2e3, 350, firdes.WIN_HAMMING, 6.76))
		self.wxgui_fftsink2_0.set_sample_rate(self.asrate)
		self.gr_fft_filter_xxx_0.set_taps((firdes.low_pass(self.tone_low/10.0,self.asrate,1.2e3,500,firdes.WIN_HAMMING)))
		self.gr_fft_filter_xxx_0_0_0.set_taps((firdes.band_pass(self.tone_high/10.0,self.asrate,3.5e3,13.5e3,3.5e3,firdes.WIN_HAMMING)))
		self.low_pass_filter_0.set_taps(firdes.low_pass(3, self.asrate, 10e3, 2e3, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_1.set_taps(firdes.low_pass(3, self.asrate/5, 1e3, 200, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_2.set_taps(firdes.low_pass(3, self.asrate/50, 100, 30, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_3.set_taps(firdes.low_pass(3, self.asrate/500, 10, 3, firdes.WIN_HAMMING, 6.76))
		self.gr_single_pole_iir_filter_xx_1.set_taps(2.5/(self.asrate/500))
		self.gr_fft_filter_xxx_0_0.set_taps((firdes.band_pass(self.tone_med/10.0,self.asrate,1.0e3,4.0e3,2.0e3,firdes.WIN_HAMMING)))
		self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.asrate, 38e3-(15e3), 38e3+(15e3), 4.0e3, firdes.WIN_HAMMING, 6.76))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	parser.add_option("", "--devid", dest="devid", type="string", default="type=b100",
		help="Set Device ID [default=%default]")
	parser.add_option("", "--rdsfile", dest="rdsfile", type="string", default="rds_fifo",
		help="Set RDS Output FIFO name [default=%default]")
	parser.add_option("", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(35.0),
		help="Set RF Gain [default=%default]")
	parser.add_option("", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(101.1e6),
		help="Set RF Center Frequency [default=%default]")
	parser.add_option("", "--xmlport", dest="xmlport", type="intx", default=13777,
		help="Set XML RPC Port [default=%default]")
	parser.add_option("", "--arate", dest="arate", type="intx", default=int(48e3),
		help="Set Audio Rate [default=%default]")
	parser.add_option("", "--mute", dest="mute", type="eng_float", default=eng_notation.num_to_str(-15.0),
		help="Set Mute Level [default=%default]")
	parser.add_option("", "--ftune", dest="ftune", type="eng_float", default=eng_notation.num_to_str(0),
		help="Set Fine Tuning [default=%default]")
	parser.add_option("", "--ant", dest="ant", type="string", default="J1",
		help="Set Antenna Spec [default=%default]")
	parser.add_option("", "--subdev", dest="subdev", type="string", default="A:0",
		help="Set Subdev spec [default=%default]")
	parser.add_option("", "--ahw", dest="ahw", type="string", default="pulse",
		help="Set Audio Hardware Spec [default=%default]")
	parser.add_option("", "--deemph", dest="deemph", type="eng_float", default=eng_notation.num_to_str(75.0e-6),
		help="Set FM Deemphasis [default=%default]")
	parser.add_option("", "--prenames", dest="prenames", type="string", default='["UWRF","89.3","950","WEVR"]',
		help="Set Preset Frequencies [default=%default]")
	parser.add_option("", "--prefreqs", dest="prefreqs", type="string", default="[88.715e6,89.3e6,950.735e6,106.317e6]",
		help="Set Preset Frequencies [default=%default]")
	parser.add_option("", "--volume", dest="volume", type="eng_float", default=eng_notation.num_to_str(1.0),
		help="Set Volume Level [default=%default]")
	(options, args) = parser.parse_args()
	tb = simple_fm_rcv(devid=options.devid, rdsfile=options.rdsfile, gain=options.gain, freq=options.freq, xmlport=options.xmlport, arate=options.arate, mute=options.mute, ftune=options.ftune, ant=options.ant, subdev=options.subdev, ahw=options.ahw, deemph=options.deemph, prenames=options.prenames, prefreqs=options.prefreqs, volume=options.volume)
	tb.Run(True)

