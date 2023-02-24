import numpy as np

from Layer import Layer
from Vector import Vector

class Algorithm:
    def __init__(self, layer) -> object:
        for i in range(layer.neurons.size):
            layer.coefs[i] = 1
        return layer.coefs