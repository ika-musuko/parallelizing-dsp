from itertools import cycle, zip_longest, islice
import math
import wave
import struct
import multiprocessing as mp

# multiprocessing settings
TOTAL_PROCESSES = 12

# note settings
LOW_OCTAVE, HIGH_OCTAVE = 0, 10
FIRST_NOTE = LOW_OCTAVE*12
NOTE_LETTERS = ('c-', 'c#', 'd-', 'd#', 'e-', 'f-', 'f#', 'g-', 'g#', 'a-', 'a#', 'b-')
NOTES = ['%s%s' % (note, octave) for octave in range(LOW_OCTAVE, HIGH_OCTAVE+1) for note in NOTE_LETTERS]
C0 = 16.3515978312874667365624595206543835278 # frequency of C0
RATIO = 2**(1/12)
SECONDS = 3

# wave settings
NCHANNELS = 1
SAMPWIDTH = 2
FRAMERATE = 44100
COMPTYPE = "NONE"
COMPNAME = "not compressed"

def distributor(iterable, groups):
    "distributor('ABCDEFGH', 3) -> ADG BEH CF"
    "raymond hettinger-sensei pls notice me"
    return [[e for e in islice(iterable, i, None, groups)] for i in range(groups)]     

def make_sinewave(
            frequency: float
          , amplitude: int=20000
          , seconds: float=2.0
          , framerate: int=192000
          ) -> list:
    '''
    generate a sinewave signal into a list of floats
    '''
    nframes = int(FRAMERATE*seconds)
    waveform = [(amplitude/2) * math.sin(2*math.pi*frequency*(float(i)/framerate)) for i in range(nframes)]
    return waveform
              
    
def main():
    note_map = []
    for f, note in enumerate(NOTES):
        freq = C0 * RATIO ** (f+FIRST_NOTE)
        note_map.append((freq, note))
    pool = mp.Pool(processes=TOTAL_PROCESSES)
    pool.map(render_noteset, distributor(note_map, TOTAL_PROCESSES))
    
if __name__ == "__main__":
    mp.freeze_support()
    main()
 
