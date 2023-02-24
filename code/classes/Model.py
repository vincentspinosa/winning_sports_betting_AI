import numpy as np

from Layer import Layer

class Model:

    def __init__(self):
        self.input = None
        self.output = None
        self.fitted = False
        self.layers = np.empty([0], dtype=object)
        self.coefs = np.empty([0], dtype=object)

    def set_input(self):
        return None

    def set_output(self):
        return None

    def add_layer(self, layer) -> object:
        if type(layer) == list:
            for el in layer:
                self.layers = np.append(self.layers, el)
        else:
            self.layers = np.append(self.layers, layer)
        return self.layers

    def remove_layer(self, index) -> object:
        self.layers = np.delete(self.layers, index)
        return self.layers

    def fit(self):
        for lay in self.layers:
            lay.train()
            self.coefs = np.append(self.coefs, lay.coefs)
        self.fitted = True
        return self.coefs

    def make_predictions(self):
        return

    def print_model(self):
        return
    def print_input(self):
        return
    def print_output(self):
        return
    def print_layer(self):
        return
    def print_coefs(self):
        return
    def print_predictions(self):
        return