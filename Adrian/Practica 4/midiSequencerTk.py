
import instrument
from tkinter import *
from consts import *
import sounddevice as sd
import numpy as np
import mido
import time 


class MidiSequencerTk:
    # análogo a lo anterior
    def __init__(self,tk,instrument=None, instrument2=None):
        if instrument == None:            
            self.instrument = instrument.Instrument(tk,amp=0.2,ratio=3,beta=0.6)
        else:
            self.instrument = instrument

        if instrument2 == None:            
            self.instrument2 = instrument2.Instrument(tk,amp=0.2,ratio=3,beta=0.6)
        else:
            self.instrument2 = instrument2

        frame = LabelFrame(tk, text="Midi Sequencer", bg="#908060")
        frame.pack(side=LEFT)

        frameFile = Frame(frame, highlightbackground="blue", highlightthickness=6)
        frameFile.pack(side=TOP)
        Label(frameFile,text='Archivo MIDI: ').pack(side=TOP)
 
        self.file = Entry(frameFile) #.pack(side=RIGHT)
        self.file.insert(14,"pirates.mid")
        self.file.pack(side=TOP)

        self.transport = 0
        
        
        self.text = Text(frame,height=6,width=23)
        self.text.pack(side=RIGHT)
        playBut = Button(frame,text="Play", command=self.play)
        playBut.pack(side=TOP)
        stopBut = Button(frame,text="Stop", command=self.stop)
        stopBut.pack(side=BOTTOM)

        #------

        frame2 = LabelFrame(tk, text="Midi Sequencer2", bg="#908060")
        frame2.pack(side=LEFT)

        frameFile2 = Frame(frame2, highlightbackground="red", highlightthickness=6)
        frameFile2.pack(side=TOP)
        Label(frameFile2,text='Archivo MIDI 2: ').pack(side=TOP)
 
        self.file2 = Entry(frameFile2) #.pack(side=RIGHT)
        self.file2.insert(14,"pirates.mid")
        self.file2.pack(side=TOP)

        self.transport = 0
        
        
        self.text2 = Text(frame2,height=6,width=23)
        self.text2.pack(side=RIGHT)
        playBut2 = Button(frame2,text="Play", command=self.play)
        playBut2.pack(side=TOP)
        stopBut2 = Button(frame2,text="Stop", command=self.stop)
        stopBut2.pack(side=BOTTOM)

        self.tick = 1
        self.state = 'off'
        
    # obtención de la secuencia midi (noteOn/Off) con tiempos relativos al inicio
    def getSeq(self,midiEvents):
        seq = []
        accTime = 0
        for m in midiEvents:
            accTime += m.time
            if m.type=='note_on':
                if m.velocity==0: seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
                else: seq.append((accTime,'noteOn',m.note+self.transport,m.channel))    
            elif m.type=='note_off':
                seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
        return seq

  
    def play(self):
        events = mido.MidiFile(self.file.get())
        seq = self.getSeq(events)
        print(seq)

        self.state = 'on'
        self.playLoop(seq)

    def playLoop(self,seq,item=0,accTime=0):   
        if item>=len(seq) or self.state =='off':
            return

        # ahora tenemos que procesar todos los ítems cuyo tiempo supere el crono accTime    
        while item<len(seq) and accTime>=seq[item][0]:
            (_,msg,midiNote,_chan) = seq[item]  # (time,'noteOff',midNote,channel)
            self.text.insert('6.0',  f'{msg} {midiNote}\n') 
            if msg=='noteOn':  
                self.instrument.noteOn(midiNote)                   
            else: # msg noteOff    
                self.instrument.noteOff(midiNote)                   
            item += 1 # y avanzmos ítem


        # avanzammos crono 
        accTime += self.tick/1000

        self.text.after(self.tick,lambda: self.playLoop(seq,item,accTime)) 

         
    def stop(self):
        self.instrument.stop()
        self.state = 'off'   
