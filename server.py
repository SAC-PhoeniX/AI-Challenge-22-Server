from os import environ

NO_TF = environ.get("MODELS", "TF") == "NO_TF"
if not NO_TF:
    import tensorflow as tf

from aiohttp import web
from utils import read_config
from routes import info_routes, circuits_routes, infer_routes
from race import Team, Race

config = read_config(".conf")
teams = [
            Team(name, info)
            for name, info
            in config["TEAMS"].items()
        ]
RACE = Race(teams)

app = web.Application()
app.add_routes([
    *info_routes(RACE),
    *circuits_routes(RACE),
    *infer_routes(RACE)
    ])

web.run_app(app)



