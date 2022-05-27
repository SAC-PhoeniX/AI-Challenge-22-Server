from typing import List
import uuid
from aiohttp import web
from aiohttp.web import Request
import json

from ai.team import Team

def dump_utf8(data, **kwargs):
    return json.dumps(data, **kwargs, ensure_ascii=False)

def team_routes(TEAMS: List[Team]) -> web.RouteTableDef:

    routes = web.RouteTableDef()

    @routes.get("/teams")
    async def teams(request: Request):
        return web.json_response({
            "count": len(TEAMS),
            "teams": [team.serialize() for team in TEAMS]
        }, dumps=dump_utf8)

    @routes.get("/team/name/{name}")
    async def team(request: Request):
        name = request.match_info["name"]
        return web.json_response(
            [team.serialize() for team in TEAMS if team.team_name == name], dumps=dump_utf8
        )

    @routes.get("/team/id/{id}")
    async def team(request: Request):
        id = uuid.UUID(request.match_info["id"])
        return web.json_response(
            [team.serialize() for team in TEAMS if team.id == id], dumps=dump_utf8
        )

    @routes.post("/infer/{team_id}/{car_id}")
    async def infer(request: Request):
        team_id = request.match_info["team_id"]
        found_teams = [team for team in TEAMS if team.id.hex == team_id]
        if len(found_teams) != 1:
            raise web.HTTPBadRequest()
        team = found_teams[0]

        car_id = request.match_info["car_id"]
        if car_id != "0" and car_id != "1":
            raise web.HTTPBadRequest()
        car_id = int(car_id)

        print(f"asked for car #{car_id} of team {team_id}")
        
        
        inp = (await request.post()).get("rays")
        return web.json_response(team.infer_car(inp, car_id), dumps=dump_utf8)

    return routes
