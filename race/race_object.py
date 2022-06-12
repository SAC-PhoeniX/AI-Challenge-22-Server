from uuid import uuid4

class RaceObject:
    def __init__(self):
        self.id = uuid4()

    def get_id(self) -> str:
        return self.id.hex