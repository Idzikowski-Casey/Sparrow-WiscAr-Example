# Sparrow Example Implementation (WiscAr db)

This is an implementation of sparrow for the WiscAr Lab. This can be used as an example for creating
customized frontend and backend plugins for individual lab's instances of sparrow.

Customization depends heavily on the environmental variables a lab defines in it's `sparrow-config.sh` and `sparrow-config.overrides.sh`. It is within these files where you define directories for frontend and backend plugins.

```
export SPARROW_PLUGIN_DIR="$PROJECT_DIR/site-content/backend-plugins"
export SPARROW_SITE_CONTENT="$PROJECT_DIR/site-content"
```

`SPARROW_PLUGIN_DIR` is the directory where sparrow will search for Backend plugins. `SPARROW_SITE_CONTENT` is the directory where sparrow will get frontend plugins from.

## Frontend plugin development and deployment:

Sparrow frontend plugins are written in javascript or must be exportable from a javascript file and compilable on the browser. All plugins should be exported as part of a single default export object with a specific key. The keys are predefined and correspond to a specific place where the plugin will appear on the U.I. List of plugin id's yet to come.

In the internal codebase of Sparrow, frontend plugins are created by using `Frames`. These `Frames` grab the external component by the `id` and renders them. Most Sparrow plugins need to be react elements but some are javascript data objects (i.e `mapStyles` is a list of objects with key value pairs corresponding to the mapstyle name that will appear and a valid mapbox style).

Most plugins are also set up to recieve `props` and is often model data (i.e the plugin for `projectPage` gets the project data for each specific project). The best way to develop external plugins is to begin small, make sure you can get something rendering in the correct spot and then layer complexity on top.

## Backend plugin development and deployment:

Sparrow backend plugins are developed a bit differently from frontend ones. All Sparrow plugins should be created as python classes that inherit `SparrowPlugin`.

```
from sparrow.plugins import SparrowPlugin

class TestPlugin(SparrowPlugin):
```

Sparrow plugins are read into sparrow during app building (every `sparrow up`). But Sparrow also uses hooks to perform different actions. For instance if you want to create an API plugin this would be done under the `on_api_initialized_v2` hook.

```
class MetricsEndpoint(SparrowPlugin):
    name = 'metrics'

    def on_api_initialized_v2(self, api):

        root_route = "Lab Plugins"
        basic_info = dict(
            route = "/metrics",
            description = "A metrics route for My Lab",
        )
        api.add_route("/metrics", metrics_view(), methods=['GET'], include_in_schema=False)
        api.route_descriptions[root_route].append(basic_info)
```

In this example, I have defined a `MetricsEndpoint` class that has one method `on_api_initialized_v2`. In this function I am adding a new route to the api using `add_route()` and I am also appending the API documentation by appending `basic_info` to `route_descriptions`.

There are similar hooks for working on the database:

- `on_database_ready`
- `on_load_complete`

These hooks can be used to load data into the database, to add tables and views to the database, create new users, etc.

## Sparrow Configuration

The `sparrow-config.sh` file in this repository contains configuration for WiscAr's
version of Sparrow. It will be automatically sourced anytime you run `sparrow`
in this repository's directory or a subdirectory.
You will need to create a file `sparrow-config.overrides.sh` in this directory
containing application secrets:

```
export MAPBOX_API_TOKEN=<your-api-token>
export SPARROW_SECRET_KEY=<example>
```

You can also override other Sparrow environment variables in this file.

### Restoring from a database dump

The state of an existing Sparrow installation can be restored using the command
`sparrow db-import <your-database.pg-dump>`.
