from itertools import count
from functools import reduce

class Circuit:
    def __init__(self, id):
        self.id = id
        self.cars: dict[str, float] = {}


    def update_time(self, car_id, time):
        self.cars[car_id] = time

    def get_grid(self):
        return {
            "cars": sorted([{"id": car_id, "time": time} for car_id, time in self.cars.items()], key=lambda el: el["time"])
        }

if __name__ == "__main__":
    from pprint import pprint

    c = Circuit(1)
    c.update_time("def", 2)
    c.update_time("gkhj", 3)
    c.update_time("abc", 1.2)
    pprint(c.get_grid())