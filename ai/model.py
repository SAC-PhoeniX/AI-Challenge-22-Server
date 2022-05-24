from os import environ
NO_TF = environ.get("MODELS", "") == "NO_TF"
if not NO_TF:
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras
from random import choice

ADJECTIVES = ["Fast", "Jetting", "Quick", "Agile", "Stable", "Derpy", "Distracted"]
NOUNS = ["Driver", "Model", "Getaway Driver", "AI", "Xenial", "Agent"]

class Model:
    def __init__(self, filename, name):
        if not name:
            name = choice(ADJECTIVES) + " " + choice(NOUNS)
        self.name = name
        self.model = Model.load_model(filename)
        print(self.model)


    @staticmethod
    def load_model(model_filename):
        # return keras.models.Sequential(name="testModel")
        if NO_TF:
            return MockModel(model_filename)
        else:
            return keras.models.load_model(f"nets/{model_filename}")

    def infer(self, inp):
        return self.model.predict(inp)

    def serialize(self):
        return {"name": self.name}


class MockModel:
    def __init__(self, filename):
        self.name = filename
    def predict(x):
        return [0 for _ in range(17)]