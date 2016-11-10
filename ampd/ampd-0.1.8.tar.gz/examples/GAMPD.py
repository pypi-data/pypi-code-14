# coding: utf-8

# Asynchronous Music Player Daemon client library for Python

# Copyright (C) 2015 Itaï BEN YAACOV

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gio
import pprint
import sys
import ampd


class App(Gio.Application):
    def __init__(self):
        super(App, self).__init__()
        self.connect('startup', self.startup_cb)
        self.connect('shutdown', self.shutdown_cb)
        self.connect('activate', self.prompt)

    @staticmethod
    def startup_cb(self):
        self.client = ampd.ClientGLib()
        self.client.connect_to_server()
        self.ampd_worker_group = self.client.new_worker_group()
        self.hold()

    @staticmethod
    def shutdown_cb(self):
        self.client.close()
        self.disconnect_by_func(self.startup_cb)
        self.disconnect_by_func(self.shutdown_cb)
        self.disconnect_by_func(self.prompt)

    @staticmethod
    @ampd.worker
    def prompt(self):
        PROMPT = 'ampd: '
        yield ampd.CONNECT
        print('Connected')
        while True:
            try:
                try:
                    command = input(PROMPT) if sys.version_info >= (3, 0) else raw_input(PROMPT)
                except EOFError:
                    command = None
                if not command:
                    self.release()
                    return
                command = eval(command, vars(ampd))
            except:
                sys.excepthook(*sys.exc_info())
                continue
            try:
                try:
                    reply = yield command
                except DeprecationWarning as reply:
                    print('Warning: \"%s\" is deprecated' % command.split(' ')[0])
                    reply = reply.message
                MyPrettyPrinter().pprint(reply)
            except GeneratorExit:
                print('Disconnected')
                break
            except Exception as e:
                print('ERROR:', e)
                self.release()
                raise


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, str):
            return (obj, True, False)
        return pprint.PrettyPrinter.format(self, obj, context, maxlevels, level)


App().run()
