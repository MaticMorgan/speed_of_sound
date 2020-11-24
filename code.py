from pydub import AudioSegment
from pydub.utils import make_chunks
import scipy.io.wavfile as wavfile
import scipy
from scipy.signal import find_peaks
#import scipy.fftpack as fftpk
import numpy as np
import matplotlib.pyplot as plt
# import itertools
# from itertools import tee, islice, chain, izip

myaudio = AudioSegment.from_file("Recording2.wav" , "wav") 
chunk_length_ms = 1000 # dolzina kosa v milisekundah
chunks = make_chunks(myaudio, chunk_length_ms) 

frekvence = []
amplitude = []
maks_amp = []

for i, chunk in enumerate(chunks): # naredi audio kose dolge 1 sekundo in jih shrani
    chunk_name = "chunk{0}.wav".format(i)
    chunk.export(chunk_name, format="wav")
    
    s_rate, signal = wavfile.read(chunk_name)  # naj bo signal moj zvocni zapis
    FFT = abs(scipy.fft.fft(signal)) # vrne absolutno vrednost fourierjeve transformacije (oz. magnitudo, ker je v kompleksnem)
#   freqs = fftpk.fftfreq(len(FFT), 1.0 / s_rate) # vrne korespondencne neodvisne spremenljivke za FFT prilagojene na s_rate
    
    maksimum = np.argmax(FFT) # ta funkcija najde maksimum FFT(freqs)
    if maksimum >= 1000 :
         frekvence.append(maksimum) # mnozica frekvenc, ki korespondirajo enosekundnim intervalom
         average = np.average(FFT) # ta funkcija najde povprecje amplitud FFT
         amplitude.append(average) #mnozica vseh amplitud ki korespondirajo posameznemu enosekundnemu intervalu

# peaks, properties  = find_peaks(myaudio, prominence=1000)
# print(peaks)

# dobre_amplitude = scipy.signal.find_peaks(amplitude, prominence = 1000)
# print(dobre_amplitude)