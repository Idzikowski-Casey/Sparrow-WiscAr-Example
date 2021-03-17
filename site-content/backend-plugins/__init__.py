from sparrow.plugins import SparrowPlugin
from sparrow.context import app_context
from sparrow.util import relative_path
from starlette.routing import Route, Router
from starlette.responses import JSONResponse
import pandas as pd
from pathlib import Path
import json


class MetricsEndpointWiscAr(SparrowPlugin):
    '''
        This Sparrow Plugin adds a GET route to the API. 
        It works by reading in a postgreSQL query from a 
        file in this directory, querying the sparrow 
        database, and then returning the response a JSON.

        It then uses the on_api_initialized_v2 hook to add the route
        and some route documentation that shows up on the api.
    '''
    name = 'metrics'

    def metrics_view(self):

        db = self.app.database
        p = Path(relative_path(__file__, "metrics.sql"))
        sqlfile = open(p, "r")
        query = sqlfile.read()

        metrics = db.exec_query(query)
        res = metrics.to_json(orient='records')

        return JSONResponse(json.loads(res))

    def on_api_initialized_v2(self, api):

        root_route = "Lab Plugins"
        basic_info = dict(
            route = "/metrics",
            description = "A metrics route for WiscAr Lab",
        )
        api.add_route("/metrics", self.metrics_view(), methods=['GET'], include_in_schema=False)
        api.route_descriptions[root_route].append(basic_info)


class AddNewTable(SparrowPlugin):
    '''
        This plugin's purpose is to create a new table in the database.

        An example of how a lab can add a table for unqiue data models.
        TODO: How does this then get added to the api?
    '''
    name = 'favorite-rock'

    def on_database_ready(self, db):

        p = Path(relative_path(__file__, "favorite_rock.sql"))
        db.exec_sql(p)
