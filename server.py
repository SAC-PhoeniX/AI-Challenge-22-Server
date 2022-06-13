from os import environ

NO_TF = environ.get("MODELS", "TF") == "NO_TF"
if not NO_TF:
    import tensorflow as tf

from aiohttp import web
from utils import read_config
from routes import info_routes, circuits_routes, infer_routes, stream_routes
from race import Team, Race

config = read_config(".conf")
teams = [
            Team(name, info)
            for name, info
            in config["TEAMS"].items()
        ]
RACE = Race(teams)


async def clean_streams(_):
    await RACE.stats.clean_all_streams()

app = web.Application()
app.on_shutdown.append(clean_streams)

app.add_routes([
    *info_routes(RACE),
    *circuits_routes(RACE),
    *infer_routes(RACE),
    *stream_routes(RACE),
    ])

web.run_app(app)



