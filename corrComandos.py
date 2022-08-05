import wave
import pyaudio
import numpy as  np
import matplotlib.pylab as plt
import scipy.io.wavfile as wavfile
#Iniciamos Pyaudio

p = pyaudio.PyAudio()
#Archivo a reproducir

# Abrir (archivo, modo en que queremos abrirlo)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DURACION = 2
archivoComando = 'D:\\Datos\Documentos\\1. Programas y Proyectos\\Python 3.7\\DSP_1\\Carro\\audios\\comando.wav'
#Iniciamos PyAudio
stream = p.open(format=FORMAT,channels=CHANNELS,rate =RATE,input=True,frames_per_buffer=CHUNK)

# Se inicia la grabación   
print ("Grabando Comando")
frames = []
samples = (RATE / CHUNK) * DURACION
for i in range(0, int(samples)):
        dataComando = stream.read(CHUNK)
        frames.append(dataComando)
print ("Fin de la grabación Comando")

#fin de grabacion      
stream.stop_stream()
stream.close()
#p.terminate()
#guardar archivo
wf = wave.open(archivoComando, 'wb')
wf.setnchannels(CHANNELS)
wf.setframerate(RATE)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.writeframes(b''.join(frames))
wf.close()
print("reproducirComando")
rfComando = wave.open(archivoComando, 'rb')

#reproducir de a partes de 1024
prof = rfComando.getsampwidth()
channels = rfComando.getnchannels()
rateComando = rfComando.getframerate()
audioN = pyaudio.PyAudio()
streamReproducir  = audioN.open(format = audioN.get_format_from_width(prof), channels = channels, rate = rateComando, output = True)
#Leemos la información
datosComando = rfComando.readframes(1024)

rateComando, comando = wavfile.read(archivoComando)
t = np.linspace(0, (len(comando) / rateComando), num = len(comando))
#graficar
plt.figure(1)
plt.plot(t, comando)
plt.show() 

#Se reproduce el stream
while datosComando != b'':
    streamReproducir.write(datosComando)
    datosComando = rfComando.readframes(1024)

print("reproduciraudios")
a = 4
while a !=0:
    
    archivoString = 'D:\\Datos\Documentos\\1. Programas y Proyectos\\Python 3.7\\DSP_1\\Carro\\audios\\'
    comandoString = 'derecha'
    numString = str(a)
    waveString = '.wav'
    archivo = archivoString + comandoString + numString + waveString
    print(archivo)
    rf = wave.open(archivo, 'rb')
    #Escoger otro audio
    a = a - 1 

    #reproducir de a partes de 1024
    prof = rf.getsampwidth()
    channels = rf.getnchannels()
    rate = rf.getframerate()
    audioN = pyaudio.PyAudio()
    streamReproducir  = audioN.open(format = audioN.get_format_from_width(prof), channels = channels, rate = rate, output = True)
    #Leemos la información
    datos = rf.readframes(1024)
    #Correlación

    #abrir documento 
    rate2, data = wavfile.read(archivo)
    rate3, comando = wavfile.read(archivoComando)
    correlacion = np.corrcoef(comando, data)
    print(correlacion)

    """ t = np.linspace(0, (len(data) / rate2), num = len(data))
    #graficar
    plt.figure(1)
    plt.plot(t, data)
    plt.show() """

    #Se reproduce el stream
    while datos != b'':
        streamReproducir.write(datos)
        datos = rf.readframes(1024)
    
   
#cerrar
streamReproducir.stop_stream()
streamReproducir.close()
p.terminate()
rf.close()