'''
makes heavy use of https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/audio_spectrum.py
'''

import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyaudio
import time
import wave
import sys
import numpy as np
import struct
import multiprocessing as mp


class SoundcardAnalyzer():
    '''
    epic hack where i record the output from the computer's audio device instead of from the wave file LOL
    '''
    def __init__(self, fft_func):
        # fft function to be used
        self.fft = fft_func

    def init_plotter(self):
        
        # x variables for plotting
        x = np.arange(0, 2 * self.CHUNK, 2)
        xf = np.linspace(0, self.RATE, self.CHUNK)

        # create matplotlib figure and axes
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        #self.fig.canvas.mpl_connect('button_press_event', self.onClick)

        # create a line object with random data
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), '-', lw=2)

        # create semilogx line for spectrum
        self.line_fft, = ax2.semilogx(
            xf, np.random.rand(self.CHUNK), '-', lw=2)

        # format waveform axes
        ax1.set_title('AUDIO WAVEFORM')
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')
        ax1.set_ylim(0, 255)
        ax1.set_xlim(0, 2 * self.CHUNK)
        plt.setp(
            ax1, yticks=[0, 128, 255],
            xticks=[0, self.CHUNK, 2 * self.CHUNK],
        )
        plt.setp(ax2, yticks=[0, 1],)

        # format spectrum axes
        ax2.set_xlim(20, self.RATE / 2)

        # show axes
        #thismanager = plt.get_current_fig_manager()
        #thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)



    def plot(self):
        data_int = struct.unpack(str(2 * self.CHUNK) + 'B', self.data)
        data_np = np.array(data_int, dtype='b')[::2] + 128

        self.line.set_ydata(data_np)

        # compute FFT and update line
        yf = self.fft(data_int)
        self.line_fft.set_ydata(
            np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK))

        # update figure canvas
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class WavePlayer():
    def __init__(self, wave_file: str):
       
        # status
        self.playing = False

        # settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        
        # load wave
        self.wave_filename = wave_file
        self.load()

    def load(self):
        print("load")
        self.wf = wave.open(self.wave_filename, 'rb')

        # instantiate PyAudio (1)
        self.pa = pyaudio.PyAudio()

        # callback function (non blocking)
        def _pa_callback(in_data, frame_count, time_info, status):
            self.data = self.wf.readframes(frame_count)
            callback_flag = pyaudio.paContinue if self.playing else pyaudio.paComplete
            signal = (self.data, callback_flag)
            #print(signal)
            return signal
        
        # open stream (2)
        self.stream = self.pa.open(
                  format=self.pa.get_format_from_width(self.wf.getsampwidth())
                , channels=self.wf.getnchannels()
                , rate=self.wf.getframerate()
                , output=True
                , stream_callback = _pa_callback
                )
    
        self.data = self.wf.readframes(self.CHUNK)

    def play(self):
        # play stream (3)
        print("play")
        self._start_stream()
        while self.stream.is_active():
            time.sleep(0.1)

        '''
        while len(self.data) > 0:
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.CHUNK)
        '''

    def cleanup(self):
        print("cleanup")
        # stop stream (4)
        self._stop_stream()
        self.stream.close()

        # close PyAudio (5)
        self.pa.terminate()

    def stop(self):
        self._stop_stream()
    
    def _start_stream(self):
        self.playing = True
        self.stream.start_stream()

    def _stop_stream(self):
        self.playing = False
        self.stream.stop_stream()

    def play_loop(self):
        while True:
            self.play()
            self.stop()
            self.load()


if __name__ == "__main__":
    def play_loop(): 
        wp = WavePlayer(wave_file=sys.argv[1])
        wp.play_loop()

    def plot_loop():
        pass
    
    play_proc = mp.Process(target=play_loop)
    #plot_proc = mp.Process(target=plot_loop)

    play_proc.start()
    #plot_proc.start()
