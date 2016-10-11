"""
Mambo

"""

import re
import os
import sys
import inspect
import datetime
import functools
import logging
import logging.config
import copy
from six import string_types
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter, parse_rule
from werkzeug import import_string
from flask import (Flask, g, render_template, flash, session, make_response,
                   Response, request, abort,
                   url_for as f_url_for, redirect as f_redirect)
from flask_assets import Environment
import jinja2
from importlib import import_module
from . import utils
from .__about__ import *

from sqlalchemy.engine.url import make_url as sa_make_url
import active_alchemy

_py2 = sys.version_info[0] == 2
# ------------------------------------------------------------------------------

__all__ = [
            "Mambo",
            "MamboInit",
            "db",
            "models",
            "views",
            "get_env",
            "set_env",
            "get_app_env",
            "get_env_config",
            "get_config",
            "page_meta",
            "flash_success",
            "flash_error",
            "flash_info",
            "flash_data",
            "get_flash_data",
            "init_app",
            "register_package",
            "register_models",
            "abort",
            "redirect",
            "url_for",

            # For convenience when importing from mambo, but can use
            # the flask one
            "flash",
            "session",
            "request",

            # Not sure why it's there
            "import_module",
           ]


# Will hold all active class views
# It can be used for redirection etc
# ie: redirect(views.ContactPage.index)
views = type('', (), {})

# Will hold models from apps, or to be shared
# ie, set new model property -> models.MyNewModel = MyModel
# ie: use property -> models.MyNewModel.all()
# For convenience, use `register_models(**kw)` to register the models
# By default mambo will load all the application/models.py models
models = type('', (), {})


def register_models(**kwargs):
    """
    Alias to register model
    :param kwargs:
    :return:
    """
    [setattr(models, k, v) for k, v in kwargs.items()]


# Hold the current environment
__ENV__ = None


def set_env(env):
    """
    Set the envrionment manually
    :param env:
    :return:
    """
    global __ENV__
    __ENV__ = env.lower().capitalize()


def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str Capitalized
    """
    if not __ENV__:
        env = os.environ["env"] if "env" in os.environ else "Development"
        set_env(env)
    return __ENV__


def get_app_env():
    """
    if the app and the envi are passed in the command line as 'app=app:env'
    :return: tuple app, env
    """
    app, env = None, get_env()
    if "app" in os.environ:
        app = os.environ["app"].lower()
        if ":" in app:
            app, env = os.environ["app"].split(":", 2)
            set_env(env)
    return app, env


def get_env_config(config):
    """
    Return config class based based on the config
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())


def init_app(kls):
    """
    To bind middlewares, plugins that needs the 'app' object to init
    Bound middlewares will be assigned on cls.init()
    """
    if not hasattr(kls, "__call__"):
        raise exceptions.MamboError("init_app: '%s' is not callable" % kls)
    Mambo._init_apps.add(kls)
    return kls


def register_package(pkg):
    """
    Allow to register an app packages by loading and exposing: templates, static,
    and exceptions for abort()

    Structure of package
        root
            | $package_name
                | __init__.py
                |
                | /templates
                    |
                    |
                |
                | /static
                    |
                    | assets.yml

    :param pkg: str - __package__
                    or __name__
                    or The root dir
                    or the dotted resource package (package.path.path,
                    usually __name__ of templates and static
    """

    root_pkg_dir = pkg
    if not os.path.isdir(pkg) and "." in pkg:
        root_pkg_dir = utils.get_pkg_resources_filename(pkg)

    template_path = os.path.join(root_pkg_dir, "templates")
    static_path = os.path.join(root_pkg_dir, "static")

    logging.info("Registering App: " + pkg)
    if os.path.isdir(template_path):
        template_path = jinja2.FileSystemLoader(template_path)
        Mambo._template_paths.add(template_path)

    if os.path.isdir(static_path):
        Mambo._static_paths.add(static_path)
        Mambo._add_asset_bundle(static_path)


def get_config(key, default=None):
    """
    Shortcut to access the application's config in your class
    :param key: The key to access
    :param default: The default value when None
    :returns mixed:
    """
    return Mambo._app.config.get(key, default)


def page_meta(**kwargs):
    """
    Meta allows you to add page meta data
    :params **kwargs:

    meta keys we're expecting:
        title (str)
        description (str)
        url (str) (Will pick it up by itself if not set)
        image (str)
        site_name (str) (but can pick it up from config file)
        object_type (str)
        keywords (list)
        locale (str)
        card (str)

        **Boolean By default these keys are True
        use_opengraph
        use_twitter
        use_googleplus
python
    """
    meta = Mambo._global.get("__META__", {})
    meta.update(**kwargs)
    Mambo.g(__META__=meta)


def flash_success(msg):
    """
    Alias to flash, but set a success message
    :param msg:
    :return:
    """
    return flash(msg, "success")


def flash_error(msg):
    """
    Alias to flash, but set an error message
    :param msg:
    :return:
    """
    return flash(msg, "error")


def flash_info(msg):
    """
    Alias to flash, but set an info message
    :param msg:
    :return:
    """
    return flash(msg, "info")


def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session["_flash_data"] = data


def get_flash_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop("_flash_data", None)


is_method = lambda x: inspect.ismethod if _py2 else inspect.isfunction


# ------------------------------------------------------------------------------

def _get_action_endpoint(action):
    """
    Return the endpoint base on the view's action
    :param action:
    :return:
    """
    _endpoint = None
    if is_method(action):
        if hasattr(action, "_rule_cache"):
            rc = action._rule_cache
            if rc:
                k = list(rc.keys())[0]
                rules = rc[k]
                len_rules = len(rules)
                if len_rules == 1:
                    rc_kw = rules[0][1]
                    methods = rc_kw.get("methods", None)
                    if methods and ("GET" not in methods or "POST" not in methods):
                        raise exceptions.MamboError("Mambo `url_for` requires endpoint to have a GET or POST method")
                    _endpoint = rc_kw.get("endpoint", None)
                    if not _endpoint:
                        _endpoint = _build_endpoint_route_name(action)
                elif len_rules > 1:
                    _prefix = _build_endpoint_route_name(action)
                    for r in Mambo._app.url_map.iter_rules():
                        if ('GET' in r.methods or 'POST' in r.methods) \
                                and _prefix in r.endpoint:
                            _endpoint = r.endpoint
                            break
    return _endpoint


def url_for(endpoint, **kw):
    """
    Mambo url_for is an alias to the flask url_for, with the ability of
    passing the function signature to build the url, without knowing the endpoint
    :param endpoint:
    :param kw:
    :return:
    """

    _endpoint = None
    if isinstance(endpoint, string_types):
        return f_url_for(endpoint, **kw)
    else:
        # self, will refer the caller method, by getting the method name
        if isinstance(endpoint, Mambo):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)

        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_url_for(_endpoint, **kw)
    else:
        raise exceptions.MamboError('Mambo `url_for` received an invalid endpoint')


def redirect(endpoint, **kw):
    """
    Redirect allow to redirect dynamically using the classes methods without
    knowing the right endpoint.
    Expecting all endpoint have GET as method, it will try to pick the first
    match, based on the endpoint provided or the based on the Rule map_url

    An endpoint can also be passed along with **kw

    An http: or https: can also be passed, and will redirect to that site.

    example:
        redirect(self.hello_world)
        redirect(self.other_page, name="x", value="v")
        redirect("https://google.com")
        redirect(views.ContactPage.index)
    :param endpoint:
    :return: redirect url
    """

    _endpoint = None

    if isinstance(endpoint, string_types):
        _endpoint = endpoint
        # valid for https:// or /path/
        # Endpoint should not have slashes. Use : (colon) to build endpoint
        if "/" in endpoint:
            return f_redirect(endpoint)
        else:
            for r in Mambo._app.url_map.iter_rules():
                _endpoint = endpoint
                if 'GET' in r.methods and endpoint in r.endpoint:
                    _endpoint = r.endpoint
                    break
    else:
        # self, will refer the caller method, by getting the method name
        if isinstance(endpoint, Mambo):
            fn = sys._getframe().f_back.f_code.co_name
            endpoint = getattr(endpoint, fn)

        if is_method(endpoint):
            _endpoint = _get_action_endpoint(endpoint)
            if not _endpoint:
                _endpoint = _build_endpoint_route_name(endpoint)
    if _endpoint:
        return f_redirect(url_for(_endpoint, **kw))
    else:
        raise exceptions.MamboError("Invalid endpoint")


def _build_endpoint_route_name(endpoint):

    cls = endpoint.im_class() \
        if (not hasattr(endpoint, "__self__") or endpoint.__self__ is None) \
        else endpoint.__self__

    return cls.build_route_name(endpoint.__name__)


# ------------------------------------------------------------------------------

class _MamboAlchemy(active_alchemy.ActiveAlchemy):
    """
    A custom ActiveAlchemy wrapper which defers the connection
    """
    def __init__(self):
        self.Model = active_alchemy.declarative_base(cls=active_alchemy.Model, name='Model')
        self.BaseModel = active_alchemy.declarative_base(cls=active_alchemy.BaseModel, name='BaseModel')

    def _connect(self, uri, app):
        self.uri = uri
        self.info = sa_make_url(uri)
        self.options = self._cleanup_options(
            echo=False,
            pool_size=None,
            pool_timeout=None,
            pool_recycle=None,
            convert_unicode=True,
        )

        self.connector = None
        self._engine_lock = active_alchemy.threading.Lock()
        self.session = active_alchemy._create_scoped_session(self,
                                                             query_cls=active_alchemy.BaseQuery)

        self.Model.db, self.BaseModel.db = self, self
        self.Model._query, self.BaseModel._query = self.session.query, self.session.query

        self.init_app(app)
        active_alchemy._include_sqlalchemy(self)

# Setup the DB
# Mambo upon initialization will use the right URI for it
db = _MamboAlchemy()


class Mambo(object):
    """Base view for any class based views implemented with Flask-Classy. Will
    automatically configure routes when registered with a Flask app instance.
    Credit: Shout out to Flask-Classy for the greatest logic in this class
    Flask-Classy -> https://github.com/apiguy/flask-classy
    """

    decorators = []
    base_route = None
    route_prefix = None
    trailing_slash = True
    base_layout = "layout.html"
    assets = None
    logger = None
    __special_methods = ["get", "put", "patch", "post", "delete", "index"]
    _installed_apps = []
    _app = None
    _init_apps = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_meta = dict(
            title="",
            description="",
            url="",
            image="",
            site_name="",
            object_type="article",
            locale="",
            keywords=[],
            use_opengraph=True,
            use_googleplus=True,
            use_twitter=True,
            properties={}
        )
    _global = dict(
        __NAME__=__title__,
        __VERSION__=__version__,
        __YEAR__=datetime.datetime.now().year,
        __META__=_default_page_meta
    )

    @classmethod
    def __call__(cls,
                 flask_or_import_name,
                 app_name=None,
                 app_directory="application",
                 implicit_import=True,
                 load_app=True,
                 load_installed_apps=True
                 ):
        """
        Allow to register all subclasses of Mambo at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param app_name: name of the project. If the directory and config is empty, it will guess them from here
        :param app_directory: the directory name relative to the current execution path
        :param implicit_import: when True, it will automatically load the views, models
        :param load_app: when True it will load your application
        :param load_installed_apps: bool - When True it will load the installed apps
        """

        app = flask_or_import_name \
            if isinstance(flask_or_import_name, Flask) \
            else Flask(flask_or_import_name)

        app_name = app_name if app_name else get_app_env()[0] or "www"
        app_env = get_env()

        # Load global and project config
        for c in [
                  "%s.config.%s" % (app_directory, app_env),  # Global config
                  "%s.%s.config.%s" % (app_directory, app_name, app_env)  # project config
                  ]:
            try:
                app.config.from_object(c)
            except ImportError as e:
                pass

        app.wsgi_app = ProxyFix(app.wsgi_app)
        app.url_map.converters['regex'] = RegexConverter
        app.template_folder = "%s/%s/templates" % (app_directory, app_name)
        app.static_folder = "%s/%s/static" % (app_directory, app_name)

        # Extensions to remove extra white spaces in html
        if app.config.get("COMPRESS_HTML"):
            app.jinja_env.add_extension('mambo.htmlcompress.HTMLCompress')

        cls._app = app

        cls._setup_logger()

        # Flask Assets
        cls.assets = Environment(cls._app)

        cls._setup_db()

        # INSTALLED_APPS
        if load_installed_apps:
            _ = cls.setup_installed_apps()

        cls._expose_models()

        # Implicit import.
        # Mambo can load models and view files according to the convention:
        # application.models,
        # application.$project_name.models,
        # application.$project_name.views
        if implicit_import:
            # Import global application's models and project's models
            for m in ["%s.models" % app_directory,
                      "%s.%s.models" % (app_directory, app_name)
                      ]:
                try:
                    import_module(m)
                    cls._expose_models()
                except ImportError as ie1:
                    pass

            # The view is required
            import_module("%s.%s.views" % (app_directory, app_name))

        cls._expose_models()

        # Setup init_app
        # init_app instanciate functions that may need the flask.app object
        # Usually for flask extension to be setup
        [_app(cls._app) for _app in cls._init_apps]

        if load_app:
            # Ad bundles
            cls._add_asset_bundle(cls._app.static_folder)

            # Register templates
            if cls._template_paths:
                loader = [cls._app.jinja_loader] + list(cls._template_paths)
                cls._app.jinja_loader = jinja2.ChoiceLoader(loader)
                
            # Static
            if cls._static_paths:
                cls.assets.load_path = [cls._app.static_folder] + list(cls._static_paths)
                [cls.assets.from_yaml(a) for a in cls._asset_bundles]
                
            # Register views
            for subcls in cls.__subclasses__():
                base_route = subcls.base_route
                if not base_route:
                    base_route = utils.dasherize(utils.underscore(subcls.__name__))
                    if subcls.__name__.lower() == "index":
                        base_route = "/"
                subcls._register(cls._app, base_route=base_route)

        @cls._app.after_request
        def _after_request_cleanup(response):
            cls._global["__META__"] = cls._default_page_meta.copy()
            return response
        return cls._app

    @classmethod
    def setup_installed_apps(cls):
        """
        To import 3rd party applications along with associated properties

        It is a list of dict or string.

        When a dict, it contains the `app` key and the configuration,
        if it's a string, it is just the app name

        If you require dependencies from other packages, dependencies
        must be placed before the calling package.

        It is required that __init__ in the package app has an entry point method
        -> 'main(**kw)' which will be used to setup the default app.

        By default the following **kwargs are passed to the main function:
            app: (object)[always] object of the flask app
            route: (string) the base route for the app. default: /
            nav_menu: (dict) the navigation config for navigation menu. By default the title is set to None
            decorators: (list) list of decorators (as string) to use
            options: (dict) all the app's customs options

        As a dict
        INSTALLED_APPS = [
            "my.contrib.app",
            "my.other.contrib.app",
            {
                "app": "my.contrib.app3",
                "options": {

                },
                "modules": {
                    "module_a": {
                        "route": "/",
                        "nav_menu": {

                        }
                    },
                    "module_b": {
                        "route": "/",
                        "decorators": []
                    }
                }
            }
        ]
        :return:
        """
        cls._installed_apps = cls._app.config.get("INSTALLED_APPS", [])
        if cls._installed_apps:
            _ = []

            def import_app(app, kwargs):
                try:
                    _.append(import_string("%s.main" % app)(**kwargs))
                except ImportError as e:
                    logging.warning(e.message)

            for k in cls._installed_apps:
                if isinstance(k, string_types):
                    a = k
                    prop = {}
                elif isinstance(k, dict):
                    a = k.get("app")
                    k["name"] = a
                    prop = k

                _kwargs = {
                    "app": cls._app,
                    "name": prop.get("name"),
                    "route": prop.get("route") or "/",
                    "nav_menu": prop.get("nav_menu") or {"title": None},
                    "decorators": [import_string(d) for d in prop.get("decorators")]
                                    if "decorators" in prop
                                    else [],
                    "options": prop.get("options") or {}
                }

                # Loading the module
                try:
                    _impm = import_string(a)
                    logging.info("Loading installed app: %s v.%s" % (a, _impm.__version__))
                    try:
                        import_string("%s.models" % a)
                        cls._expose_models()
                    except ImportError as ie: pass
                    import_app(a, _kwargs)
                except ImportError as e:
                    logging.warning(e)

                modules = prop["modules"] if "modules" in prop else None
                if modules:
                    if isinstance(modules, list):
                        for m in modules:
                            import_app("%s.%s" % (a, m), _kwargs)
                    elif isinstance(modules, dict):
                        for n, kw in modules.items():
                            kw2 = {
                                "app": _kwargs["app"],
                                "name": "%s.%s" % (a, n),
                                "route": kw.get("route") or "/",
                                "nav_menu": kw.get("nav_menu") or {"title": None},
                                "decorators": _kwargs["decorators"],
                                "options": _kwargs["options"]
                            }
                            import_app("%s.%s" % (a, n), kw2)
            return _

    @classmethod
    def render(cls, data={}, _template=None, _layout=None, **kwargs):
        """
        Render the view template based on the class and the method being invoked
        :param data: The context data to pass to the template
        :param _template: The file template to use. By default it will map the classname/action.html
        :param _layout: The body layout, must contain {% include __template__ %}
        """
        if not _template:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split(".")[-1]
            action_name = stack[3]      # The method being called in the class
            view_name = cls.__name__    # The name of the class without View

            if view_name.endswith("View"):
                view_name = view_name[:-4]
            _template = "%s/%s.html" % (view_name, action_name)

        data = data or dict()
        if kwargs:
            data.update(kwargs)
        data["__"] = cls._global
        data["__template__"] = _template

        return render_template(_layout or cls.base_layout, **data)

    @classmethod
    def g(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._global.update(kwargs)

    @classmethod
    def _add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = "%s/assets.yml" % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def _setup_logger(cls):
        logging_config = cls._app.config.get("LOGGING")
        if not logging_config:
            logging_config = {
                "version": 1,
                "handlers": {
                    "default": {
                        "class": cls._app.config.get("LOGGING_CLASS", "logging.StreamHandler")
                    }
                },
                'loggers': {
                    '': {
                        'handlers': ['default'],
                        'level': 'WARN',
                    }
                }
            }

        logging.config.dictConfig(logging_config)
        cls.logger = logging.getLogger("root")
        cls._app._logger = cls.logger
        cls._app._loger_name = cls.logger.name

    @classmethod
    def _setup_db(cls):
        cls._app.db = None
        uri = cls._app.config.get("DB_URI")
        if uri:
            db._connect(uri, cls._app)
            cls._app.db = db

    @classmethod
    def _expose_models(cls):
        if cls._app.db:
            register_models(**{m.__name__:m
                               for m in cls._app.db.Model.__subclasses__()
                               if not hasattr(models, m.__name__)})

    @classmethod
    def _register(cls, app, base_route=None, subdomain=None, route_prefix=None,
                 trailing_slash=None):
        """Registers a Mambo class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param base_route: The base path to use for all routes registered for
                           this class. Overrides the base_route attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes base_route. Overrides
                             the class' route_prefix if it has been set.
        """

        if cls is Mambo:
            raise TypeError("cls must be a subclass of Mambo, not Mambo itself")

        # Assign views
        setattr(views, cls.__name__, cls)

        if base_route:
            cls.orig_base_route = cls.base_route
            cls.base_route = base_route

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        for name, value in get_interesting_members(Mambo, cls):
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "%s_%d" % (route_name, idx,)

                        app.add_url_rule(rule, endpoint, proxy,
                                         subdomain=subdomain,
                                         **options)
                elif name in cls.__special_methods:
                    if name in ["get", "index"]:
                        methods = ["GET"]
                        if name == "index":
                            if hasattr(value, "_methods_cache"):
                                methods = value._methods_cache
                    else:
                        methods = [name.upper()]

                    rule = cls.build_rule("/", value)
                    if not cls.trailing_slash:
                        rule = rule.rstrip("/")
                    app.add_url_rule(rule, route_name, proxy,
                                     methods=methods,
                                     subdomain=subdomain)

                else:
                    methods = value._methods_cache \
                        if hasattr(value, "_methods_cache") \
                        else ["GET"]

                    name = utils.dasherize(name)
                    route_str = '/%s/' % name
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    app.add_url_rule(rule, route_name, proxy,
                                     subdomain=subdomain,
                                     methods=methods)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError("Incompatible decorator detected on %s in class %s" % (name, cls.__name__))

        if hasattr(cls, "orig_base_route"):
            cls.base_route = cls.orig_base_route
            del cls.orig_base_route

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash

    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the Mambo subclass and calls the appropriate
        method.
        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        if cls.decorators:
            for decorator in cls.decorators:
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)

            # You can also return a dict or None, it will pass it to render
            if isinstance(response, dict) or response is None:
                response = response or {}
                if hasattr(i, "_renderer"):
                    response = i._renderer(response)
                else:
                    df_v_t = "%s/%s.html" % (cls.__name__, view.__name__)
                    response.setdefault("_template", df_v_t)
                    response = i.render(**response)

            if not isinstance(response, Response):
                response = make_response(response)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `base_route` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        base_route = cls.get_base_route()
        if base_route:
            rule_parts.append(base_route)

        rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method:
            args = get_true_argspec(method)[0]
            for arg in args:
                if arg not in ignored_rule_args:
                    rule_parts.append("<%s>" % arg)

        result = "/%s" % "/".join(rule_parts)
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def get_base_route(cls):
        """Returns the route base to use for the current class."""

        if cls.base_route is not None:
            base_route = cls.base_route
            base_rule = parse_rule(base_route)
            cls.base_args = [r[2] for r in base_rule]
        else:
            if cls.__name__.endswith("View"):
                base_route = cls.__name__[:-4].lower()
            else:
                base_route = cls.__name__.lower()

        return base_route.strip("/")

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":%s" % method_name

    @staticmethod
    def _bind_route_rule_cache(f, rule, append_method=False, **kwargs):
        # Put the rule cache on the method itself instead of globally
        if rule is None:
            rule = utils.dasherize(f.__name__) + "/"
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, kwargs)]}
        elif not f.__name__ in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, kwargs)]
        else:
            # when and endpoint accepts multiple METHODS, ie: post(), get()
            if append_method:
                for r in f._rule_cache[f.__name__]:
                    if r[0] == rule and "methods" in r[1] and "methods" in kwargs:
                        r[1]["methods"] = list(set(r[1]["methods"] + kwargs["methods"]))
            else:
                f._rule_cache[f.__name__].append((rule, kwargs))
        return f


# MamboInit
MamboInit = Mambo()

# ------------------------------------------------------------------------------


def get_interesting_members(base_class, cls):
    """Returns a generator of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return (member for member in all_members
            if not member[0] in base_members
            and ((hasattr(member[1], "__self__") and not member[1].__self__ in inspect.getmro(cls)) if _py2 else True)
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_"))


def get_true_argspec(method):
    """Drills through layers of decorators attempting to locate the actual argspec for the method."""

    argspec = inspect.getargspec(method)
    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method) \
            and not inspect.ismethod(inner_method):
            continue
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec


class DecoratorCompatibilityError(Exception):
    pass


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def get_installed_app_options(app):
    """
    Get the app's options
    :param app: the app, ie: __name__
    :return:
    """
    options = {}
    if Mambo._installed_apps:
        for k in Mambo._installed_apps:
            if isinstance(k, dict) and "name" in k and k["name"] == app:
                options = k["options"] if "options" in k else {}
                break
    return options