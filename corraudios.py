import pyaudio
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pylab as plt

global t, rate, data
#abrir documento 
rate, data = wavfile.read("primer.wav")

#conversion a tiempo
t = np.linspace(0, (len(data) / rate), num = len(data))
#graficar
plt.figure(1)
plt.plot(t, data)
plt.show()
data2 = 0.5*data;
correlacion = np.corrcoef(data, data2 )
print(correlacion)