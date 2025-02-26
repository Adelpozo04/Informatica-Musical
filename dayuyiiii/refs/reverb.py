
from consts import *
from pedalboard import Pedalboard, Compressor, Reverb
from slider import *


class MiReverb:
    def __init__(self,tk,signal):
        self.signal = signal
        frame = LabelFrame(tk, text="PB Reverb", bg="#808090")
        frame.pack(side=BOTTOM)
        
        self.wetlS = Slider(frame,'WetLevel',packSide=TOP,
                           ini=0.0,from_=0.0,to=1.0,step=0.05) 
        
        self.board = Pedalboard([Reverb()])
        self.rev = self.board[0]
        self.rev.wet_level = .3

    def next(self):
        chunk = self.signal.next()
        self.rev.wet_level = self.wetlS.get()
        #print(self.rev.wet_level)
        chunk = self.board.process(chunk,sample_rate=SRATE, reset=False)
        return chunk
