
import numpy as np   
import osc
import matplotlib.pyplot as plt
import scipy.signal as sg 
from consts import *

class OscFM:
    def __init__(self,fc=110.0,amp=1.0,fm=6.0, beta = osc.Osc(), shapeFM='sin', shapeFC='sin'):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0
        self.shapeFM = shapeFM
        self.shapeFC = shapeFC

        # moduladora = βsin(2πfm)
        self.mod = osc.Osc(freq=fm,amp=self.beta.amp,shape=self.shapeFM)
        
    def next(self):  
        # sin(2πfc+mod)  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()
        beta = self.beta.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+CHUNK)        
        # aplicamos formula

        if self.shapeFC=='sin':
            out = self.amp* np.sin(2*np.pi*self.fc*sample/SRATE + mod + beta)
        elif self.shapeFC=='square':
            out = self.amp* sg.square(2*np.pi*self.fc*sample/SRATE + mod + beta)
        elif self.shapeFC=='sawtooth':
            out = self.amp* sg.sawtooth(2*np.pi*self.fc*sample/SRATE + mod + beta)
        elif self.shapeFC=='triangle':
            # Ojo, la triangular no existe como tal en scipy, pero podemos hacerla con dos sawtooth
            # el 2º parametro define la "rampa" la subida y bajada (ver documentacion)
            out = self.amp* sg.sawtooth(2*np.pi*self.fc*sample/SRATE + mod + beta, 0.5)

        self.frame += CHUNK
        return out 

    def setBetaFreq(self,betaFreq):
        self.beta.freq = betaFreq

    def setBetaAmp(self,betaAmp):
        self.beta.amp = betaAmp
        self.mod.amp = betaAmp

    def setFm(self,fm):
        self.fm = fm
        self.mod.freq = fm

    def setShapeFM(self, shape):
        self.mod.setShape(shape)

    def setShapeFC(self, shape):
        if shape=='square' or shape=='sawtooth' or shape=='triangle':
            self.shapeFC = shape
        else:
            self.shapeFC = 'sin'

    def getBetaFreq(self):
        return self.beta.freq  

    def getBetaAmp(self):
        return self.beta.amp 

    def getFm(self):
        return self.fm

    

        
