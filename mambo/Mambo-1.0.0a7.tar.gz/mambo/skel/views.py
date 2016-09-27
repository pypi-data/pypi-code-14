"""
Mambo

Views

"""
from mambo import (Mambo, page_meta, get_config, flash_success, flash_error,
                   abort, request, url_for, redirect, models,
                   # decorators
                   nav_menu, get, post, render_json)

# ------------------------------------------------------------------------------


class Index(Mambo):

    @nav_menu("Home", order=1)
    def index(self):
        page_meta(title="Hello View!")
        return {}

    @get("/hello-json/")
    @render_json
    def hello(self):
        return {"Hello": "World"}


