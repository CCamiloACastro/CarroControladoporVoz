import wave
import pyaudio
#Iniciamos Pyaudio

p = pyaudio.PyAudio()
#Archivo a reproducir

# Abrir (archivo, modo en que queremos abrirlo)
a = 10
while a !=1:
    
    archivoString = 'D:\\Datos\Documentos\\1. Programas y Proyectos\\Python 3.7\\DSP_1\\Carro\\audios\\'
    comandoString = 'adelante'
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
    #Se reproduce el stream
    while datos != b'':
        streamReproducir.write(datos)
        datos = rf.readframes(1024)
    
   
#cerrar
streamReproducir.stop_stream()
streamReproducir.close()
p.terminate()
rf.close()