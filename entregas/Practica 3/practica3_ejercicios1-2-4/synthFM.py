#Adrian del Pozo Hernandez
#Ines Primo Lopez

import numpy as np   
import matplotlib.pyplot as plt
from consts import *
from tkinter import *
from adsr import *
from oscFM import *

class SynthFM:
    def __init__(self,
                fc=Constante(110),amp=Constante(1.0),ratio=Constante(0.5), betaFreq = Constante(440), betaAmp = Constante(0.3),   # parámetros del generador FM
                attack=0.01,decay=0.02, sustain=0.3,release=1.0, shapeFM='sin', shapeFC='sin'): # parámetros del ADSR        
        self.fc = fc
        self.amp =  amp
        self.ratio = ratio
        self.fm = Constante(self.ratio.next()*self.fc.next()) # fm en función de fc y ratio
        self.beta = osc.Osc(freq=betaFreq, amp=betaAmp)
        self.betaFreq = betaFreq
        self.betaAmp = betaAmp
        self.shapeFM = shapeFM
        self.shapeFC = shapeFC
        
        self.signal = OscFM(self.fc,amp=self.amp,fm=self.fm, beta = self.beta, 
                            shapeFM=self.shapeFM, shapeFC=self.shapeFC) # generador
        self.adsr = ADSR(attack,decay,sustain,release)  # envolvente adsr

        # se dispara automáticamente
        self.state = 'on' # activo
        self.adsr.start() # adsr activa

    def start(self):
        self.adsr.start()

    # siguiente chunk del generador
    def next(self): 
        out = self.signal.next()*self.adsr.next()
        if self.adsr.state=='off': # cuando acaba el adsr por completo (incluido el release)
            self.state = 'off'     # el sinte tb acaba de producir señal
        return out     
    
    # el noteOff del sinte activa el release del ADSR
    def noteOff(self):
        #print('release')
        self.adsr.release()

    def setAmp(self,val): 
        self.amp = val 

    def setFm(self,val): 
        self.fm = val  

    def setBetaFreq(self,betaFreq):
        self.beta.freq = betaFreq

    def setBetaAmp(self,betaAmp):
        self.beta.amp = betaAmp

    def setShapeFM(self, shape):
        self.signal.setShapeFM(shape)

    def setShapeFC(self, shape):
        self.signal.setShapeFC(shape)
