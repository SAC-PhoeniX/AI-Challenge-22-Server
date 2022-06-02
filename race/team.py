from typing import Union
import uuid
from aiohttp import web

from .car import Car

class Team:

    def __init__(self, name, team_config):
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

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "id": self.id.hex,
            "color": self.color,
            "details": self.details,
            "cars": [car.serialize() for car in self.cars]
        }

