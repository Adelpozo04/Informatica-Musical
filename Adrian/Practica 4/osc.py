#Adrian del Pozo
#Ines Primo

from consts import *
from signal_interface import *
from constante import *
from abc import ABC, abstractmethod
import numpy as np         
import sounddevice as sd       
import matplotlib.pyplot as plt
import scipy.signal as sg 

class Osc(Signal_Interface):
    def __init__(self,freq=Constante(440),amp=Constante(1.0),phase=Constante(0.0),shape='sin'):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.frame = 0
        self.shape = shape

    def next(self):    
         
         if self.shape=='sin':
            out = np.sin(2*np.pi*(np.arange(self.frame,self.frame + CHUNK))*(self.freq.next())/SRATE+(self.phase.next()))
         elif self.shape=='square':
            out = sg.square(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq.next()/SRATE+self.phase.next())
         elif self.shape=='sawtooth':
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq.next()/SRATE+self.phase.next())
         elif self.shape=='triangle':
            # Ojo, la triangular no existe como tal en scipy, pero podemos hacerla con dos sawtooth
            # el 2º parametro define la "rampa" la subida y bajada (ver documentacion)
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq.next()/SRATE+self.phase.next(),0.5)
         self.frame += CHUNK

         return np.float32(self.amp.next()*out)
    
    def setShape(self, shape):
        if shape=='square' or shape=='sawtooth' or shape=='triangle':
            self.shape = shape
        else:
            self.shape = 'sin'
            
