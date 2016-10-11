# noqa: E402
import os
import time
from subprocess import Popen
from signal import SIGINT
from socket import socket

import requests

from django.conf import settings
from django.core.management.base import BaseCommand

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit  # nopep8


class Proton(object):
    """
    Run a Django app without using a web browser (similar to Electron).
    Settings are loaded from the main project's settings.py file.
    The following settings must be defined:

    WINDOW_TITLE: a string containing the label for the window
    WINDOW_SIZE: a tuple of integers representing the default width/height
    WINDOW_MAXIMIZE: whether the window should be maximized by default
    """

    def __init__(self):
        # pick a free port
        sock = socket()
        sock.bind(('', 0))  # port 0 means 'let the OS find me one'
        self.port = sock.getsockname()[1]
        # per the docs, getsockname() returns (addr, port) for IPv4
        # and (addr, port, flow, scope) for IPv6.
        sock.close()

        self.URL = "http://localhost:%d" % self.port

        self.window = Gtk.Window()
        scrolled_window = Gtk.ScrolledWindow()
        self.webview = WebKit.WebView()
        scrolled_window.add(self.webview)
        self.window.add(scrolled_window)
        self.window.set_wmclass(settings.WINDOW_TITLE, settings.WINDOW_TITLE)
        self.window.set_title(settings.WINDOW_TITLE)
        self.window.set_default_size(*settings.WINDOW_SIZE)
        self.window.connect('destroy', self.cb_window_destroy)

    def run(self):
        command = ['python',
                   os.path.join(settings.BASE_DIR, 'manage.py'),
                   'runserver',
                   str(self.port)]
        self.server = Popen(command, preexec_fn=os.setsid)
        self.waitForServer()
        self.webview.load_uri(self.URL)
        self.window.show_all()
        if settings.WINDOW_MAXIMIZE:
            self.window.maximize()
        Gtk.main()

    def waitForServer(self):
        while True:
            try:
                requests.head(self.URL)
            except requests.exceptions.ConnectionError:
                time.sleep(0.5)
            else:
                break

    def cb_window_destroy(self, *args):
        os.killpg(os.getpgid(self.server.pid), SIGINT)
        Gtk.main_quit()


class Command(BaseCommand):
    help = "Runs the app in a window"

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        Proton().run()
