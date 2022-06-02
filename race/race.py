from uuid import UUID

from .team import Team
from .car import Car
from .circuit import Circuit

class Race:
    def __init__(self, teams, circuit_number=6):
        self.teams: dict[UUID, Team] = {team.id: team for team in teams}
        self.cars: dict[UUID, Car] = {
            car.id:car for team in self.teams.values() for car in team.cars
        }
        self.circuits: list[Circuit] = [Circuit(i) for i in range(circuit_number)]


    def get_team_with_id(self, team_id) -> Team:
        if type(team_id) is str:
            team_id = UUID(team_id)

        if team_id in self.teams:
            return self.teams[team_id]
        else:
            raise "Team not found"

    def get_car_with_id(self, car_id) -> Car:
        if type(car_id) is str:
            car_id = UUID(car_id)

        if car_id in self.cars:
            return self.cars[car_id]
        else:
            raise "Car not found"
