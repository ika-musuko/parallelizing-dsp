import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from sys import argv
import numpy as np

DTYPES = {
      "float32" : 0
      , "int32" : 32
      , "int16" : 16
      , "uint8" : 8
}

def plotter(fft_func, wavename: str):
    ### read the wav data
    sample_rate, data = wavfile.read(wavename)
    bit = DTYPES[str(data.dtype)] # get the data type
    data = data / (2. ** bit) # normalize the data
    data_len = data.shape[0] # get the total data points and number of channels
    
    ### plot the time domain
    time_axis = np.arange(0, data_len, 1) / sample_rate  # scale time pointsto seconds
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, data, color='b')
    plt.xlabel("Time (sec)")
    plt.ylabel("Amplitude")

    ### plot the frequency domain (fourier transform)
    N = data_len
    FFT = fft_func(data) # calculate the fft with the specified function
    num_unique_points = int(np.ceil((N+1)/2.0))
    FFT = np.abs(FFT[0:num_unique_points]) # truncate the FFT to the region of the data points
    FFT = (FFT/float(N)) ** 2 # normalize the FFT

    # nyquist fix, see https://web.archive.org/web/20120615002031/http://www.mathworks.com/support/tech-notes/1700/1702.html
    if N % 2 != 0: # odd amount of FFT points
        FFT[1:len(FFT)] = FFT[1:len(FFT)] * 2
    else: # even amount of FFT points 
        FFT[1:len(FFT) - 1] = FFT[1:len(FFT) - 1] * 2

    plt.subplot(2, 1, 2)
    frequency_axis = np.arange(0, num_unique_points, 1.0) * (sample_rate / N)
    plt.plot(frequency_axis, 10*np.log10(FFT), color='r')
    
    plt.xlabel("Frequency (Hz)")
    plt.semilogx(base=10, subsx=[440])
    plt.xlim(xmin=1, xmax=35000)

    plt.ylabel("Energy (dB)")
    plt.ylim(ymin=-60, ymax=0)
    
    plt.show()


if __name__ == "__main__":
    plotter(fft_func=np.fft.fft, wavename=argv[1])
