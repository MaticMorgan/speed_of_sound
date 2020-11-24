from pydub import AudioSegment
from pydub.utils import make_chunks
import scipy.io.wavfile as wavfile
import scipy
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

myaudio = AudioSegment.from_file("Recording7.wav" , "wav") 
chunk_length_ms = 1000 # dolzina kosa v milisekundah
chunks = make_chunks(myaudio, chunk_length_ms) # naredu avdio kose, ki so dolgi 1 sekundo

frekvence = range(400, 3000) # frekvence so zaporedje od 400 Hz do 3000 Hz
amplitude = [] # prazno zaporedje za amplitude

for i, chunk in enumerate(chunks): # naredi audio kose dolge 1 sekundo in jih shrani
    chunk_name = "chunk{0}.wav".format(i) #poimenuj avdio kose in jim doloci format, prav tako so avdio kosi to kar iteriramo
    # chunk.export(chunk_name, format="wav") # izvozi narejene avdio kose
    
    s_rate, signal = wavfile.read(chunk_name)  # naj bo signal moj zvocni zapis (s_rate nam vrne sample rate, ki ga tu ne uporabimo)
    FFT = abs(scipy.fft.fft(signal)) # vrne absolutno vrednost fourierjeve transformacije (oz. magnitudo, ker je v kompleksnem)
    ampl = np.mean(FFT) # vrne povprecno vrednost od FTT
    amplitude.append(ampl) # zaporedju amplitud na konec doda povprecno vrednost FTT

del amplitude[:5] # odstranimo prvih 5 elementov zaporedja (=prvih 5 sekund ni bilo zvoka, ker sem ga prizigal)
del amplitude[-204:] # odstraino zadnje 204 elemente zaporedja (=odstranimo zadnje 204 sekund posnetka, ko je snemal v prazno)

resonancni_indeksi, _ = find_peaks(amplitude, prominence = 40000) # zaporedje indeksov pri katerih se pojavi maksimum
resonance = [x + 400 for x in resonancni_indeksi] # zaporedje z dejanskimi frekvencami, ki so indeksi povecani za zacetno frekvenco 400 Hz

k = ( frekvence[-1] - frekvence[0]) / (3*len(resonance)) # izracunamo naklon premice frekvenca v odv od (stevilo vozlov)
c = 4*k*(0.72+0.61*0.0375) # ヽ༼ຈل͜ຈ༽ﾉ izracunamo hitrost zvoka v zraku ヽ༼ຈل͜ຈ༽ﾉ

 # ta oddelek narise graf frekvenc v odvisnosti od stevila vozlov
a = frekvence
b = range(1,13)
new_a = np.linspace(a[0], a[-1])
new_b = np.linspace(b[0], b[-1])
plt.xlabel('število vozlov')
plt.ylabel('frekvenca [Hz]')
plt.plot(new_b, new_a)
plt.savefig('linearna.png') # izvozi graf
plt.show()

 # ta oddelek narise graf, fita polinom in ga narise
x = frekvence
y = amplitude
coefficients = np.polyfit(x, y, 50) # fitaj polinom stopnje 50. to je veliko racunanja, zato morda sam izbere nizjo stopnjo, ampak vseeno sprocesira. pri npr. stopnji 100 je to neizvedljivo
poly = np.poly1d(coefficients)
new_x = np.linspace(x[0], x[-1])
new_y=poly(new_x)
plt.xlabel('frekvence [Hz]')
plt.ylabel('amplitude')
plt.plot(x, y, "o", new_x, new_y)
plt.xlim([x[0]-1, x[-1] + 1 ])
plt.savefig('polinom.png') # izvozi graf

print("hitrost zvoka v zraku je", c, "m/s") # izpis rezultata