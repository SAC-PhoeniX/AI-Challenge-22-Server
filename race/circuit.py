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
            car_id: reduce(
                lambda prev, cur: prev + 1 if cur[0] < time or (cur[0] == time and cur[1] < i) else prev, zip(self.cars.values(), count(0, 1)), 0
            )
            for (i, (car_id, time))
            in zip(count(0,1), self.cars.items())
        }

if __name__ == "__main__":
    from pprint import pprint

    c = Circuit(1)
    c.update_time("def", 2)
    c.update_time("gkhj", 3)
    c.update_time("abc", 1.2)
    pprint(c.get_grid())