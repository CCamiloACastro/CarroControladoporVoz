from tkinter import *
from tkinter import Button
from tkinter import Entry,StringVar
from tkinter import filedialog
from tkinter import Label
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
from scipy import signal
from scipy.fftpack import fft
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pylab as plt
import pyaudio
import scipy.io.wavfile as wavfile
import sys
import wave


###############################################################################
def IMPORTAR():
    #inicializacion de variables
    global a
    a = 0
    import os
    from os import path

    #abrimos carpeta
    file_path = filedialog.askopenfilename()
    print(file_path)
    Fs, dato = wavfile.read(file_path)
    print("Frecuencia de muestreo" , Fs)
    scaled = np.int16(dato)
    #Remover Archivos
    if path.exists('s_filtrada.wav'):
        os.remove('s_filtrada.wav')
    if path.exists('primer.wav'):
        os.remove('primer.wav')
    if path.exists('segundo.wav'):
        os.remove('segundo.wav')
    if path.exists('Tercer.wav'):
        os.remove('Tercer.wav')
    #abrir en archivo
    write(("primer.wav"), Fs, scaled)

    Bajo1.set(1)
    Bajo2.set(1)
    Medio1.set(1)
    Medio2.set(1)
    Alto1.set(1)
    Alto2.set(1)
    Volumen.set(1)

###############################################################################
def GUARDAR():
    #inicializacion de variables
    global Fs, sf
    #guardar enarchivo
    filename = asksaveasfilename(initialdir = "/", title = "Save as",
                                 filetypes = (("audio file", ".wav"), ("all files", ".*")),
                                 defaultextension = ".wav")
    print(filename)
    scaled = np.int16(sf)
    write(filename, Fs, scaled)
    
    
    
###############################################################################

def FILTRO():
    #inicializacion de variables
    global b1, b2, m1, m2, a1, a2, sf, Fs, vol
    #filtros
    bajo1 = float(Bajo1.get())
    print('Bajo1', bajo1)
    bajo2 = float(Bajo2.get())
    print('Bajo2', bajo2)
    medio1 = float(Medio1.get())
    print('Medio1', medio1)
    medio2 = float(Medio2.get())
    print('Medio2', medio2)
    alto1 = float(Alto1.get())
    print('Alto1', alto1)
    alto2 = float(Alto2.get())
    print('Alto2', alto2)
    vol = float(Volumen.get())
    print('Volumen', vol)
    #abrir archivo
    Fs, y = wavfile.read("primer.wav")
    N = len(y)
    #inicio de filtro
    T = 1.0 / Fs
    x = np.linspace(0.0, N * T, N)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N / 2))
    #Filtro
    nyq = Fs * 0.5
    
    #primer filtro bajo1
    cutoff = 60
    #print('Frecuencia de corte', cutoff)
    
    stopfreq = float(cutoff)
    cornerfreq = 0.4 * stopfreq
    
    ws = cornerfreq / nyq
    wp = stopfreq / nyq
    N1, wn = signal.buttord(wp, ws, 3, 40)
    b, a = signal.butter(N1, wn, btype='low')
    
    b1 = signal.lfilter(b, a, y) * bajo1
    
    #filtro 2 bajo 2
    lowcut = 60
    highcut = 250
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    b2 = signal.lfilter(b, a, y) * bajo2   
    
    #filtro 3 medio 1
    lowcut = 250
    highcut = 2000
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    m1 = signal.lfilter(b, a, y) * medio1
    
    #filtro 4 medio 2
    lowcut = 2000
    highcut = 4000
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype = 'bandpass')
    
    m2 = signal.lfilter(b, a, y) * medio2
    
    #filtro 5 altos 1
    lowcut = 4000
    highcut = 6000
    order = 4
    
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order,[ low,high ], btype = 'bandpass')
    
    a1 = signal.lfilter(b, a, y) * alto1
    
    #filtro 6 altos 2
    cutoff= 6000
    stopfreq = float(cutoff)
    cornerfreq = 0.4 * stopfreq

    ws = cornerfreq/nyq
    wp = stopfreq/nyq
    
    N1, wn =signal.buttord(wp, ws, 3, 40)
    b, a = signal.butter(N1, wn, btype = 'high')
    
    a2 = signal.lfilter(b, a, y) * alto2
    
    #suma de todos los filtros
    sf = (b1 + b2 + m1 + m2 + a1 + a2)
    #graficar
    #N = len(sf)
    #yf = fft(sf)
    #xf = np.linspace(0.0, (1.0 / (2.0 * T)),int(N / 2))
    
    #plt.figure(2)
    #plt.plot(xf, 2.0 / N * np.abs(yf[0:int(N / 2)]))
    #plt.show()

###############################################################################
def APLICAR():
    #inicializacion de variables
    global Fs, b1, b2, m1, m2, a1, a2, sf, t, data, a
    
    a = 1
    #abrir archivo grabado
    rate, data = wavfile.read("primer.wav")
    #imprmir en tiempo
    t = np.linspace(0, (len(data) / rate), num = len(data))
    #graficar
    
    #plt.figure(1)
    #plt.plot(t, sf)
    #plt.show()
    #tamaño a 16 bit
    scaled = np.int16(sf)
    #escribir archivo con filtro
    write(("s_filtrada.wav"), Fs, scaled)

###############################################################################
def TIEMPO():
    #inicializacion de variables
    global t, rate, data
    #abrir documento 
    rate, data = wavfile.read("primer.wav")
    #conversion a tiempo
    t = np.linspace(0, (len(data) / rate), num = len(data))
    #graficar
    plt.figure(1)
    plt.plot(t, data)
    plt.show()
    
###############################################################################
def FRECUENCIA():  
    #abrir archivo 
    Fs, y = wavfile.read("primer.wav")
    N = len(y)
    T = 1.0 / Fs
    #transformada de furier
    yf = fft(y)
    xf = np.fft.fftfreq(N, T)[:N//2]
    #graficar en frecuencia
    plt.figure(2)
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    plt.show()
    
###############################################################################
def REPRODUCIR():
    #global t, rate, data
    #comparacion    
    #if a == 0:
    #volumen
    rate, data = wavfile.read("primer.wav")
    #se amplifica la señal data 2 veces y se guarda en c
    c = Volumen.get() * data
    scaled = np.int16(c)
    #se graba el nuevo archivo con nombre diferente#
    wavfile.write("segundo.wav", rate, scaled)
    #abrir archivo
    rf = wave.open('segundo.wav', 'rb')
    #reproducir de a partes de 1024
    prof = rf.getsampwidth()
    channels = rf.getnchannels()
    rate = rf.getframerate()
    audioN = pyaudio.PyAudio()
    stream1  = audioN.open(format = audioN.get_format_from_width(prof), channels = channels, rate = rate, output = True)
    datos = rf.readframes(1024)
    
    while datos != b'':
        stream1.write(datos)
        datos = rf.readframes(1024)
    #cerrar
    rf.close()
    ###############################################################
    #GRAFICAR
    ###############################################################
        #abrir documento 
    #rate, data = wavfile.read("primer.wav")
    #conversion a tiempo
    t = np.linspace(0, (len(data) / rate), num = len(data))
    ###############################################################
    N = len(data)
    T = 1.0 / rate
    #transformada de furier
    yf = fft(data)
    xf = np.fft.fftfreq(N, T)[:N//2]
    #graficar en tiempo
    plt.figure(1)
    plt.subplot(211)             # the first subplot in the first figure
    plt.xlabel('A')
    plt.ylabel('B')
    plt.title('Tiempo')
    plt.plot(t, data)
    #graficar en frecuencia
    plt.subplot(212)             # the second subplot in the first figure
    plt.xlabel('C')
    plt.ylabel('D')
    plt.title('Frecuencia')
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    plt.show()

def REPRODUCIRFFT():
    if a == 1:  
        #volumen
        rate, data = wavfile.read("s_filtrada.wav")
        #se amplifica la señal data 2 veces y se guarda en c
        c = Volumen.get() * data
        scaled = np.int16(c)
        #se graba el nuevo archivo con nombre diferente#
        wavfile.write("Tercer.wav", rate, scaled)
        rf = wave.open('Tercer.wav', 'rb')
    
        prof = rf.getsampwidth()
        channels = rf.getnchannels()
        rate = rf.getframerate()
        audioN = pyaudio.PyAudio()
        stream1  = audioN.open(format=audioN.get_format_from_width(prof), channels=channels, rate=rate, output=True)
        datos = rf.readframes(1024)
        
        while datos != b'':
            stream1.write(datos)
            datos = rf.readframes(1024)
        #cerrar
        rf.close()

        ###############################################################
        #GRAFICAR
        ###############################################################
         #abrir documento 
        #rate, data = wavfile.read("s_filtrada.wav")
        #conversion a tiempo
        t = np.linspace(0, (len(data) / rate), num = len(data))
        ###############################################################
        N = len(data)
        T = 1.0 / rate
        #transformada de furier
        yf = fft(data)
        xf = np.fft.fftfreq(N, T)[:N//2]
        #graficar en tiempo
        plt.figure(2)
        plt.subplot(211)             # the first subplot in the first figure
        plt.xlabel('A')
        plt.ylabel('B')
        plt.title('Tiempo')
        plt.plot(t, data)
        #graficar en frecuencia
        plt.subplot(212)             # the second subplot in the first figure
        plt.xlabel('C')
        plt.ylabel('D')
        plt.title('Frecuencia')
        plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
        plt.show()
    
###############################################################################
#creacion de ventana principal
ventana = Tk()
#tamaño
ventana.geometry("700x300+100+200")
#fondo
imagen = PhotoImage(file = "fondo.png")
fondo = Label(ventana, image = imagen).place(x = 0, y = 0)
#titulo
ventana.title("Ecualizador")
lblusuario2 = Label(text = " ECUALIZADOR ").place(x = 270, y = 10)
a = 0
b = 0
#imagenes
Play = PhotoImage(file = "Play.gif")
LabelPlay = Label(text = "Reproducir \nOriginal").place(x = 25, y = 90)
LabelPlayFFT = Label(text = "Reproducir \nFFT").place(x = 25, y = 200)
#botones
btnReproducir = Button(ventana, image = Play, command = REPRODUCIR, font = ("Arial", 14)).place(x = 30, y = 30)
btnReproducirFFT = Button(ventana, image = Play, command = REPRODUCIRFFT, font = ("Arial", 14)).place(x = 30, y = 140)
btnFFT = Button(ventana, text = "FFT", command = FILTRO, font = ("Arial", 14)).place(x = 300, y = 208)
btnAplicar = Button(ventana, text = "APLICAR", command = APLICAR, font = ("Arial", 14)).place(x = 380, y = 208)
#sliders
Bajo1 = DoubleVar()
Bajo2 = DoubleVar()
Medio1 = DoubleVar()
Medio2 = DoubleVar()
Alto1 = DoubleVar()
Alto2 = DoubleVar()
Volumen = DoubleVar()
#ubicacion de slider
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Bajo1).place(x = 100, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Bajo2).place(x = 180, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Medio1).place(x = 260, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Medio2).place(x = 340, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Alto1).place(x = 420, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 100, width = 10,from_ = 2,to = 0, resolution = 0.1, variable = Alto2).place(x = 500, y = 70)
sldbarra = Scale(ventana, orient = VERTICAL, length = 200, width = 20,from_ = 2,to = 0, resolution = 0.1, variable = Volumen).place(x = 595, y = 70)
#titulo de sliders
lblusuario2 = Label(text = " 60 Hz ").place(x = 105, y = 50)
lblusuario2 = Label(text = " 250 Hz ").place(x = 178, y = 50)
lblusuario2 = Label(text = " 2000 Hz ").place(x = 258, y = 50)
lblusuario2 = Label(text = " 4000 Hz ").place(x = 332, y = 50)
lblusuario2 = Label(text = " 6000 Hz ").place(x = 412, y = 50)
lblusuario2 = Label(text = " 16000 Hz ").place(x = 504, y = 50)
lblusuario2 = Label(text = " VOLUMEN ").place(x = 584, y = 50)
#menus
# paso 1 crear la barra de menus
barramenu = Menu(ventana)
#paso 2 crear los menus
mnuarchivo = Menu(barramenu)
mnugrafica = Menu(barramenu)
#paso 3 crear los comandos de los menus
mnuarchivo.add_command(label = "Importar", command = IMPORTAR)
mnuarchivo.add_command(label = "Exportar", command = GUARDAR)
#mnuarchivo.add_separator()
mnuarchivo.add_command(label = "Salir", command = ventana.destroy)
mnugrafica.add_command(label = "Tiempo", command = TIEMPO)
mnugrafica.add_command(label = "Frecuencia", command = FRECUENCIA)
#paso 4 agergar los menus a la barra de menus
barramenu.add_cascade(label = "Archivo", menu = mnuarchivo)
barramenu.add_cascade(label = "Graficas", menu = mnugrafica)
#paso 5 indicamos que la barra de menus estara en la ventana
ventana.config(menu = barramenu)
#cerrar ventana principal
ventana.mainloop()
###############################################################################