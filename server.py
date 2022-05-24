from aiohttp import web
import tensorflow as tf

from ai.team import Team
from config import read_config
from routes import team_routes

config = read_config(".conf")
teams = [
            Team(name,info["color"],info["details"],info["models"])
            for name, info
            in config["TEAMS"].items()
        ]


app = web.Application()
app.add_routes(team_routes(teams))

web.run_app(app)



