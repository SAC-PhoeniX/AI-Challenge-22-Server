from aiohttp import web
from aiohttp.web import Request, Response
from aiohttp_sse import sse_response

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

    @routes.get("/stream/info/{race_id}")
    async def info(req: Request):
        stats = race.stats.get_stats_by_id(req.match_info["race_id"])
        async with sse_response(req) as res:
            await stats.subscribe(["all"], res)
        return res

    @routes.put("/telemetry/qual")
    async def start_qual(req: Request):
        d = await req.json()
        car = race.get_car_with_id(d["car_id"])
        
        return web.json_response({
            "id": race.stats.start(
                race.circuits[verify_circuit_id(race, d["circuit"])],
                {car.team.get_id(): car.team},
                {car.get_id(): car}
            ).get_id()}, 
            dumps=dump_utf8
        )
    
    @routes.post("/telemetry/{race_id}")
    async def update_stats(req: Request):
        d = await req.json()
        event = d["event"] or "all"

    return routes


