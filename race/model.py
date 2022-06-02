from os import environ
NO_TF = environ.get("MODELS", "TF") == "NO_TF"
if not NO_TF:
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
from random import choice

class Model:
    model_cache = {}

    def __init__(self, filename, name):
        self.model = Model.load_model(filename)
        print(self.model)


    def infer(self, inp):
        pass

    def serialize(self):
        return {"name": self.name}





class MockModel:
    def __init__(self, filename):
        self.name = filename

    def predict(self, inp):
        print("predicting using " + str(self.name) + " and input " + str(inp))
        return [[0, 0]]