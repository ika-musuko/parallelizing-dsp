import math

def make_sinewave(
            frequency: float
          , amplitude: int=20000
          , seconds: float=2.0
          , framerate: int=192000
          ) -> list:
    '''
    generate a sinewave signal into a list of floats
    '''
    nframes = int(framerate*seconds)
    waveform = [(amplitude/2) * math.sin(2*math.pi*frequency*(float(i)/framerate)) for i in range(nframes)]
    return waveform

def basic_dft(signal: list, frequency: float) -> float:
    '''
        basic discrete fourier transform
        params
            signal: a list containing the values in the signal
            frequency: which frequency should be analyzed
        return value
            the energy of the signal at that frequency in Hz
    '''
    def spinner(n: int, total_samples: int) -> float:
        return math.e**(-1j*2*math.pi*frequency*(n/total_samples))
    return 1/len(signal) * sum(sample*spinner(n, len(signal)) for n, sample in enumerate(signal))
    
