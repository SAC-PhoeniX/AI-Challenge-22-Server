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
    model_cache = {}

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
            if model_filename not in Model.model_cache:
                Model.model_cache[model_filename] = keras.models.load_model(f"nets/{model_filename}")

            return Model.model_cache[model_filename]

    def infer(self, inp):
        return self.model.predict(np.array([inp]))[0,:]

    def serialize(self):
        return {"name": self.name}


class MockModel:
    def __init__(self, filename):
        self.name = filename

    def predict(self, inp):
        print("predicting using " + str(self.name) + " and input " + str(inp))
        return [0, 0]