from uuid import uuid4
from hashlib import sha1

class RaceObject:
    def __init__(self):
        self.id = self.__class__.generate_id()

    @staticmethod
    def generate_id(string: str=None):
        if not string:
            return uuid4().hex
        else: 
            return sha1(string.encode("utf-8")).hexdigest()

    def get_id(self) -> str:
        return self.id