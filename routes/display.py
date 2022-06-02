from aiohttp import web
from aiohttp.web import HTTPBadRequest, json_response, Request, Response


from utils import dump_utf8
from race.race import Race

def get_routes(race: Race) -> web.RouteTableDef:
    routes = web.RouteTableDef()



    return routes