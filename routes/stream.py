from aiohttp import web
from aiohttp.web import Request, Response
from aiohttp_sse import sse_response

from race.stats import RaceStats
from utils import dump_utf8
from race import Race
from os.path import exists

from .circuits import verify_circuit_id


def get_routes(race: Race) -> web.RouteTableDef:
    routes = web.RouteTableDef()
    if exists("stream/dist"):
        print("Serving stream files")
        routes.static("/obs", "stream/dist")
    else:
        print("Stream files not found")

    @routes.get("/stream/races")
    async def race_index(req: Request):
        return web.json_response({
            "races": list(race.stats.current_races.keys())
        }, dumps=dump_utf8)

    @routes.get("/stream/info/{race_type}/circuit/{circuit_id}")
    async def info(req: Request):
        s: dict[str, RaceStats]
        if req.match_info["race_type"] == "qual":
            s = race.stats.quals
        elif req.match_info["race_type"] == "race":
            s = race.stats.gps
        else:
            return web.HTTPBadRequest()
        stats = s[verify_circuit_id(race, req.match_info["circuit_id"])]
        async with sse_response(req) as res:
            await stats.subscribe(res)
        return res

    @routes.post("/telemetry/{race_type}/circuit/{circuit_id}/car/{car_id}")
    async def update_stats(req: Request):
        s: dict[str, RaceStats]
        if req.match_info["race_type"] == "qual":
            s = race.stats.quals
        elif req.match_info["race_type"] == "race":
            s = race.stats.gps
        else:
            return web.HTTPBadRequest()
        data = await req.json()
        data["car_id"] = req.match_info["car_id"]
        await s[verify_circuit_id(race, req.match_info["circuit_id"])].update(data)

        return web.HTTPOk()

    return routes
