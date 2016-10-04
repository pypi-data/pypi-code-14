import json, requests

class SwaggerFileNotFoundError(FileNotFoundError):
    pass

def get_swagger_data(swagger_location):
    try:
        return {
            "swagger_data": json.load(open(swagger_location, encoding="utf-8")),
            "swagger_file": swagger_location
        }

    except (FileNotFoundError, OSError):
        try:
            return {
                "swagger_data": requests.get(swagger_location).json(),
                "swagger_uri": swagger_location
            }

        except (requests.ConnectionError, json.JSONDecodeError):
            raise SwaggerFileNotFoundError(
                "Swagger file not found at %s" % swagger_location
            )

def rstjinja(app, docname, source):
    source[0] = app.builder.templates.render_string(
        source[0], get_swagger_data(app.config.swagger2sphinx_swagger_location)
    )

def setup(app):
    app.add_config_value("swagger2sphinx_swagger_location", None, "")
    app.connect("source-read", rstjinja)
    return {"version": "0.1.3"}
