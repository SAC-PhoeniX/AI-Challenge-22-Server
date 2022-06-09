from aiohttp import ClientSession
import asyncio

base = "http://localhost:8080"

async def main():
    async with ClientSession() as session:
        async with session.get(base + "/cars") as res:
            ids = [car["id"] for car in (await res.json())["cars"]]
            for time,car_id in zip(range(len(ids)), ids):
                await session.post(base + "/circuits/1/qual/" + car_id, data='{"laptime": ' + str((1+time)/10) + '}')
            print()

asyncio.run(main())