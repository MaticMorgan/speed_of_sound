from pydub import AudioSegment
from pydub.utils import make_chunks
import scipy.io.wavfile as wavfile
import scipy
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

myaudio = AudioSegment.from_file("Recording7.wav" , "wav") 
chunk_length_ms = 1000
chunks = make_chunks(myaudio, chunk_length_ms)

frekvence = range(400, 3000)
amplitude = []

for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    # chunk.export(chunk_name, format="wav")
    
    s_rate, signal = wavfile.read(chunk_name)
    FFT = abs(scipy.fft.fft(signal)) # returns the absolte value of the FFT
    ampl = np.mean(FFT) # average FFT value
    amplitude.append(ampl)

del amplitude[:5] # remove the first 5 elements becauce there was silence
del amplitude[-204:] # remove the last 204 elements because there was silence

resonancni_indeksi, _ = find_peaks(amplitude, prominence = 40000) # list of indices of the maximums
resonance = [x + 400 for x in resonancni_indeksi] # last of actual frequencies

k = ( frekvence[-1] - frekvence[0]) / (3*len(resonance)) # icalculate the slope of the linear functions showing frequency with respect to the number of knots
c = 4*k*(0.72+0.61*0.0375) # calculte the speed of sound

 # draw the graphs
a = frekvence
b = range(1,13)
new_a = np.linspace(a[0], a[-1])
new_b = np.linspace(b[0], b[-1])
plt.xlabel('number of knots')
plt.ylabel('frequency [Hz]')
plt.plot(new_b, new_a)
plt.savefig('linear.png')
plt.show()

 # draw agraph and fit a polinome
x = frekvence
y = amplitude
coefficients = np.polyfit(x, y, 50) # fit a polinome
poly = np.poly1d(coefficients)
new_x = np.linspace(x[0], x[-1])
new_y=poly(new_x)
plt.xlabel('frequency [Hz]')
plt.ylabel('amplitudes')
plt.plot(x, y, "o", new_x, new_y)
plt.xlim([x[0]-1, x[-1] + 1 ])
plt.savefig('polinom.png')

print("speed of sound in air is: ", c, "m/s")
