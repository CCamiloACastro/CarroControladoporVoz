import wave
import pyaudio  

#inicializacion de variables
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DURACION = 2
archivo = 'D:\\Datos\Documentos\\1. Programas y Proyectos\\Python 3.7\\DSP_1\\Carro\\audios\\adelante10.wav'


#Iniciamos PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,channels=CHANNELS,rate =RATE,input=True,frames_per_buffer=CHUNK)

# Se inicia la grabación   
print ("Grabando...")
frames = []
samples = (RATE / CHUNK) * DURACION
for i in range(0, int(samples)):
        data = stream.read(CHUNK)
        frames.append(data)
print ("Fin de la grabacion")

#fin de grabacion      
stream.stop_stream()
stream.close()
p.terminate()
#guardar archivo
wf = wave.open(archivo, 'wb')
wf.setnchannels(CHANNELS)
wf.setframerate(RATE)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.writeframes(b''.join(frames))
wf.close()

