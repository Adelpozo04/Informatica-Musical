
from consts import *
import numpy as np
from tkinter import *
from slider import *
#from controller import *

class LPfilter:
    def __init__(self,tk,signal=None,freq=10000):        
        # señal de entrada
        self.signal = signal

        self.memo = 0.0
        frame = LabelFrame(tk, text="LP Filter", bg="#908060")
        frame.pack(side=TOP)

        self.freqS = Slider(frame,'freq',packSide=TOP,
                           ini=freq,from_=50,to=20000,step=100) 
        
    def next(self):    
        print('entro')  
        # calculo de alpha en función de la frecuencia de corte       
        alpha = np.exp(-2*np.pi*self.freqS.get() / SRATE)       

        # chunk de entrada pedido next() al generador 
        bloque= self.signal.next()
        bloque[0] = alpha * self.memo + (1-alpha) * bloque[0]
        for i in range(1,CHUNK):         
            bloque[i] = alpha * bloque[i-1] + (1-alpha) * bloque[i]            
        
        self.memo = bloque[CHUNK-1]
        return bloque
