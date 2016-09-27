"""
MamboAdmin
"""
from mambo import Mambo, register_package

register_package(__package__)

__version__ = "1.0.0"

def main(**kwargs):

    decorators = kwargs.get("decorators", [])
    options = kwargs.get("options", {})

    Mambo.g(MAMBO_ADMIN_BRAND=options.get("brand", "Admin"),
            MAMBO_ADMIN_THEME=options.get("theme", "yeti"))
    Mambo.base_layout = "MamboAdmin/layout.html"
    if decorators:
        Mambo.decorators += decorators





