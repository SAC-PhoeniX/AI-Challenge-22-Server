from typing import List
import uuid
from aiohttp import web
from aiohttp.web import Request

from ai.team import Team


def team_routes(t: List[Team]) -> web.RouteTableDef:
    TEAMS = t

    routes = web.RouteTableDef()

    @routes.get("/teams")
    async def teams(request: Request):
        return web.json_response({
            "count": len(TEAMS),
            "teams": [team.serialize() for team in TEAMS]
        })

    @routes.get("/team/name/{name}")
    async def team(request: Request):
        name = request.match_info["name"]
        return web.json_response(
            [team.serialize() for team in TEAMS if team.team_name == name]
        )

    @routes.get("/team/id/{id}")
    async def team(request: Request):
        id = uuid.UUID(request.match_info["id"])
        return web.json_response(
            [team.serialize() for team in TEAMS if team.id == id]
        )

    @routes.post("/infer/{team_name}/{car_id}")
    async def infer(request: Request):
        team_name = request.match_info["team_name"]
        found_teams = [team for team in TEAMS if team.team_name == team_name]
        if len(found_teams) != 1:
            raise web.HTTPBadRequest("Team not found")
        team = found_teams[0]

        car_id = request.match_info["car_id"]
        if car_id != "0" and car_id != "1":
            raise web.HTTPBadRequest("Bad car ID")
        car_id = int(car_id)

        

        print(f"asked for car #{car_id} of team {team_name}")
        raise web.HTTPNotImplemented()

    return routes