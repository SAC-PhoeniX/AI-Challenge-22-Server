from typing import List
import uuid
from aiohttp import web
from ai.model import Model

class Team:
    team_name: str
    models: [Model]
    id: uuid.UUID

    color: str
    details: str

    def __init__(self, team_name: str, color: str, details: str, models_info) -> None:
        self.team_name = team_name
        self.color = color
        self.details = details

        self.models = [
                Model( mi["model_file"], mi.get("name", ""))
                for mi
                in models_info
            ]
        self.id = uuid.uuid4()

        pass

    def infer_car(self, inp, car_id):
        return self.infer_car0(inp) if car_id == 0 else self.infer_car1(inp)

    def infer_car0(self, inp):
        return self.models[0].infer(inp)

    def infer_car1(self, inp):
        if len(self.models) > 1:
            return self.models[1].infer(inp)
        else:
            return self.infer_car0(inp)

    def serialize(self):
        return {
            "name": self.team_name,
            "id": self.id.hex,
            "color": self.color,
            "details": self.details,
            "hasTwoModels": len(self.models) > 1,
            "models": [dict(**model.serialize(), id=i) for i, model in enumerate(self.models)]
        }

        