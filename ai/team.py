from typing import List
import uuid
import numpy as np
from tensorflow import keras

class Team:
    team_name: str
    models = []
    id: uuid.UUID

    def __init__(self, team_name: str, model_filenames: List[str]) -> None:
        self.team_name = team_name
        self.models = [Team.load_model(mf) for mf in model_filenames]
        self.id = uuid.uuid4()
        pass

    def infer_car(self, input, car_id):
        return self.infer_car(input) if car_id == 0 else self.infer_car2(input)

    def infer_car(self, input):
        return Team.infer(self.models[0], input)

    def infer_car2(self, input):
        if len(self.models) > 1:
            return Team.infer(self.models[1], input)
        else:
            return self.infer_car(input)

    def serialize(self):
        return {
            "name": self.team_name,
            "id": self.id.hex,
            "hasTwoModels": len(self.models) > 1
        }


    @staticmethod
    def load_model(model_filename):
        # return keras.models.load_model(f"/nets/{model_filename}")
        return model_filename
        
        

    @staticmethod
    def infer(model: keras.Model, input):
        # return model.predict(input)
        return 0



