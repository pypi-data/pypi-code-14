# coding: utf-8
"""A tornado based Jupyter notebook server."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import absolute_import, print_function

import base64
import datetime
import errno
import importlib
import io
import json
import logging
import mimetypes
import os
import random
import re
import select
import signal
import socket
import sys
import threading
import webbrowser

from jinja2 import Environment, FileSystemLoader

# Install the pyzmq ioloop. This has to be done before anything else from
# tornado is imported.
from zmq.eventloop import ioloop
ioloop.install()

# check for tornado 3.1.0
msg = "The Jupyter Notebook requires tornado >= 4.0"
try:
    import tornado
except ImportError:
    raise ImportError(msg)
try:
    version_info = tornado.version_info
except AttributeError:
    raise ImportError(msg + ", but you have < 1.1.0")
if version_info < (4,0):
    raise ImportError(msg + ", but you have %s" % tornado.version)

from tornado import httpserver
from tornado import web
from tornado.log import LogFormatter, app_log, access_log, gen_log

from notebook import (
    DEFAULT_STATIC_FILES_PATH,
    DEFAULT_TEMPLATE_PATH_LIST,
    __version__,
)
from .base.handlers import Template404
from .log import log_request
from .services.kernels.kernelmanager import MappingKernelManager
from .services.config import ConfigManager
from .services.contents.manager import ContentsManager
from .services.contents.filemanager import FileContentsManager
from .services.sessions.sessionmanager import SessionManager

from .auth.login import LoginHandler
from .auth.logout import LogoutHandler
from .base.handlers import FileFindHandler, IPythonHandler

from traitlets.config import Config
from traitlets.config.application import catch_config_error, boolean_flag
from jupyter_core.application import (
    JupyterApp, base_flags, base_aliases,
)
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager, NoSuchKernel, NATIVE_KERNEL_NAME
from jupyter_client.session import Session
from nbformat.sign import NotebookNotary
from traitlets import (
    Dict, Unicode, Integer, List, Bool, Bytes, Instance,
    TraitError, Type, Float
)
from ipython_genutils import py3compat
from jupyter_core.paths import jupyter_runtime_dir, jupyter_path
from notebook._sysinfo import get_sys_info

from .utils import url_path_join, check_pid, url_escape

#-----------------------------------------------------------------------------
# Module globals
#-----------------------------------------------------------------------------

_examples = """
jupyter notebook                       # start the notebook
jupyter notebook --certfile=mycert.pem # use SSL/TLS certificate
"""

#-----------------------------------------------------------------------------
# Helper functions
#-----------------------------------------------------------------------------

def random_ports(port, n):
    """Generate a list of n random ports near the given port.

    The first 5 ports will be sequential, and the remaining n-5 will be
    randomly selected in the range [port-2*n, port+2*n].
    """
    for i in range(min(5, n)):
        yield port + i
    for i in range(n-5):
        yield max(1, port + random.randint(-2*n, 2*n))

def load_handlers(name):
    """Load the (URL pattern, handler) tuples for each component."""
    name = 'notebook.' + name
    mod = __import__(name, fromlist=['default_handlers'])
    return mod.default_handlers


#-----------------------------------------------------------------------------
# The Tornado web application
#-----------------------------------------------------------------------------

class NotebookWebApplication(web.Application):

    def __init__(self, ipython_app, kernel_manager, contents_manager,
                 session_manager, kernel_spec_manager,
                 config_manager, log,
                 base_url, default_url, settings_overrides, jinja_env_options):

        settings = self.init_settings(
            ipython_app, kernel_manager, contents_manager,
            session_manager, kernel_spec_manager, config_manager, log, base_url,
            default_url, settings_overrides, jinja_env_options)
        handlers = self.init_handlers(settings)

        super(NotebookWebApplication, self).__init__(handlers, **settings)

    def init_settings(self, ipython_app, kernel_manager, contents_manager,
                      session_manager, kernel_spec_manager,
                      config_manager,
                      log, base_url, default_url, settings_overrides,
                      jinja_env_options=None):

        _template_path = settings_overrides.get(
            "template_path",
            ipython_app.template_file_path,
        )
        if isinstance(_template_path, py3compat.string_types):
            _template_path = (_template_path,)
        template_path = [os.path.expanduser(path) for path in _template_path]

        jenv_opt = {"autoescape": True}
        jenv_opt.update(jinja_env_options if jinja_env_options else {})

        env = Environment(loader=FileSystemLoader(template_path), **jenv_opt)
        
        sys_info = get_sys_info()
        if sys_info['commit_source'] == 'repository':
            # don't cache (rely on 304) when working from master
            version_hash = ''
        else:
            # reset the cache on server restart
            version_hash = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        settings = dict(
            # basics
            log_function=log_request,
            base_url=base_url,
            default_url=default_url,
            template_path=template_path,
            static_path=ipython_app.static_file_path,
            static_custom_path=ipython_app.static_custom_path,
            static_handler_class = FileFindHandler,
            static_url_prefix = url_path_join(base_url,'/static/'),
            static_handler_args = {
                # don't cache custom.js
                'no_cache_paths': [url_path_join(base_url, 'static', 'custom')],
            },
            version_hash=version_hash,
            ignore_minified_js=ipython_app.ignore_minified_js,

            # rate limits
            iopub_msg_rate_limit=ipython_app.iopub_msg_rate_limit,
            iopub_data_rate_limit=ipython_app.iopub_data_rate_limit,
            rate_limit_window=ipython_app.rate_limit_window,

            # authentication
            cookie_secret=ipython_app.cookie_secret,
            login_url=url_path_join(base_url,'/login'),
            login_handler_class=ipython_app.login_handler_class,
            logout_handler_class=ipython_app.logout_handler_class,
            password=ipython_app.password,

            # managers
            kernel_manager=kernel_manager,
            contents_manager=contents_manager,
            session_manager=session_manager,
            kernel_spec_manager=kernel_spec_manager,
            config_manager=config_manager,

            # IPython stuff
            jinja_template_vars=ipython_app.jinja_template_vars,
            nbextensions_path=ipython_app.nbextensions_path,
            websocket_url=ipython_app.websocket_url,
            mathjax_url=ipython_app.mathjax_url,
            config=ipython_app.config,
            config_dir=ipython_app.config_dir,
            jinja2_env=env,
            terminals_available=False,  # Set later if terminals are available
        )

        # allow custom overrides for the tornado web app.
        settings.update(settings_overrides)
        return settings

    def init_handlers(self, settings):
        """Load the (URL pattern, handler) tuples for each component."""
        
        # Order matters. The first handler to match the URL will handle the request.
        handlers = []
        handlers.extend(load_handlers('tree.handlers'))
        handlers.extend([(r"/login", settings['login_handler_class'])])
        handlers.extend([(r"/logout", settings['logout_handler_class'])])
        handlers.extend(load_handlers('files.handlers'))
        handlers.extend(load_handlers('notebook.handlers'))
        handlers.extend(load_handlers('nbconvert.handlers'))
        handlers.extend(load_handlers('kernelspecs.handlers'))
        handlers.extend(load_handlers('edit.handlers'))
        handlers.extend(load_handlers('services.api.handlers'))
        handlers.extend(load_handlers('services.config.handlers'))
        handlers.extend(load_handlers('services.kernels.handlers'))
        handlers.extend(load_handlers('services.contents.handlers'))
        handlers.extend(load_handlers('services.sessions.handlers'))
        handlers.extend(load_handlers('services.nbconvert.handlers'))
        handlers.extend(load_handlers('services.kernelspecs.handlers'))
        handlers.extend(load_handlers('services.security.handlers'))
        
        # BEGIN HARDCODED WIDGETS HACK
        # TODO: Remove on notebook 5.0
        try:
            import widgetsnbextension
        except:
            try:
                import ipywidgets as widgets
                handlers.append(
                    (r"/nbextensions/widgets/(.*)", FileFindHandler, {
                        'path': widgets.find_static_assets(),
                        'no_cache_paths': ['/'], # don't cache anything in nbextensions
                    }),
                )
            except:
                app_log.warning('Widgets are unavailable. Please install widgetsnbextension or ipywidgets 4.0')
        # END HARDCODED WIDGETS HACK
        
        handlers.append(
            (r"/nbextensions/(.*)", FileFindHandler, {
                'path': settings['nbextensions_path'],
                'no_cache_paths': ['/'], # don't cache anything in nbextensions
            }),
        )
        handlers.append(
            (r"/custom/(.*)", FileFindHandler, {
                'path': settings['static_custom_path'],
                'no_cache_paths': ['/'], # don't cache anything in custom
            })
        )
        # register base handlers last
        handlers.extend(load_handlers('base.handlers'))
        # set the URL that will be redirected from `/`
        handlers.append(
            (r'/?', web.RedirectHandler, {
                'url' : settings['default_url'],
                'permanent': False, # want 302, not 301
            })
        )

        # prepend base_url onto the patterns that we match
        new_handlers = []
        for handler in handlers:
            pattern = url_path_join(settings['base_url'], handler[0])
            new_handler = tuple([pattern] + list(handler[1:]))
            new_handlers.append(new_handler)
        # add 404 on the end, which will catch everything that falls through
        new_handlers.append((r'(.*)', Template404))
        return new_handlers


class NbserverListApp(JupyterApp):
    version = __version__
    description="List currently running notebook servers."
    
    flags = dict(
        json=({'NbserverListApp': {'json': True}},
              "Produce machine-readable JSON output."),
    )
    
    json = Bool(False, config=True,
          help="If True, each line of output will be a JSON object with the "
                  "details from the server info file.")

    def start(self):
        if not self.json:
            print("Currently running servers:")
        for serverinfo in list_running_servers(self.runtime_dir):
            if self.json:
                print(json.dumps(serverinfo))
            else:
                print(serverinfo['url'], "::", serverinfo['notebook_dir'])

#-----------------------------------------------------------------------------
# Aliases and Flags
#-----------------------------------------------------------------------------

flags = dict(base_flags)
flags['no-browser']=(
    {'NotebookApp' : {'open_browser' : False}},
    "Don't open the notebook in a browser after startup."
)
flags['pylab']=(
    {'NotebookApp' : {'pylab' : 'warn'}},
    "DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib."
)
flags['no-mathjax']=(
    {'NotebookApp' : {'enable_mathjax' : False}},
    """Disable MathJax
    
    MathJax is the javascript library Jupyter uses to render math/LaTeX. It is
    very large, so you may want to disable it if you have a slow internet
    connection, or for offline use of the notebook.
    
    When disabled, equations etc. will appear as their untransformed TeX source.
    """
)

# Add notebook manager flags
flags.update(boolean_flag('script', 'FileContentsManager.save_script',
               'DEPRECATED, IGNORED',
               'DEPRECATED, IGNORED'))

aliases = dict(base_aliases)

aliases.update({
    'ip': 'NotebookApp.ip',
    'port': 'NotebookApp.port',
    'port-retries': 'NotebookApp.port_retries',
    'transport': 'KernelManager.transport',
    'keyfile': 'NotebookApp.keyfile',
    'certfile': 'NotebookApp.certfile',
    'client-ca': 'NotebookApp.client_ca',
    'notebook-dir': 'NotebookApp.notebook_dir',
    'browser': 'NotebookApp.browser',
    'pylab': 'NotebookApp.pylab',
})

#-----------------------------------------------------------------------------
# NotebookApp
#-----------------------------------------------------------------------------

class NotebookApp(JupyterApp):

    name = 'jupyter-notebook'
    version = __version__
    description = """
        The Jupyter HTML Notebook.
        
        This launches a Tornado based HTML Notebook Server that serves up an
        HTML5/Javascript Notebook client.
    """
    examples = _examples
    aliases = aliases
    flags = flags
    
    classes = [
        KernelManager, Session, MappingKernelManager,
        ContentsManager, FileContentsManager, NotebookNotary,
        KernelSpecManager,
    ]
    flags = Dict(flags)
    aliases = Dict(aliases)
    
    subcommands = dict(
        list=(NbserverListApp, NbserverListApp.description.splitlines()[0]),
    )

    _log_formatter_cls = LogFormatter

    def _log_level_default(self):
        return logging.INFO

    def _log_datefmt_default(self):
        """Exclude date from default date format"""
        return "%H:%M:%S"
    
    def _log_format_default(self):
        """override default log format to include time"""
        return u"%(color)s[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s]%(end_color)s %(message)s"

    ignore_minified_js = Bool(False,
            config=True,
            help='Use minified JS file or not, mainly use during dev to avoid JS recompilation', 
            )

    # file to be opened in the notebook server
    file_to_run = Unicode('', config=True)

    # Network related information
    
    allow_origin = Unicode('', config=True,
        help="""Set the Access-Control-Allow-Origin header
        
        Use '*' to allow any origin to access your server.
        
        Takes precedence over allow_origin_pat.
        """
    )
    
    allow_origin_pat = Unicode('', config=True,
        help="""Use a regular expression for the Access-Control-Allow-Origin header
        
        Requests from an origin matching the expression will get replies with:
        
            Access-Control-Allow-Origin: origin
        
        where `origin` is the origin of the request.
        
        Ignored if allow_origin is set.
        """
    )
    
    allow_credentials = Bool(False, config=True,
        help="Set the Access-Control-Allow-Credentials: true header"
    )
    
    default_url = Unicode('/tree', config=True,
        help="The default URL to redirect to from `/`"
    )
    
    ip = Unicode('localhost', config=True,
        help="The IP address the notebook server will listen on."
    )
    def _ip_default(self):
        """Return localhost if available, 127.0.0.1 otherwise.
        
        On some (horribly broken) systems, localhost cannot be bound.
        """
        s = socket.socket()
        try:
            s.bind(('localhost', 0))
        except socket.error as e:
            self.log.warn("Cannot bind to localhost, using 127.0.0.1 as default ip\n%s", e)
            return '127.0.0.1'
        else:
            s.close()
            return 'localhost'

    def _ip_changed(self, name, old, new):
        if new == u'*': self.ip = u''

    port = Integer(8888, config=True,
        help="The port the notebook server will listen on."
    )
    port_retries = Integer(50, config=True,
        help="The number of additional ports to try if the specified port is not available."
    )

    certfile = Unicode(u'', config=True, 
        help="""The full path to an SSL/TLS certificate file."""
    )
    
    keyfile = Unicode(u'', config=True, 
        help="""The full path to a private key file for usage with SSL/TLS."""
    )
    
    client_ca = Unicode(u'', config=True,
        help="""The full path to a certificate authority certificate for SSL/TLS client authentication."""
    )
    
    cookie_secret_file = Unicode(config=True,
        help="""The file where the cookie secret is stored."""
    )
    def _cookie_secret_file_default(self):
        return os.path.join(self.runtime_dir, 'notebook_cookie_secret')
    
    cookie_secret = Bytes(b'', config=True,
        help="""The random bytes used to secure cookies.
        By default this is a new random number every time you start the Notebook.
        Set it to a value in a config file to enable logins to persist across server sessions.
        
        Note: Cookie secrets should be kept private, do not share config files with
        cookie_secret stored in plaintext (you can read the value from a file).
        """
    )
    def _cookie_secret_default(self):
        if os.path.exists(self.cookie_secret_file):
            with io.open(self.cookie_secret_file, 'rb') as f:
                return f.read()
        else:
            secret = base64.encodestring(os.urandom(1024))
            self._write_cookie_secret_file(secret)
            return secret
    
    def _write_cookie_secret_file(self, secret):
        """write my secret to my secret_file"""
        self.log.info("Writing notebook server cookie secret to %s", self.cookie_secret_file)
        with io.open(self.cookie_secret_file, 'wb') as f:
            f.write(secret)
        try:
            os.chmod(self.cookie_secret_file, 0o600)
        except OSError:
            self.log.warn(
                "Could not set permissions on %s",
                self.cookie_secret_file
            )

    password = Unicode(u'', config=True,
                      help="""Hashed password to use for web authentication.

                      To generate, type in a python/IPython shell:

                        from notebook.auth import passwd; passwd()

                      The string should be of the form type:salt:hashed-password.
                      """
    )

    open_browser = Bool(True, config=True,
                        help="""Whether to open in a browser after starting.
                        The specific browser used is platform dependent and
                        determined by the python standard library `webbrowser`
                        module, unless it is overridden using the --browser
                        (NotebookApp.browser) configuration option.
                        """)

    browser = Unicode(u'', config=True,
                      help="""Specify what command to use to invoke a web
                      browser when opening the notebook. If not specified, the
                      default browser will be determined by the `webbrowser`
                      standard library module, which allows setting of the
                      BROWSER environment variable to override it.
                      """)
    
    webapp_settings = Dict(config=True,
        help="DEPRECATED, use tornado_settings"
    )
    def _webapp_settings_changed(self, name, old, new):
        self.log.warn("\n    webapp_settings is deprecated, use tornado_settings.\n")
        self.tornado_settings = new
    
    tornado_settings = Dict(config=True,
            help="Supply overrides for the tornado.web.Application that the "
                 "Jupyter notebook uses.")
    
    cookie_options = Dict(config=True,
        help="Extra keyword arguments to pass to `set_secure_cookie`."
             " See tornado's set_secure_cookie docs for details."
    )
    ssl_options = Dict(config=True,
            help="""Supply SSL options for the tornado HTTPServer.
            See the tornado docs for details.""")
    
    jinja_environment_options = Dict(config=True, 
            help="Supply extra arguments that will be passed to Jinja environment.")

    jinja_template_vars = Dict(
        config=True,
        help="Extra variables to supply to jinja templates when rendering.",
    )
    
    enable_mathjax = Bool(True, config=True,
        help="""Whether to enable MathJax for typesetting math/TeX

        MathJax is the javascript library Jupyter uses to render math/LaTeX. It is
        very large, so you may want to disable it if you have a slow internet
        connection, or for offline use of the notebook.

        When disabled, equations etc. will appear as their untransformed TeX source.
        """
    )
    def _enable_mathjax_changed(self, name, old, new):
        """set mathjax url to empty if mathjax is disabled"""
        if not new:
            self.mathjax_url = u''

    base_url = Unicode('/', config=True,
                               help='''The base URL for the notebook server.

                               Leading and trailing slashes can be omitted,
                               and will automatically be added.
                               ''')
    def _base_url_changed(self, name, old, new):
        if not new.startswith('/'):
            self.base_url = '/'+new
        elif not new.endswith('/'):
            self.base_url = new+'/'
    
    base_project_url = Unicode('/', config=True, help="""DEPRECATED use base_url""")
    def _base_project_url_changed(self, name, old, new):
        self.log.warn("base_project_url is deprecated, use base_url")
        self.base_url = new

    extra_static_paths = List(Unicode(), config=True,
        help="""Extra paths to search for serving static files.
        
        This allows adding javascript/css to be available from the notebook server machine,
        or overriding individual files in the IPython"""
    )
    
    @property
    def static_file_path(self):
        """return extra paths + the default location"""
        return self.extra_static_paths + [DEFAULT_STATIC_FILES_PATH]
    
    static_custom_path = List(Unicode(),
        help="""Path to search for custom.js, css"""
    )
    def _static_custom_path_default(self):
        return [
            os.path.join(d, 'custom') for d in (
                self.config_dir,
                DEFAULT_STATIC_FILES_PATH)
        ]

    extra_template_paths = List(Unicode(), config=True,
        help="""Extra paths to search for serving jinja templates.

        Can be used to override templates from notebook.templates."""
    )

    @property
    def template_file_path(self):
        """return extra paths + the default locations"""
        return self.extra_template_paths + DEFAULT_TEMPLATE_PATH_LIST

    extra_nbextensions_path = List(Unicode(), config=True,
        help="""extra paths to look for Javascript notebook extensions"""
    )
    
    @property
    def nbextensions_path(self):
        """The path to look for Javascript notebook extensions"""
        path = self.extra_nbextensions_path + jupyter_path('nbextensions')
        # FIXME: remove IPython nbextensions path after a migration period
        try:
            from IPython.paths import get_ipython_dir
        except ImportError:
            pass
        else:
            path.append(os.path.join(get_ipython_dir(), 'nbextensions'))
        return path

    websocket_url = Unicode("", config=True,
        help="""The base URL for websockets,
        if it differs from the HTTP server (hint: it almost certainly doesn't).
        
        Should be in the form of an HTTP origin: ws[s]://hostname[:port]
        """
    )
    mathjax_url = Unicode("", config=True,
        help="""The url for MathJax.js."""
    )
    def _mathjax_url_default(self):
        if not self.enable_mathjax:
            return u''
        static_url_prefix = self.tornado_settings.get("static_url_prefix", "static")
        return url_path_join(static_url_prefix, 'components', 'MathJax', 'MathJax.js')
    
    def _mathjax_url_changed(self, name, old, new):
        if new and not self.enable_mathjax:
            # enable_mathjax=False overrides mathjax_url
            self.mathjax_url = u''
        else:
            self.log.info("Using MathJax: %s", new)

    contents_manager_class = Type(
        default_value=FileContentsManager,
        klass=ContentsManager,
        config=True,
        help='The notebook manager class to use.'
    )
    kernel_manager_class = Type(
        default_value=MappingKernelManager,
        config=True,
        help='The kernel manager class to use.'
    )
    session_manager_class = Type(
        default_value=SessionManager,
        config=True,
        help='The session manager class to use.'
    )

    config_manager_class = Type(
        default_value=ConfigManager,
        config = True,
        help='The config manager class to use'
    )

    kernel_spec_manager = Instance(KernelSpecManager, allow_none=True)

    kernel_spec_manager_class = Type(
        default_value=KernelSpecManager,
        config=True,
        help="""
        The kernel spec manager class to use. Should be a subclass
        of `jupyter_client.kernelspec.KernelSpecManager`.

        The Api of KernelSpecManager is provisional and might change
        without warning between this version of Jupyter and the next stable one.
        """
    )

    login_handler_class = Type(
        default_value=LoginHandler,
        klass=web.RequestHandler,
        config=True,
        help='The login handler class to use.',
    )

    logout_handler_class = Type(
        default_value=LogoutHandler,
        klass=web.RequestHandler,
        config=True,
        help='The logout handler class to use.',
    )

    trust_xheaders = Bool(False, config=True,
        help=("Whether to trust or not X-Scheme/X-Forwarded-Proto and X-Real-Ip/X-Forwarded-For headers"
              "sent by the upstream reverse proxy. Necessary if the proxy handles SSL")
    )

    info_file = Unicode()

    def _info_file_default(self):
        info_file = "nbserver-%s.json" % os.getpid()
        return os.path.join(self.runtime_dir, info_file)
    
    pylab = Unicode('disabled', config=True,
        help="""
        DISABLED: use %pylab or %matplotlib in the notebook to enable matplotlib.
        """
    )
    def _pylab_changed(self, name, old, new):
        """when --pylab is specified, display a warning and exit"""
        if new != 'warn':
            backend = ' %s' % new
        else:
            backend = ''
        self.log.error("Support for specifying --pylab on the command line has been removed.")
        self.log.error(
            "Please use `%pylab{0}` or `%matplotlib{0}` in the notebook itself.".format(backend)
        )
        self.exit(1)

    notebook_dir = Unicode(config=True,
        help="The directory to use for notebooks and kernels."
    )

    def _notebook_dir_default(self):
        if self.file_to_run:
            return os.path.dirname(os.path.abspath(self.file_to_run))
        else:
            return py3compat.getcwd()

    def _notebook_dir_validate(self, value, trait):
        # Strip any trailing slashes
        # *except* if it's root
        _, path = os.path.splitdrive(value)
        if path == os.sep:
            return value

        value = value.rstrip(os.sep)

        if not os.path.isabs(value):
            # If we receive a non-absolute path, make it absolute.
            value = os.path.abspath(value)
        if not os.path.isdir(value):
            raise TraitError("No such notebook dir: %r" % value)
        return value

    def _notebook_dir_changed(self, name, old, new):
        """Do a bit of validation of the notebook dir."""
        # setting App.notebook_dir implies setting notebook and kernel dirs as well
        self.config.FileContentsManager.root_dir = new
        self.config.MappingKernelManager.root_dir = new

    # TODO: Remove me in notebook 5.0
    server_extensions = List(Unicode(), config=True,
        help=("DEPRECATED use the nbserver_extensions dict instead")
    )
    def _server_extensions_changed(self, name, old, new):
        self.log.warning("server_extensions is deprecated, use nbserver_extensions")
        self.server_extensions = new
    
    nbserver_extensions = Dict({}, config=True,
        help=("Dict of Python modules to load as notebook server extensions."
              "Entry values can be used to enable and disable the loading of"
              "the extensions.")
    )

    reraise_server_extension_failures = Bool(
        False,
        config=True,
        help="Reraise exceptions encountered loading server extensions?",
    )

    iopub_msg_rate_limit = Float(0, config=True, help="""(msg/sec)
        Maximum rate at which messages can be sent on iopub before they are
        limited.""")

    iopub_data_rate_limit = Float(0, config=True, help="""(bytes/sec)
        Maximum rate at which messages can be sent on iopub before they are
        limited.""")

    rate_limit_window = Float(1.0, config=True, help="""(sec) Time window used to 
        check the message and data rate limits.""")

    def parse_command_line(self, argv=None):
        super(NotebookApp, self).parse_command_line(argv)

        if self.extra_args:
            arg0 = self.extra_args[0]
            f = os.path.abspath(arg0)
            self.argv.remove(arg0)
            if not os.path.exists(f):
                self.log.critical("No such file or directory: %s", f)
                self.exit(1)
            
            # Use config here, to ensure that it takes higher priority than
            # anything that comes from the config dirs.
            c = Config()
            if os.path.isdir(f):
                c.NotebookApp.notebook_dir = f
            elif os.path.isfile(f):
                c.NotebookApp.file_to_run = f
            self.update_config(c)

    def init_configurables(self):
        self.kernel_spec_manager = self.kernel_spec_manager_class(
            parent=self,
        )
        self.kernel_manager = self.kernel_manager_class(
            parent=self,
            log=self.log,
            connection_dir=self.runtime_dir,
            kernel_spec_manager=self.kernel_spec_manager,
        )
        self.contents_manager = self.contents_manager_class(
            parent=self,
            log=self.log,
        )
        self.session_manager = self.session_manager_class(
            parent=self,
            log=self.log,
            kernel_manager=self.kernel_manager,
            contents_manager=self.contents_manager,
        )
        self.config_manager = self.config_manager_class(
            parent=self,
            log=self.log,
            config_dir=os.path.join(self.config_dir, 'nbconfig'),
        )

    def init_logging(self):
        # This prevents double log messages because tornado use a root logger that
        # self.log is a child of. The logging module dipatches log messages to a log
        # and all of its ancenstors until propagate is set to False.
        self.log.propagate = False
        
        for log in app_log, access_log, gen_log:
            # consistent log output name (NotebookApp instead of tornado.access, etc.)
            log.name = self.log.name
        # hook up tornado 3's loggers to our app handlers
        logger = logging.getLogger('tornado')
        logger.propagate = True
        logger.parent = self.log
        logger.setLevel(self.log.level)
    
    def init_webapp(self):
        """initialize tornado webapp and httpserver"""
        self.tornado_settings['allow_origin'] = self.allow_origin
        if self.allow_origin_pat:
            self.tornado_settings['allow_origin_pat'] = re.compile(self.allow_origin_pat)
        self.tornado_settings['allow_credentials'] = self.allow_credentials
        self.tornado_settings['cookie_options'] = self.cookie_options
        # ensure default_url starts with base_url
        if not self.default_url.startswith(self.base_url):
            self.default_url = url_path_join(self.base_url, self.default_url)
        
        self.web_app = NotebookWebApplication(
            self, self.kernel_manager, self.contents_manager,
            self.session_manager, self.kernel_spec_manager,
            self.config_manager,
            self.log, self.base_url, self.default_url, self.tornado_settings,
            self.jinja_environment_options
        )
        ssl_options = self.ssl_options
        if self.certfile:
            ssl_options['certfile'] = self.certfile
        if self.keyfile:
            ssl_options['keyfile'] = self.keyfile
        if self.client_ca:
            ssl_options['ca_certs'] = self.client_ca
        if not ssl_options:
            # None indicates no SSL config
            ssl_options = None
        else:
            # SSL may be missing, so only import it if it's to be used
            import ssl
            # Disable SSLv3 by default, since its use is discouraged.
            ssl_options.setdefault('ssl_version', ssl.PROTOCOL_TLSv1)
            if ssl_options.get('ca_certs', False):
                ssl_options.setdefault('cert_reqs', ssl.CERT_REQUIRED)
        
        self.login_handler_class.validate_security(self, ssl_options=ssl_options)
        self.http_server = httpserver.HTTPServer(self.web_app, ssl_options=ssl_options,
                                                 xheaders=self.trust_xheaders)

        success = None
        for port in random_ports(self.port, self.port_retries+1):
            try:
                self.http_server.listen(port, self.ip)
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    self.log.info('The port %i is already in use, trying another port.' % port)
                    continue
                elif e.errno in (errno.EACCES, getattr(errno, 'WSAEACCES', errno.EACCES)):
                    self.log.warn("Permission to listen on port %i denied" % port)
                    continue
                else:
                    raise
            else:
                self.port = port
                success = True
                break
        if not success:
            self.log.critical('ERROR: the notebook server could not be started because '
                              'no available port could be found.')
            self.exit(1)
    
    @property
    def display_url(self):
        ip = self.ip if self.ip else '[all ip addresses on your system]'
        return self._url(ip)

    @property
    def connection_url(self):
        ip = self.ip if self.ip else 'localhost'
        return self._url(ip)

    def _url(self, ip):
        proto = 'https' if self.certfile else 'http'
        return "%s://%s:%i%s" % (proto, ip, self.port, self.base_url)

    def init_terminals(self):
        try:
            from .terminal import initialize
            initialize(self.web_app, self.notebook_dir, self.connection_url)
            self.web_app.settings['terminals_available'] = True
        except ImportError as e:
            log = self.log.debug if sys.platform == 'win32' else self.log.warn
            log("Terminals not available (error was %s)", e)

    def init_signal(self):
        if not sys.platform.startswith('win') and sys.stdin.isatty():
            signal.signal(signal.SIGINT, self._handle_sigint)
        signal.signal(signal.SIGTERM, self._signal_stop)
        if hasattr(signal, 'SIGUSR1'):
            # Windows doesn't support SIGUSR1
            signal.signal(signal.SIGUSR1, self._signal_info)
        if hasattr(signal, 'SIGINFO'):
            # only on BSD-based systems
            signal.signal(signal.SIGINFO, self._signal_info)
    
    def _handle_sigint(self, sig, frame):
        """SIGINT handler spawns confirmation dialog"""
        # register more forceful signal handler for ^C^C case
        signal.signal(signal.SIGINT, self._signal_stop)
        # request confirmation dialog in bg thread, to avoid
        # blocking the App
        thread = threading.Thread(target=self._confirm_exit)
        thread.daemon = True
        thread.start()
    
    def _restore_sigint_handler(self):
        """callback for restoring original SIGINT handler"""
        signal.signal(signal.SIGINT, self._handle_sigint)
    
    def _confirm_exit(self):
        """confirm shutdown on ^C
        
        A second ^C, or answering 'y' within 5s will cause shutdown,
        otherwise original SIGINT handler will be restored.
        
        This doesn't work on Windows.
        """
        info = self.log.info
        info('interrupted')
        print(self.notebook_info())
        sys.stdout.write("Shutdown this notebook server (y/[n])? ")
        sys.stdout.flush()
        r,w,x = select.select([sys.stdin], [], [], 5)
        if r:
            line = sys.stdin.readline()
            if line.lower().startswith('y') and 'n' not in line.lower():
                self.log.critical("Shutdown confirmed")
                ioloop.IOLoop.current().stop()
                return
        else:
            print("No answer for 5s:", end=' ')
        print("resuming operation...")
        # no answer, or answer is no:
        # set it back to original SIGINT handler
        # use IOLoop.add_callback because signal.signal must be called
        # from main thread
        ioloop.IOLoop.current().add_callback(self._restore_sigint_handler)
    
    def _signal_stop(self, sig, frame):
        self.log.critical("received signal %s, stopping", sig)
        ioloop.IOLoop.current().stop()

    def _signal_info(self, sig, frame):
        print(self.notebook_info())
    
    def init_components(self):
        """Check the components submodule, and warn if it's unclean"""
        # TODO: this should still check, but now we use bower, not git submodule
        pass

    def init_server_extensions(self):
        """Load any extensions specified by config.

        Import the module, then call the load_jupyter_server_extension function,
        if one exists.
        
        The extension API is experimental, and may change in future releases.
        """
        
        # TODO: Remove me in notebook 5.0
        for modulename in self.server_extensions:
            # Don't override disable state of the extension if it already exist
            # in the new traitlet
            if not modulename in self.nbserver_extensions:
                self.nbserver_extensions[modulename] = True
        
        for modulename in self.nbserver_extensions:
            if self.nbserver_extensions[modulename]:
                try:
                    mod = importlib.import_module(modulename)
                    func = getattr(mod, 'load_jupyter_server_extension', None)
                    if func is not None:
                        func(self)
                except Exception:
                    if self.reraise_server_extension_failures:
                        raise
                    self.log.warning("Error loading server extension %s", modulename,
                                  exc_info=True)

    def init_mime_overrides(self):
        # On some Windows machines, an application has registered an incorrect
        # mimetype for CSS in the registry. Tornado uses this when serving
        # .css files, causing browsers to reject the stylesheet. We know the
        # mimetype always needs to be text/css, so we override it here.
        mimetypes.add_type('text/css', '.css')

    @catch_config_error
    def initialize(self, argv=None):
        super(NotebookApp, self).initialize(argv)
        self.init_logging()
        if self._dispatching:
            return
        self.init_configurables()
        self.init_components()
        self.init_webapp()
        self.init_terminals()
        self.init_signal()
        self.init_server_extensions()
        self.init_mime_overrides()

    def cleanup_kernels(self):
        """Shutdown all kernels.
        
        The kernels will shutdown themselves when this process no longer exists,
        but explicit shutdown allows the KernelManagers to cleanup the connection files.
        """
        self.log.info('Shutting down kernels')
        self.kernel_manager.shutdown_all()

    def notebook_info(self):
        "Return the current working directory and the server url information"
        info = self.contents_manager.info_string() + "\n"
        info += "%d active kernels \n" % len(self.kernel_manager._kernels)
        return info + "The Jupyter Notebook is running at: %s" % self.display_url

    def server_info(self):
        """Return a JSONable dict of information about this server."""
        return {'url': self.connection_url,
                'hostname': self.ip if self.ip else 'localhost',
                'port': self.port,
                'secure': bool(self.certfile),
                'base_url': self.base_url,
                'notebook_dir': os.path.abspath(self.notebook_dir),
                'pid': os.getpid()
               }

    def write_server_info_file(self):
        """Write the result of server_info() to the JSON file info_file."""
        with open(self.info_file, 'w') as f:
            json.dump(self.server_info(), f, indent=2)

    def remove_server_info_file(self):
        """Remove the nbserver-<pid>.json file created for this server.
        
        Ignores the error raised when the file has already been removed.
        """
        try:
            os.unlink(self.info_file)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def start(self):
        """ Start the Notebook server app, after initialization
        
        This method takes no arguments so all configuration and initialization
        must be done prior to calling this method."""
        super(NotebookApp, self).start()

        info = self.log.info
        for line in self.notebook_info().split("\n"):
            info(line)
        info("Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).")

        self.write_server_info_file()

        if self.open_browser or self.file_to_run:
            try:
                browser = webbrowser.get(self.browser or None)
            except webbrowser.Error as e:
                self.log.warn('No web browser found: %s.' % e)
                browser = None
            
            if self.file_to_run:
                if not os.path.exists(self.file_to_run):
                    self.log.critical("%s does not exist" % self.file_to_run)
                    self.exit(1)

                relpath = os.path.relpath(self.file_to_run, self.notebook_dir)
                uri = url_escape(url_path_join('notebooks', *relpath.split(os.sep)))
            else:
                # default_url contains base_url, but so does connection_url
                uri = self.default_url[len(self.base_url):]
            if browser:
                b = lambda : browser.open(url_path_join(self.connection_url, uri),
                                          new=2)
                threading.Thread(target=b).start()
        
        self.io_loop = ioloop.IOLoop.current()
        if sys.platform.startswith('win'):
            # add no-op to wake every 5s
            # to handle signals that may be ignored by the inner loop
            pc = ioloop.PeriodicCallback(lambda : None, 5000)
            pc.start()
        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            info("Interrupted...")
        finally:
            self.cleanup_kernels()
            self.remove_server_info_file()
    
    def stop(self):
        def _stop():
            self.http_server.stop()
            self.io_loop.stop()
        self.io_loop.add_callback(_stop)


def list_running_servers(runtime_dir=None):
    """Iterate over the server info files of running notebook servers.
    
    Given a runtime directory, find nbserver-* files in the security directory,
    and yield dicts of their information, each one pertaining to
    a currently running notebook server instance.
    """
    if runtime_dir is None:
        runtime_dir = jupyter_runtime_dir()

    # The runtime dir might not exist
    if not os.path.isdir(runtime_dir):
        return

    for file in os.listdir(runtime_dir):
        if file.startswith('nbserver-'):
            with io.open(os.path.join(runtime_dir, file), encoding='utf-8') as f:
                info = json.load(f)

            # Simple check whether that process is really still running
            # Also remove leftover files from IPython 2.x without a pid field
            if ('pid' in info) and check_pid(info['pid']):
                yield info
            else:
                # If the process has died, try to delete its info file
                try:
                    os.unlink(file)
                except OSError:
                    pass  # TODO: This should warn or log or something
#-----------------------------------------------------------------------------
# Main entry point
#-----------------------------------------------------------------------------

main = launch_new_instance = NotebookApp.launch_instance

