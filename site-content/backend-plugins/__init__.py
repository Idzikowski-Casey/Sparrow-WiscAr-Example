from sparrow.plugins import SparrowPlugin
from sparrow.context import app_context
from sparrow.util import relative_path
from starlette.routing import Route, Router
from starlette.responses import JSONResponse
import pandas as pd
from pathlib import Path
import json


def metrics_view():

    db = app_context().database

    p = Path(relative_path(__file__, "metrics.sql"))
    sqlfile = open(p, "r")
    query = sqlfile.read()

    test = pd.read_sql(query, db.engine.connect())
    
    res = test.to_json(orient='records')

    return JSONResponse(json.loads(res))

class MetricsEndpointWiscAr(SparrowPlugin):
    name = 'metrics'

    def on_api_initialized_v2(self, api):

        root_route = "Lab Plugins"
        basic_info = dict(
            route = "/metrics",
            description = "A metrics route for WiscAr Lab",
        )
        api.add_route("/metrics", metrics_view(), methods=['GET'], include_in_schema=False)
        api.route_descriptions[root_route].append(basic_info)

