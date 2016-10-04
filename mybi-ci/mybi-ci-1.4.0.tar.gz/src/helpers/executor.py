__author__ = 'marcoantonioalberoalbero'

import optparse
import os.path
import sys
from helpers.loader import Loader
from helpers.valdano import Log
from helpers.env import read_config
from server.server import Server

# Support vars.
ENDL = "\n"
usage = """
\twhere options are:
\t\t -s => server mode, start a server for receiving jobs
\t\t -b build_file.json => build
\t\t -t build_file.json => test config
"""


class Executor:
    """ Class for execute the ci engine """
    def __init__(self):
        self.parser = optparse.OptionParser(usage='usage: %prog [options]'+usage)
        self.parser.add_option('-b', '--build', action='store_true', default=False, help='build mode')
        self.parser.add_option('-t', '--test', action='store_true', default=False, help='test mode')
        self.parser.add_option('-s', '--server', action='store_true', default=False, help='server mode')
        self.config = read_config()
        self.logger = Log().setup(config=self.config, task_id=__name__)

    def run(self, args):
        (options, arguments) = self.parser.parse_args(args)

        if options.server:
            Server.run()
            sys.exit(0)

        if (options.test or options.build) and len(args) == 2:
            file_path = args[1]
            op = "Testing " if options.test else "Building "
            if os.path.isfile(file_path):
                Log.id_log(self.logger, op + args[1])
                task = Loader.load_from_file(file_path)
            else:
                Log.id_log(self.logger, str(args[1]) + " is not a valid file")
                sys.exit(0)
            if options.build:
                Log.id_log(self.logger, "Running " + args[1])
                task.run()
                Log.id_log(self.logger, "Your build ID: "
                           + os.environ['MYBICI_BUILD_ID'] +
                           " has finished with status: " + str(task.finish_status))
            sys.exit(0)

        self.parser.print_usage()
