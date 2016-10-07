import os
import sys
import logging
from functools import partial, wraps

# Begin exports.
from . import input, output, render, exceptions
from . import templates
from .util import config_template, CallableDict
from .signature import COUNT
from .exceptions import Error

logger = logging.getLogger(__name__)

def _config(name, override):
    if override:
        return override

    if name:
        envvar = '%s_CONFIG' % name.upper()
        if envvar in os.environ:
            return os.environ[name]

def Interface(function, config_file, config_sep, i):
    '''
    :param i: Function that takes no arguments and returns an input.Input
    '''
    try:
        body = output.Output(config_file, config_sep, function, i())
    except exceptions.HoretuException as e:
        body = e
    return body

def wsgi(function, url=None,
         name=None, config_file=None, config_sep=None,
         default_content_type='text/plain; charset=UTF-8', debug=False):
    '''
    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config_file: str or None
    :param config_file: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    :param str name: Name of the program, used for environment variable settings
        If it is ``None`` (the default), we attempt to get the name from the function.
    :param str url: If this is set, simply evaluate the function for that particular URL,
        rather than creating a WSGI application. This is nice for testing.
    :param str default_content_type: Content-Type with which pages should be served
    :param bool debug: Print errors and debugging information to web pages?
    :rtype: function
    :returns: WSGI application
    '''
    import traceback
    try:
        from webob import Response
    except ImportError:
        logger.error('WebOb is not installed; run this: pip install horetu[all]')
        sys.exit(1)
  

    if not config_file:
        if hasattr(function, '__call__') and not name:
            name = function.__name__
        config_file = _config(name, config_file)

    def app(environ, start_response):
        res = Response()
        i = partial(input.wsgi, function, environ)
        try:
            out = Interface(config_file, config_sep, function, i)
        except Exception:
            if debug:
                res.content_type = 'text/plain; charset=UTF-8'
                body = [traceback.format_exception().encode('utf-8')]
            else:
                raise

        if isinstance(out, exceptions.HoretuCouldNotParse):
            res.status = 404
            wr = render.wsgi.usage(function, out)
        elif isinstance(out, exceptions.HoretuShowHelp):
            res.status = 200
            wr = render.wsgi.man(function, out)
        elif isinstance(out, exceptions.HoretuError):
            res.status = 400
            out2 = out
            if isinstance(out2, render.wsgi.WebResponse):
                wr = out2
            else:
                wr = render.wsgi.WebResponse(default_content_type, out2)
        else:
            res.status = 200
            if isinstance(out, render.wsgi.WebResponse):
                wr = out
            else:
                wr = render.wsgi.WebResponse(default_content_type, out)

        if wr.content_type.lower().startswith('text/plain'):
            res.app_iter = (chunk + b'\n' for chunk in wr.data)
        else:
            res.app_iter = wr.data
        res.content_type = wr.content_type
        return res(environ, start_response)
    return app

def cli(function, argv=sys.argv, return_=False,
        name=None, config_file=None, config_sep=None,
        exit_=sys.exit, stdout=sys.stdout.buffer, stderr=sys.stderr.buffer):
    '''
    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config_file: str or None
    :param config_file: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    :param str name: Name of the program (``$0``), for usage text and
        environment variables. If it is ``None`` (the default), we
        use the following instead.
       
        1. If a function, rather than a list or dictionary, is passed as ``f``,
           use the function's name (``f.__name__``).
        2. Otherwise, use the first argv (``sys.argv[0]``).
    :param list argv: :py:obj:`sys.argv` by default
    :param bool return_: If this is ``True``, simply return the result of the function;
        do not write stuff to ``exit_``, ``stdout``, or ``stderr``.
    :param function exit_: :py:func:`sys.exit` by default
    :type stdout: Binary file
    :param stdout: :py:func:`sys.stdout.buffer` by default
    :type stderr: Binary file
    :param stderr: :py:func:`sys.stderr.buffer` by default
    '''
    argv = list(argv) # Prevent myself from modifying the input.

    if name is None:
        if hasattr(function, '__call__'):
            name = function.__name__
        else:
            name = os.path.basename(argv[0])
    config_file = _config(name, config_file)

    try:
        out = Interface(function, config_file, config_sep,           # pass through
                        partial(input.cli, function, argv[1:])) # input
    except exceptions.Error as e:
        out = e

    code = 0
    fp = stdout
    if isinstance(out, exceptions.HoretuException):
        if not out.ok:
            fp = stderr

        if isinstance(out, exceptions.HoretuShowHelp):
            app_iter = templates.AppIter(render.cli.man(name, function, out))
        else:
            if isinstance(out, exceptions.HoretuCouldNotParse):
                code = 2
            else:
                code = 1
            app_iter = templates.AppIter(render.cli.usage(name, function, out))
    else:
        app_iter = out

    try:
        for line in app_iter:
            fp.write(line + b'\n')
    except BrokenPipeError:
        stderr.close()
    except exceptions.Error as e:
        stdout.buffer.write(e.message.rstrip('\n').encode('utf-8') + b'\n')
    exit_(code)

@wraps(cli)
def horetu(*args, **kwargs):
    logger.warn('The horetu.horetu interface is deprecated; use horetu.cli.')

    if 'description' in kwargs:
        del(kwargs['description'])

    if 'args' in kwargs:
        kwargs['argv'] = sys.argv[:1] + kwargs.pop('args')

    return cli(*args, **kwargs)

def irc(function, config=None, config_sep=' ',
        ):
    '''
    Render Python functions as an IRC bot.

    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config: str or None
    :param config: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    '''
    raise NotImplementedError

def webcli(function, config=None, config_sep=' '):
    '''
    Render Python functions as text terminal website.

    :type f: Callable, list, or dict
    :param f: The callable to produce the argument parser too,
        or a dict of (dicts of...) str to callable to make subparsers.
    :type config: str or None
    :param config: Configuration file location, or None to disable
    :param str config_sep: Separator character between command and
        subcommand names in the configuration file (Default is " ".)
    '''
    raise NotImplementedError
