import weakref
from abc import ABCMeta, abstractmethod
import numpy as np


class Layer(metaclass=ABCMeta):
    @abstractmethod
    def forward(self, inp):
        return inp


class Linear(Layer):
    def __init__(self, weights: np.array, biases: np.array):
        self.weights = weights
        self.biases = biases

    def forward(self, inp):
        return self.weights @ inp + self.biases


class SlotsLinear(Layer):
    __slots__ = ("weights", "biases")

    def __init__(self, weights: np.array, biases: np.array):
        self.weights = weights
        self.biases = biases

    def forward(self, inp):
        return self.weights @ inp + self.biases


class WeakrefLinear(Layer):
    def __init__(self, weights: np.array, biases: np.array):
        self.weights = weakref.ref(weights) if weights is not None else None
        self.biases = weakref.ref(biases) if biases is not None else None

    def forward(self, inp):
        if self.weights() is not None and self.biases() is not None:
            return self.weights() @ inp + self.biases()
        return None
