import aiohttp.web
from aiohttp_sse import EventSourceResponse
from asyncio import Queue, gather
from weakref import WeakSet
from functools import partial
from json import dumps
from typing import TYPE_CHECKING

dump_utf8 = partial(dumps, ensure_ascii=False)

if TYPE_CHECKING:
    from .race import Race


class Subscribable:
    def __init__(self):
        self.streams: WeakSet[EventSourceResponse] = WeakSet()
        self.subscribers: set[Queue] = set()
        self.state = {}

    # mostly stolen from https://github.com/aio-libs/aiohttp-sse/blob/master/examples/chat.py
    async def subscribe(self, response: EventSourceResponse):
        q = Queue()
        self.subscribers.add(q)
        self.streams.add(response)
        try:
            await self.send_state(response)
            while not response.task.done():
                payload = await q.get()
                await response.send(dump_utf8(payload))
                q.task_done()
        finally:
            self.subscribers.discard(q)
            self.streams.discard(response)

    async def send_state(self, response):
        await response.send(dump_utf8({"event": "initial", "state": self.state}))

    def update_state(self, data, *args, **kwargs):
        self.state.update(data)
        pass

    async def update(self, data, *args, **kwargs):
        self.update_state(data)
        await gather(*[
            q.put(data)
            for q
            in self.subscribers
        ])

    async def clean_streams(self):
        waiters = []
        for stream in self.streams:
            stream.stop_streaming()
            waiters.append(stream.wait())

        await gather(*waiters)
        self.streams.clear()


class RaceStats(Subscribable):
    def __init__(self, race: "Race"):
        super().__init__()
        self.race = race
        self.log = []

    async def update(self, data, car_id=None, *args, **kwargs):
        if not car_id:
            raise aiohttp.web.HTTPBadRequest

        # save everything that happens
        self.log.append({car_id: data})
        self.update_state(data, car_id)
        await gather(*[
            q.put({car_id: data})
            for q
            in self.subscribers
        ])


class QualStats(RaceStats):
    def __init__(self, race: "Race"):
        super().__init__(race)
        self.state = {car_id: {"timer": 0, "speed": 0} for car_id in race.cars.keys()}

    def update_state(self, data, car_id=None, *args, **kwargs):
        self.state[car_id].update(data)


class GrandPrixStats(RaceStats):
    def __init__(self, race: "Race"):
        super().__init__(race)
        self.state = {car_id: {"finish": {}, "lap": {}, "live": {}} for car_id in race.cars.keys()}

    def update_state(self, data, car_id=None, *args, **kwargs):
        self.state[car_id][data["event"]].update(data)


class Stats(Subscribable):
    def __init__(self, race: "Race"):
        super().__init__()
        self.quals: list[QualStats] = [QualStats(race) for _ in race.circuits]
        self.gps: list[GrandPrixStats] = [GrandPrixStats(race) for _ in race.circuits]
        self.state = ""
        pass

    async def clean_all_streams(self):
        await gather(
            self.clean_streams(),
            *[stats.clean_streams() for stats in self.quals],
            *[stats.clean_streams() for stats in self.gps]
        )

    def update_state(self, data, *args, **kwargs):
        self.state = data

    async def send_state(self, response):
        await response.send(self.state)

    async def update(self, data, *args, **kwargs):
        if data != self.state:
            await super().update(data)
