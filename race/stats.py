from .circuit import Circuit
from .team import Team
from .car import Car
from uuid import UUID, uuid4
from aiohttp_sse import EventSourceResponse
from asyncio import Queue, gather
from weakref import WeakSet
from .race_object import RaceObject
from functools import partial
from json import dumps

dump_utf8 = partial(dumps, ensure_ascii=False)

# runs when race telemetry begins
class RaceStats(RaceObject):
    def __init__(self, events: list[str], circuit: Circuit, teams: dict[str, Team], cars: dict[str, Car]):
        super().__init__()
        self.streams: WeakSet[EventSourceResponse] = WeakSet()
        self.subscribers: dict[str, set[Queue]] = {event_name: set() for event_name in events}
        self.states = {event_name: {} for event_name in events}
        self.log = []


    # mostly stolen from https://github.com/aio-libs/aiohttp-sse/blob/master/examples/chat.py
    async def subscribe(self, events: list[str], response: EventSourceResponse):
        q = Queue()
        multiple_events = len(events) != 1
        self.streams.add(response)

        for event in events:
            if event in self.subscribers: self.subscribers[event].add(q)
        
        try:
            # send initial state
            await response.send(dump_utf8(self.states))
            while not response.task.done():
                payload = await q.get()
                await response.send(dump_utf8(payload))
                q.task_done()
        finally:
            for event in events:
                if event in self.subscribers: self.subscribers[event].remove(q)
            self.streams.discard(response)


    # race is happening
    async def update(self, event, data):
        # save everything that happens
        self.log.append({"event": event, "data": data})
        if event not in self.subscribers:
            raise Exception("Incorrect event: " , event)
        await self.subscribers[event].add(data)


    async def end(self):
        # race ends
        waiters = []
        for stream in self.streams:
            stream.stop_streaming()
            waiters.append(stream.wait())
        await gather(*waiters)


class QualStats(RaceStats):
    pass

class GrandPrixStats(RaceStats):
    pass

class Stats:
    def __init__(self):
        self.current_races = {}
        self.previous_races =  {}
        pass


    def start(self, circuit: Circuit, teams: dict[str, Team], cars: dict[str, Car], events=["all"]):
        stat = RaceStats(events, circuit, teams, cars)
        self.current_races[stat.get_id()] = stat
        return stat


    def get_stats_by_id(self, race_id) -> RaceStats:
        if race_id in self.previous_races:
            raise Exception("Old race requested")
        if race_id not in self.current_races:
            raise Exception("Race not found")
        
        return self.current_races[race_id]

    def save(self):
        self.previous_races.insert(0, 
            self.serialize()
        )
        
        pprint(self.previous_races)

    def serialize(self, race_idx):
        if race_idx == -1:
            if not self.cars:
                return {}
            else:
                return {
                    cars: list(self.cars.items())
                }
        else: return self.previous_races[race_idx]