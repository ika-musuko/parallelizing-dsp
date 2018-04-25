Parallelizing Digital Signal Processing
-----------

CS 159 research into parallelizing DSP. various experimental scripts will be here demonstrating the ideas.

The wave_analyzer folder contains the py files for the waveform analyzer. You will need matplotlib, pyaudio, and numpy to run the scripts.

A demo of the wave analyzer can be found here: https://www.youtube.com/watch?v=DKFMqR_ypuQ

PAPER ABSTRACT
-----------
Digital Signal Processing is an ubiquitous field that can be boiled down to taking a signal, such as an audio wave, an image, or motion, applying some operation to it, and outputting the result. In software, signals are usually represented in vector-like data structures, and the operations on signals are done across the entire vector. Additionally, sometimes signal data is received in real time and the current data must be analyzed at once without slowing the system down. This paper will discuss an approach to reading and processing realtime signal data in a timely manner by means of parallelism.
