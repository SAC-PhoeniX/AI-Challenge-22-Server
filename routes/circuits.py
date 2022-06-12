from aiohttp import web
from aiohttp.web import HTTPBadRequest, json_response, Request, Response

from utils import dump_utf8
from race.race import Race

def verify_circuit_id(race, id_str):
    # circuits are 1-indexed in the game
    circuit_id = int(id_str) - 1
    if circuit_id > len(race.circuits) or circuit_id < 0:
        raise HTTPBadRequest()
    return circuit_id

def get_routes(race: Race) -> web.RouteTableDef:
    routes = web.RouteTableDef()

    @routes.get("/circuits/{circuit_id}/grid")
    async def get_grid(request: Request):
        return json_response(race.circuits[verify_circuit_id(race, request.match_info["circuit_id"])].get_grid(), dumps=dump_utf8)

    @routes.post("/circuits/{circuit_id}/qual/{car_id}")
    async def save_time(request: Request):
        race.circuits[verify_circuit_id(race, request.match_info["circuit_id"])].update_time(
            request.match_info["car_id"],
            (await request.json())["laptime"]
        )

        return Response()

    return routes