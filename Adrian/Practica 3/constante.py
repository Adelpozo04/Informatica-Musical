
from consts import *
from signal_interface import *
from abc import ABC, abstractmethod

class Constante(Signal_Interface):
    def __init__(self, valor = 0.0):
        self.valor = valor

    def next(self):    
         return self.valor
    
            
