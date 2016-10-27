from .SMBase import SMBase
from .Types import Types

import subprocess
import sys
import logging

""" A class to keep track of server scans.
This is so that they can be collected into a list and re-run or
queried after the fact.
"""

class Scan(SMBase):
    """an object to keep track of a scan on a server"""

    def __init__(self, host, stype):
        """Initalize a scan object."""
        self.host = host
        self.stype = stype
        # get the command for the type
        self.reporter = Type.find_reporter(stype)
        pass

    def remote_run(self, cmd):
        """Run a command on the host for the class."""
        ssh = subprocess.Popen(["ssh", "%s" % self.host, cmd],shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            logging.warning("[ssh err: " + self.host +"]" + error)
            return "ssh-err"
        else:
            return join(result)

    def scan(self):
        """Run the scan."""
        # check if host is reachable
        # run the command
        for report in self.reporter:
            # add result to end of that report
            report.append(self.remote_run(report[1]))
        return self.reporter
