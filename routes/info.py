from typing import List, Tuple
import uuid
from aiohttp import web
from aiohttp.web import Request
import json

from utils import dump_utf8
from race import Race



def get_routes(race: Race) -> web.RouteTableDef:

    routes = web.RouteTableDef()

    @routes.get("/cars")
    async def cars(request: Request):
        return web.json_response({
            "count": len(race.cars),
            "cars": [car.serialize(True) for car in race.cars.values()]
        }, dumps=dump_utf8)

    @routes.get("/car/{id}")
    async def car(request: Request):
        car = race.get_car_with_id(request.match_info["id"])
        return web.json_response(
            car.serialize(True), dumps=dump_utf8
        )

    @routes.get("/teams")
    async def teams(request: Request):
        return web.json_response({
            "count": len(race.teams),
            "teams": [team.serialize(True) for team in race.teams.values()]
        }, dumps=dump_utf8)

    @routes.get("/team/{id}")
    async def team(request: Request):
        team = race.get_team_with_id(request.match_info["id"])
        return web.json_response(
            team.serialize(True), dumps=dump_utf8
        )

    return routes


