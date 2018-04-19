'''
makes heavy use of https://github.com/markjay4k/Audio-Spectrum-Analyzer-in-Python/blob/master/audio_spectrum.py
'''

import pyaudio
import wave
import sys
import numpy as np

class WaveAnalyzer:
    def __init__(self, wave_file: str, fft_func):
        
        self.CHUNK = 1024
        self.wave_filename = wave_file
        self.load()


    def load(self):
        self.wf = wave.open(self.wave_filename, 'rb')

        # instantiate PyAudio (1)
        self.pa = pyaudio.PyAudio()

        # open stream (2)
        self.stream = self.pa.open(
                  format=self.pa.get_format_from_width(self.wf.getsampwidth())
                , channels=self.wf.getnchannels()
                , rate=self.wf.getframerate()
                , output=True
                )

        # read data
        self.data = self.wf.readframes(self.CHUNK)


    def play(self, analyze=True):
        # play stream (3)
        while len(self.data) > 0:
            print(len(self.data))
            self.stream.write(self.data)
            if analyze:
                self.analyze()
            self.data = self.wf.readframes(self.CHUNK)


    def analyze(self):
        pass


    def cleanup(self):
        # stop stream (4)
        self.stream.stop_stream()
        self.stream.close()

        # close PyAudio (5)
        self.pa.terminate()

if __name__ == "__main__":
    wa = WaveAnalyzer(wave_file=sys.argv[1], fft_func=np.fft.fft)
    while True:
        wa.play()
        wa.cleanup()
        wa.load()

