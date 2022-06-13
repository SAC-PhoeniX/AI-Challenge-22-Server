from aiohttp_sse import EventSourceResponse
from asyncio import Queue, gather
from weakref import WeakSet
from functools import partial
from json import dumps
from typing import TYPE_CHECKING

dump_utf8 = partial(dumps, ensure_ascii=False)

if TYPE_CHECKING:
    from .race import Race


# runs when race telemetry begins
class RaceStats:
    def __init__(self, race: "Race"):
        self.race = race
        self.streams: WeakSet[EventSourceResponse] = WeakSet()
        self.subscribers: set[Queue] = set()
        self.state = {}
        self.log = []

    # mostly stolen from https://github.com/aio-libs/aiohttp-sse/blob/master/examples/chat.py
    async def subscribe(self, response: EventSourceResponse):
        q = Queue()
        self.subscribers.add(q)
        self.streams.add(response)
        try:
            await response.send(dump_utf8({"event": "initial", "state": self.state}))
            while not response.task.done():
                payload = await q.get()
                await response.send(dump_utf8(payload))
                q.task_done()
        finally:
            self.subscribers.discard(q)
            self.streams.discard(response)

    async def update(self, data):
        # save everything that happens
        self.log.append(data)
        self.update_state(data)
        await gather(*[
            q.put(data)
            for q
            in self.subscribers
        ])

    def update_state(self, data):
        pass

    async def end(self):
        # race ends
        waiters = []
        for stream in self.streams:
            stream.stop_streaming()
            waiters.append(stream.wait())
        await gather(*waiters)


class QualStats(RaceStats):
    def __init__(self, race: "Race"):
        super().__init__(race)
        self.state = {car_id: {"timer": 0, "speed": 0} for car_id in race.cars.keys()}

    def update_state(self, data):
        self.state[data["car_id"]].update(data)


class GrandPrixStats(RaceStats):
    pass


class Stats:
    def __init__(self, race: "Race"):
        self.quals: list[QualStats] = [QualStats(race) for _ in race.circuits]
        self.gps: list[GrandPrixStats] = [GrandPrixStats(race) for _ in race.circuits]
        pass

    
