#Adrian del Pozo
#Ines Primo

import instrument
from tkinter import *
from consts import *
import sounddevice as sd
import numpy as np
import mido
import time 


class MidiSequencerTk:
    # análogo a lo anterior
    def __init__(self,tk,instrument=None):
        if instrument == None:            
            self.instrument = instrument.Instrument(tk,amp=0.2,ratio=3,beta=0.6)
        else:
            self.instrument = instrument

        self.recording = FALSE

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
        self.text.pack(side=LEFT)


        playBut = Button(frame,text="Play", command=lambda: self.play())
        playBut.pack(side=LEFT)
        stopBut = Button(frame,text="Stop", command=self.stop)
        stopBut.pack(side=LEFT)

        recordBut = Button(frame,text="Record", command=lambda: self.startRecord())
        recordBut.pack(side=RIGHT)
        recordStopBut = Button(frame,text="RecordStop", command=lambda: self.stopRecord())
        recordStopBut.pack(side=RIGHT)

        self.textRecord = Text(frame,height=4,width=40)
        self.textRecord.pack(side=BOTTOM)
        self.textRecord.bind('<KeyPress>', self.down)
        self.textRecord.bind('<KeyRelease>', self.up)

        #------

        self.tick = 1
        self.recordAccTime = 0

        self.mid = mido.MidiFile()
        
        self.track = mido.MidiTrack()

        self.mid.tracks.append(self.track)

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

    def startRecord(self):
        self.recording = TRUE
        self.recordAccTime = 0
        self.recordingTime()

    def recordingTime(self):
        
        self.recordAccTime += self.tick/1000

        self.track.append(mido.MetaMessage('key_signature', key='Dm'))
        self.track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))
        self.track.append(mido.MetaMessage('time_signature', numerator=6, denominator=8))

        #self.track.append(mido.Message('program_change', program=12, time=10))

        if self.recording:
            self.textRecord.after(self.tick, lambda: self.recordingTime())

    def stopRecord(self):
        
        self.track.append(mido.MetaMessage('end_of_track'))

        self.mid.save("mySong3.mid")

        self.recording = FALSE
    
    # lectura de teclas de teclado como eventos tkinter
    def down(self,event):

        if self.recording:
            c = event.keysym

            # tecla "panic" -> apagamos todos los sintes de golpe!
            if c=='0': 
                self.stop()            
            elif c in teclas:

                print("Time is " + (str)(self.recordAccTime))

                midiNote = 48+teclas.index(c) # buscamos indice y trasnportamos a C3 (48 en midi) 
                self.track.append(mido.Message('note_on', channel=1, note = midiNote, velocity=16, time = (int)(self.recordAccTime * 20)))       
                self.instrument.noteOn(midiNote,0)         # arrancamos noteOn con el instrumento 
            elif c in teclas2:
                midiNote = 60+teclas2.index(c) # buscamos indice y trasnportamos a C3 (60 en midi)    
                self.track.append(mido.Message('note_on', channel=0, note = midiNote, velocity=16, time = (int)(self.recordAccTime * 20)))  
                self.instrument.noteOn(midiNote,1)        # arrancamos noteOn con el instrumento 
        else:
            print("You are not recording")
            

    def up(self,event):

        if self.recording:
            c = event.keysym
            if c in teclas:
                midiNote = 48+teclas.index(c) # buscamos indice y hacemos el noteOff
                self.track.append(mido.Message('note_off', channel=1, note = midiNote, velocity=32, time = (int)(self.recordAccTime * 20)))  
                self.instrument.noteOff(midiNote) 
            elif c in teclas2:
                midiNote = 60+teclas2.index(c) # buscamos indice y hacemos el noteOff
                self.track.append(mido.Message('note_off', channel=0, note = midiNote, velocity=32, time = (int)(self.recordAccTime * 20)))
                self.instrument.noteOff(midiNote) 
        else:
            print("You are not recording")

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
            print("Wrong index in PlayLoop")

            if msg=='noteOn':  
                self.instrument.noteOn(midiNote,_chan)                   
            else: # msg noteOff    
                self.instrument.noteOff(midiNote)                   
            item += 1 # y avanzmos ítem

        # avanzammos crono 
        accTime += self.tick/1000


        self.text.after(self.tick,lambda: self.playLoop(seq, item=item, accTime=accTime))



         
    def stop(self):
        self.instrument.stop()
        self.state = 'off'   
