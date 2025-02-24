
from consts import *
from tkinter import *
from slider import *
from adsr import *
from constante import *
from synthFM import *
from tkinter import ttk 

class Instrument:
    def __init__(self,tk,name="FM synthetizer",amp=0.2,ratio=3,betaFreq=0, betaAmp=1.0): 
        
        frame = LabelFrame(tk, text=name, bg="#808090")
        frame.pack(side=LEFT)
        # Synth params con sus sliders
        frameOsc = LabelFrame(frame, text="FM oscillator", bg="#808090")
        frameOsc.pack(side=LEFT, fill="both", expand="yes")
        
        self.ampS = Slider(frameOsc,'amp',packSide=TOP,
                           ini=amp,from_=0.0,to=1.0,step=0.05) 

        self.ratioS = Slider(frameOsc,'ratio',packSide=TOP,
                           ini=ratio,from_=0.0,to=20.0,step=0.5)
    
        self.betaFreqS = Slider(frameOsc,'betaFreq',packSide=TOP,
                            ini=betaFreq,from_=0.0,to=110.0,step=1) 
        
        self.betaAmpS = Slider(frameOsc,'betaAmp',packSide=TOP,
                            ini=betaAmp,from_=0.0,to=10.0,step=0.5) 
        
        # una ventana de texto interactiva para poder lanzar notas con el teclado del ordenador
        text = Text(frameOsc,height=4,width=40)
        text.pack(side=BOTTOM)
        text.bind('<KeyPress>', self.down)
        text.bind('<KeyRelease>', self.up)

        shapes = LabelFrame(frame, text="Shapes", bg="#808090")
        shapes.pack(side=BOTTOM, fill="both", expand="yes")

        sFM = LabelFrame(shapes, text="FM", bg="#808090")
        sFM.pack(side=LEFT, fill="both", expand="yes")

        sFC = LabelFrame(shapes, text="FC", bg="#808090")
        sFC.pack(side=LEFT, fill="both", expand="yes")

        self.shapeFM = ttk.Combobox(sFM, width = 27, state="readonly", values=['sin','triangle','square','sawtooth']) 

        self.shapeFM.set("sin")

        self.shapeFM.pack(side=LEFT)

        self.shapeFC = ttk.Combobox(sFC, width = 27, state="readonly", values=['sin','triangle','square','sawtooth']) 

        self.shapeFC.set("sin")

        self.shapeFC.pack(side=LEFT)
        
        
        # ADSR params con sus sliders
        frameADSR = LabelFrame(frame, text="ADSR", bg="#808090")
        frameADSR.pack(side=LEFT, fill="both", expand="yes", )
        self.attackS = Slider(frameADSR,'attack',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP) 

        self.decayS = Slider(frameADSR,'decay',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP)

        self.sustainS = Slider(frameADSR,'sustain',
                   ini=0.4,from_=0.0,to=1.0,step=0.01,orient=HORIZONTAL,packSide=TOP) 
                    
        self.releaseS = Slider(frameADSR,'release',
                   ini=0.5,from_=0.0,to=4.0,step=0.05,orient=HORIZONTAL,packSide=TOP) 
        
        #Instrumento 2

        frame2 = LabelFrame(tk, text=name, bg="#808090")
        frame2.pack(side=BOTTOM)
        # Synth params con sus sliders
        frameOsc2 = LabelFrame(frame2, text="FM oscillator 2", bg="#808090")
        frameOsc2.pack(side=LEFT, fill="both", expand="yes")
        
        self.ampS2 = Slider(frameOsc2,'amp 2',packSide=TOP,
                           ini=amp,from_=0.0,to=1.0,step=0.05) 

        self.ratioS2 = Slider(frameOsc2,'ratio 2',packSide=TOP,
                           ini=ratio,from_=0.0,to=20.0,step=0.5)
    
        self.betaFreqS2 = Slider(frameOsc2,'betaFreq 2',packSide=TOP,
                            ini=betaFreq,from_=0.0,to=110.0,step=1) 
        
        self.betaAmpS2 = Slider(frameOsc2,'betaAmp 2',packSide=TOP,
                            ini=betaAmp,from_=0.0,to=10.0,step=0.5) 

        shapes2 = LabelFrame(frame2, text="Shapes 2", bg="#808090")
        shapes2.pack(side=BOTTOM, fill="both", expand="yes")

        sFM2 = LabelFrame(shapes2, text="FM 2", bg="#808090")
        sFM2.pack(side=LEFT, fill="both", expand="yes")

        sFC2 = LabelFrame(shapes2, text="FC 2", bg="#808090")
        sFC2.pack(side=LEFT, fill="both", expand="yes")

        self.shapeFM2 = ttk.Combobox(sFM2, width = 27, state="readonly", values=['sin','triangle','square','sawtooth']) 

        self.shapeFM2.set("sin")

        self.shapeFM2.pack(side=LEFT)

        self.shapeFC2 = ttk.Combobox(sFC2, width = 27, state="readonly", values=['sin','triangle','square','sawtooth']) 

        self.shapeFC2.set("sin")

        self.shapeFC2.pack(side=LEFT)
        
        
        # ADSR params con sus sliders
        frameADSR2 = LabelFrame(frame2, text="ADSR 2", bg="#808090")
        frameADSR2.pack(side=LEFT, fill="both", expand="yes", )
        self.attackS2 = Slider(frameADSR2,'attack 2',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP) 

        self.decayS2 = Slider(frameADSR2,'decay 2',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP)

        self.sustainS2 = Slider(frameADSR2,'sustain 2',
                   ini=0.4,from_=0.0,to=1.0,step=0.01,orient=HORIZONTAL,packSide=TOP) 
                    
        self.releaseS2 = Slider(frameADSR2,'release 2',
                   ini=0.5,from_=0.0,to=4.0,step=0.05,orient=HORIZONTAL,packSide=TOP)
        
        # canales indexados por la nota de lanzamiento -> solo una nota del mismo valor
        self.channels = dict()        
        self.tails = dict()
                         

    # obtenemos todos los parámetros del sinte (puede servir para crear presets)
    def getConfigFirstInstrument(self):
        return (self.ampS.get(),self.ratioS.get(),self.betaFreqS.get(), self.betaAmpS.get(),
                self.attackS.get(), self.decayS.get(), self.sustainS.get(),
                self.releaseS.get(), self.shapeFM.get(), self.shapeFC.get())
    
    def getConfigSecondInstrument(self):
        return (self.ampS2.get(),self.ratioS2.get(),self.betaFreqS2.get(), self.betaAmpS2.get(),
                self.attackS2.get(), self.decayS2.get(), self.sustainS2.get(),
                self.releaseS2.get(), self.shapeFM2.get(), self.shapeFC2.get())

    # activación de nota
    def noteOn(self,midiNote, instrument = 0):
        # si está el dict de canales apagamos nota actual con envolvente de fadeout
        # y guardamos en tails. El next devolverá este tail y luego comenzará la nota
        if midiNote in self.channels:                   
            lastAmp = self.channels[midiNote].adsr.last # ultimo valor de la envolvente: inicio del fadeOut
            env = Env([(0,lastAmp),(CHUNK,0)]).next()   # envolvente             
            signal = self.channels[midiNote].next()     # señal          
            self.tails[midiNote] = env*signal           # diccionario de tails (notas apagadas) 

        # generamos un nuevo synth en un canal indexado con notaMidi
        # con los parámetros actuales del synth
        freq= freqsMidi[midiNote]

        print(self.shapeFM.get())

        if instrument == 0:

            self.channels[midiNote]= SynthFM(
                    fc=Constante(freq),
                    amp=Constante(self.ampS.get()), ratio=Constante(self.ratioS.get()), betaFreq=Constante(self.betaFreqS.get()),
                    betaAmp=Constante(self.betaAmpS.get()), attack = self.attackS.get(), decay= self.decayS.get(),
                    sustain=self.sustainS.get(), release=self.releaseS.get(), 
                    shapeFM = self.shapeFM.get(), shapeFC = self.shapeFC.get())
            
        else:

            #Ponerlos en una constante
            self.channels[midiNote]= SynthFM(
                    fc=Constante(freq),
                    amp=Constante(self.ampS2.get()), ratio=Constante(self.ratioS2.get()), betaFreq=Constante(self.betaFreqS2.get()),
                    betaAmp=Constante(self.betaAmpS2.get()), attack = self.attackS2.get(), decay= self.decayS2.get(),
                    sustain=self.sustainS2.get(), release=self.releaseS2.get(), 
                    shapeFM = self.shapeFM2.get(), shapeFC = self.shapeFC2.get())

    # apagar nota -> propagamos noteOff al synth, que se encargará de hacer el release
    def noteOff(self,midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].noteOff()


    # lectura de teclas de teclado como eventos tkinter
    def down(self,event):
        c = event.keysym

        # tecla "panic" -> apagamos todos los sintes de golpe!
        if c=='0': 
            self.stop()            
        elif c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y trasnportamos a C3 (48 en midi)        
            print(f'noteOn {midiNote}')
            self.noteOn(midiNote, 0)         # arrancamos noteOn con el instrumento 
        elif c in teclas2:
            midiNote = 60+teclas2.index(c) # buscamos indice y trasnportamos a C3 (48 en midi)        
            print(f'noteOn {midiNote}')
            self.noteOn(midiNote, 1)         # arrancamos noteOn con el instrumento 
            

    def up(self,event):
        c = event.keysym
        if c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff(midiNote)
        elif c in teclas2:
            midiNote = 60+teclas2.index(c) # buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff(midiNote)

    # siguiente chunck del generador: sumamos señal de canales y hacemos limpia de silenciados
    def next(self):
        out = np.zeros(CHUNK)          
        for c in list(self.channels):            # convertimos las keys a lista para mantener la lista de claves original
            if self.channels[c].state == 'off':  # si no, modificamos diccionario en el bucle de recorrido de claves -> error 
                del self.channels[c]
            else: # si la nota está el diccionario de tails devolvemos el fadeout generado en noteOn y elminamos tail
                if c in self.tails:                  
                    out += self.tails[c]
                    del self.tails[c]
                else:
                    out += self.channels[c].next()
        return out        

    # boton del pánico
    def stop(self):
        self.channels = dict() # delegamos en el garbage collector
        # for c in list(self.channels): del self.channels[c]
