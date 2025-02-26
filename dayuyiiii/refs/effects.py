
from consts import *
from pedalboard import Pedalboard, Compressor, Reverb, Gain, Chorus, LadderFilter, Phaser
from slider import *


class Effects:
    def __init__(self,tk,signal):
        self.signal = signal
        frame = LabelFrame(tk, text="PB Reverb", bg="#808090")
        frame.pack(side=BOTTOM)
        
        self.wetlS = Slider(frame,'WetLevel',packSide=TOP,                          ini=0.0,from_=0.0,to=1.0,step=0.05) 
        
        self.board = Pedalboard([
            Compressor(threshold_db=-50, ratio=25),
            Gain(gain_db=30),
            Chorus(),
            LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=900),
            Phaser(),
            #Convolution("./guitar_amp.wav", 1.0),
            Reverb(room_size=0.25),
        ])


    def next(self):
        chunk = self.signal.next()
        #self.rev.wet_level = self.wetlS.get()
        #print(self.rev.wet_level)
        chunk = self.board.process(chunk,sample_rate=SRATE, reset=False)
        return chunk
