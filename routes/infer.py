import json
import uuid
from typing import List, Tuple

from aiohttp import web
from aiohttp.web import Request, json_response

from race import Race
from utils import dump_utf8


def get_routes(race: Race) -> web.RouteTableDef:

    routes = web.RouteTableDef()

    @routes.post("/infer/team/{team_id}/{car_number}")
    async def infer(request: Request):
        i = request.match_info
        try:
            team = race.get_team_with_id(i["team_id"])
            inp = (await request.json())["rays"]
            return json_response(team.infer_car(inp, i["car_number"]), dumps=dump_utf8)
        except KeyError:
            raise  web.HTTPBadRequest()


    @routes.post("/infer/car/{car_id}")
    async def infer(request: Request):
        i = request.match_info
        try:
            car = race.get_car_with_id(i["car_id"])
            inp = (await request.json())["rays"]
            return json_response(car.infer(inp), dumps=dump_utf8)
        except KeyError:
            raise  web.HTTPBadRequest()
    

    @routes.post("/infer/cars")
    async def infer(request: Request):
        return json_response({
            car_id: race.get_car_with_id(car_id).infer(inp) for car_id, inp in (await request.json()).items()
        }, dumps=dump_utf8)

    return routes


