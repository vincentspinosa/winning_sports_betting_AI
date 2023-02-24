import numpy as np

class Vector:
    def __init__(self, shape, datatype) -> None:
        self = np.empty([shape], dtype=datatype)
    def print_vector(self):
        return