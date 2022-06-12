from uuid import UUID

from .team import Team
from .car import Car
from .circuit import Circuit
from .stats import Stats
from .race_object import RaceObject


class Race(RaceObject):
    def __init__(self, teams, circuit_number=6):
        super().__init__()
        self.teams: dict[str, Team] = {team.get_id(): team for team in teams}
        self.cars: dict[str, Car] = {
            car.get_id():car for team in self.teams.values() for car in team.cars
        }
        self.circuits: list[Circuit] = [Circuit(i) for i in range(circuit_number)]

        self.stats = Stats()
        

    def get_team_with_id(self, team_id: str) -> Team:
        if team_id in self.teams:
            return self.teams[team_id]
        else:
            raise "Team not found"

    def get_car_with_id(self, car_id) -> Car:
        if car_id in self.cars:
            return self.cars[car_id]
        else:
            raise "Car not found"
