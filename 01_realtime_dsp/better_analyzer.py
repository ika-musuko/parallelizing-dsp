'''
base visualizer from https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/audio_spectrum.py

but i fixed the math and made the visualizer real time
'''

from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import gridspec

import pyaudio
import time
import wave
import sys
import numpy as np
import struct
import multiprocessing as mp

FPS = 30


class WaveAnalyzer():
    def __init__(self, wave_file: str, fft_func): 
        
        self.data_queue = mp.Queue()
        
        # status
        self.playing = False

        # settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100


        # fft function to be used
        self.fft = fft_func
        self.wave_filename = wave_file
        self.load()
        


    def start_plotter(self):
        '''
            initialize the plotter
        '''
        # x variables for plotting
        x = np.arange(0, self.CHUNK * 2, 2)
        xf = np.linspace(0, self.RATE, self.CHUNK)

        # create matplotlib figure and axes
        self.fig = plt.figure(figsize=(8, 7))
        gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1, 3])
        ax1 = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])

        # create a line object with random data
        self.line, = ax1.plot(x, np.random.rand(self.CHUNK), 'g', lw=2, animated=True)

        # logarithmically scale spectrum axis
        self.line_fft, = ax2.plot(xf, np.random.rand(self.CHUNK), '-', lw=2, animated=True)
        ax2.set_xscale("symlog")

        # format waveform axes
        ax1.set_xlabel('samples')
        ax1.set_ylabel('volume')
        ax1.set_ylim(-2**15, 2**15)
        ax1.set_xlim(0, self.CHUNK)
        plt.setp(
            ax1, yticks=[-2**15, 0 , 2**15],
            xticks=[0, self.CHUNK],
        )

        # format spectrum axes
        ax2.set_xlim(40, 2 * self.CHUNK)
        ax2.set_ylim(0, 2**23)
        ax2.set_xlabel('frequency (Hz)')
        ax2.set_ylabel('energy')
        ax2.set_xticks([j for i in [[5*10**i, 1*10**(i+1), 2*10**(i+1)] for i in range(1, 4)] for j in i]) # 50, 100, 200, 500, 1000, 2000....
        for axis in [ax2.xaxis, ax2.yaxis]:
            axis.set_major_formatter(ScalarFormatter())

        def plot(frame=None):
            if self.data_queue.empty():
                data = bytes(2048)
            else:
                data = self.data_queue.get()

            data_np = np.frombuffer(data, dtype='Int16') 
            self.line.set_ydata(data_np)

            # compute fft and update line
            yf = self.fft(data_np)
            self.line_fft.set_ydata(np.abs(yf[0:self.CHUNK]))
            return self.line, self.line_fft

        ani = animation.FuncAnimation(
                self.fig, plot, None,
                init_func=plot, 
                interval=1000.0 / FPS, blit=True
                )
        
        plt.show()

    
    def load(self):
        print("load")
        self.wf = wave.open(self.wave_filename, 'rb')

        # instantiate PyAudio (1)
        self.pa = pyaudio.PyAudio()

        # callback function (non blocking)
        def _pa_callback(in_data, frame_count, time_info, status):
            #print("write wave data to soundcard")
            self.data = self.wf.readframes(frame_count)
            callback_flag = pyaudio.paContinue if self.playing else pyaudio.paComplete
            signal = (self.data, callback_flag)
            self.data_queue.put(self.data)
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
        # blocking version
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


# processes
def plot_func(wa: WaveAnalyzer):
    wa.start_plotter()

if __name__ == "__main__":
    
    mp.freeze_support() # windows...
    wa = WaveAnalyzer(wave_file=sys.argv[1], fft_func=np.fft.fft)
    plot_proc = mp.Process(target=plot_func, args=(wa, ))
    plot_proc.start()
    time.sleep(2)
    wa.play_loop()
