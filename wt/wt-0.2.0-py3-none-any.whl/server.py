# -*- coding: utf-8 -*-

import os
import glob
import logging
import multiprocessing as mp
import time
import subprocess
import sys
import string
import traceback
import urllib.parse
from pathlib import Path

from aiohttp import web, FileSender

from .blog import blog


logger = logging.getLogger(__name__)

SERVER_ERROR = string.Template(
    """
    <html>
    <head>
    <title>Server Error (500)</title>
    </head>
    <body>
    <h3>${title}</h3>
    <pre>${error}</pre>
    </body>
    </html>
    """
)


async def aiohttp_handler(request):
    b = blog(request.app['config'])
    try:
        content = b.render(request.path, request.headers)
    except b.NotFound:
        sender = FileSender()
        path = urllib.parse.urldefrag(request.path)[0]
        path = path.split('?', 1)[0]
        path = urllib.parse.unquote(path)
        path = os.path.normpath(path)
        path = filter(None, path.split('/'))
        filename = os.path.join(b.static_root, *path)
        try:
            ret = await sender.send(request, Path(filename))
            return ret
        except FileNotFoundError as err:
            content = b.render_html('404.html', request=request)
            return web.Response(
                status=404, text=content, content_type='text/html')
    except Exception as exc:
        logger.error('Error rendering page', exc_info=True)
        content = traceback.format_exc()
        return web.Response(
            status=500,
            text=SERVER_ERROR.substitute(error=content, title=str(exc)),
            content_type='text/html')
    ct = ('text/xml'
          if request.path.endswith('.xml') else 'text/html')
    return web.Response(text=content, content_type=ct)


def aiohttp_app(config_filename, loop=None):
    app = web.Application(logger=logger, loop=loop)
    app.router.add_route('GET', '/', aiohttp_handler)
    app.router.add_route('GET', '/{p:.*}', aiohttp_handler)
    app['config'] = config_filename
    return app


def code_changed():  # pragma: no cover
    mtime = time.time()
    cwd = os.path.abspath(os.path.dirname(__file__))

    while True:
        files = glob.iglob(os.path.join(cwd, '**', '*.py'), recursive=True)
        changed = False
        for fn in files:
            _mtime = os.stat(fn).st_mtime
            if _mtime > mtime:
                mtime = _mtime
                changed = True
                break
        yield changed


def redirect_stdout(stdout):  # pragma: no cover
    while True:
        try:
            data = os.read(stdout.fileno(), 2**15)
        except KeyboardInterrupt:
            break
        if len(data) > 0:
            sys.stdout.write(data.decode('utf-8'))


def server(config, host, port):  # pragma: no cover

    if os.environ.get('IS_WT_CHILD') == 'yes':
        app = aiohttp_app(config)
        logger.debug('Server started at %s:%s...', host, port)
        return web.run_app(app, host=host, port=port)

    checker = code_changed()

    def run():
        env = os.environ.copy()
        env['IS_WT_CHILD'] = 'yes'
        p = subprocess.Popen(sys.argv[:],
                             env=env,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)

        t = mp.Process(target=redirect_stdout, args=(p.stdout,))
        t.start()
        return p, t

    p, t = run()

    try:
        while True:
            if next(checker):
                logger.debug('wt code changed, restarting server...')
                t.terminate()
                time.sleep(0.1)
                p.terminate()
                time.sleep(0.3)
                p, t = run()
            time.sleep(0.3)
    except KeyboardInterrupt:
        p.terminate()
    return 0
