import numpy as np
import tensorflow as tf
from tensorflow import keras
from random import choice

ADJECTIVES = ["Fast", "Jetting", "Quick", "Agile", "Stable", "Derpy", "Distracted"]
NOUNS = ["Driver", "Model", "Getaway Driver", "AI", "Xenial", "Agent"]

class Model:
    model: keras.Model

    def __init__(self, filename, name):
        if not name:
            name = choice(ADJECTIVES) + " " + choice(NOUNS)
        self.name = name
        self.model = Model.load_model(filename)
        print(self.model)


    @staticmethod
    def load_model(model_filename):
        # return keras.models.Sequential(name="testModel")
        return keras.models.load_model(f"nets/{model_filename}")

    def infer(self, inp):
        return self.model.predict(inp)

    def serialize(self):
        return {"name": self.name}