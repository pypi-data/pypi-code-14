from flask_debugtoolbar import DebugToolbarExtension


def debug_toolbar_feature(app):
    """
    Debug toolbar
    """
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
