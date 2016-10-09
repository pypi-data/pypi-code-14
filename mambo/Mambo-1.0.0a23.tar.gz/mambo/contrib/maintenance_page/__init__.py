
from mambo import Mambo, get_config, register_package, abort

register_package(__package__)

__version__ = "1.0.0"

def main(**kwargs):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    m = maintenance_view()

    :param template_: The directory containing the view pages
    :return:
    """

    template = "MaintenancePage/index.html"

    class MaintenancePage(Mambo):

        @classmethod
        def _register(cls, app, **kw):

            super(cls, cls)._register(app, **kw)

            @app.before_request
            def on_maintenance():
                return cls.render(_layout=template), 503

    return MaintenancePage
