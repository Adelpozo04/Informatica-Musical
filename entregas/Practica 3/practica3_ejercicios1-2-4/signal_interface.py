#Adrian del Pozo Hernandez
#Ines Primo Lopez

from consts import *
from abc import ABC, abstractmethod
import numpy as np         
import sounddevice as sd       
import matplotlib.pyplot as plt
import scipy.signal as sg 

class Signal_Interface(ABC):
   @abstractmethod
   def __init__():
        pass
      
   @abstractmethod
   def next(self):
       pass 
        

         
