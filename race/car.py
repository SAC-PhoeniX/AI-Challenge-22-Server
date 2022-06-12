from os import environ
NO_TF = environ.get("MODELS", "TF") == "NO_TF"
if not NO_TF:
    import numpy as np
    import tensorflow as tf
    from tensorflow import keras

from random import choice
from uuid import uuid4, UUID
from .race_object import RaceObject


ADJECTIVES = ["Fast", "Jetting", "Quick", "Agile", "Stable", "Derpy", "Distracted"]
NOUNS = ["Driver", "Model", "Getaway Driver", "AI", "Xenial", "Agent"]


class Car(RaceObject):

    model_cache = {}

    def __init__(self, team, name: str, model_filename: str):
        super().__init__()
        if not name:
            name = choice(ADJECTIVES) + " " + choice(NOUNS)
        self.name: str = name
        self.team: Team = team

        self.model = type(self).load_model(model_filename)
        pass

    def serialize(self, include_team) -> dict:
        obj = {
            "name": self.name,
            "id": self.get_id(),
            "color": self.team.color,
            "team_id": self.team.get_id()
        }
        
        if include_team:
            obj["team"] = self.team.serialize(False)

        return obj

    def infer(self, inp):
        out = self.model.predict(np.array([inp]) if not NO_TF else [inp])
        return out[0,:].tolist() if not NO_TF else out[0]



    @staticmethod
    def load_model(model_filename):
        if NO_TF:
            return MockModel(model_filename)
        else:
            if model_filename not in Car.model_cache:
                Car.model_cache[model_filename] = keras.models.load_model(f"nets/{model_filename}")

            return Car.model_cache[model_filename]


class MockModel():
    def __init__(self, filename):
        self.name = filename

    def predict(self, inp):
        print("predicting using " + str(self.name) + " and input " + str(inp))
        return [[60, 0]]