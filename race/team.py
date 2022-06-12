from typing import Union
import uuid
from aiohttp import web

from .car import Car
from .race_object import RaceObject

class Team(RaceObject):

    def __init__(self, name, team_config):
        super().__init__()

        self.name: str = name
        self.color: str = team_config["color"]
        self.details: str = team_config.get("details", "")

        self.cars: list[Car] = [
            Car(self, car.get("name", None), car["model_file"])
            for car in team_config["cars"]
        ]
        self.id: UUID = uuid.uuid4()

        pass

    def infer_car(self, inp: list, car_id: Union[str, int]):
        car_id = int(car_id)
        if car_id != 0 and car_id != 1:
            raise Error("Bad car ID")
        return self.cars[car_id].infer(inp)

    def serialize(self, include_cars) -> dict:
        obj = {
            "name": self.name,
            "id": self.get_id(),
            "color": self.color,
            "details": self.details
        }

        if include_cars:
            obj["cars"] = [car.serialize(False) for car in self.cars]

        return obj

