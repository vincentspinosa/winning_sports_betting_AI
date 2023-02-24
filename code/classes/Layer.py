import numpy as np
import pandas as pd

from Vector import Vector
from Algorithm import Algorithm

class Layer:

    def __init__(self, data) -> None:
        #self.data = df 
        #self.cible = headerCible
        self.data = data
        self.shape = data.shape[1]
        self.trained = False
        self.vector = Vector([self.shape], dtype=object)
        self.coefs = np.zeros([self.shape.size])
        #self.prediction = None
        
    #def populate(self) -> None:
        #for i in range(self.shape):
            #self.vector[i] = self.data[i]

    def train(self) -> object:
        self.coefs = Algorithm(self)
        self.trained = True
        return self.coefs

    def print_layer(self):
        return
    def print_data(self):
        return
    def print_shape(self):
        return
    def print_trained(self):
        return
    def print_vector(self):
        return
    def print_coefs(self):
        return