"""The class to handle all general invocations of the application.

Though everthing is customizable, it makes sense to have
an object keep track of all of its components.
This includes both the CLI and the python calling methods."""

from .SMBase import SMBase
from .Scan import Scan
from .Format import Format
from .Send import Send
from .Types import Types
import argparse

class Caller(SMBase):
    """A class for general invocation of statmail."""

    def __init__(self, hosts="127.0.0.1", email="root@127.0.0.1",
                 stype="minimal"):
        """The standard python init call for statmail."""
        # parse input
        self.stype = stype
        if type(hosts) is str:
            hosts = [hosts]
        self.hosts = hosts
        # check if type is supported
        if not Types.supported(stype):
            raise ValueError("The specified type is unspported.")
        # get email
        self.email = email

    def run(self):
        """Track objects and run standard."""
        self.scans = []
        for host in self.hosts:
            scanner = Scan(host[0], self.stype)
            # pass arguments at scan level
            self.scans.append(scanner.scan(host[2]))
        self.formatter = Format(self.scans, self.stype)
        self.sender = Send(self.email)
        self.status = self.sender.send(self.formatter.out())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Email a server \
                                     report.")
    parser.add_argument("email", metavar="Email", type=str, nargs="1")
    parser.add_argument("stype", metavar="Type", type=str, nargs="1")
    parser.add_argument("hosts", metavar="Host", type=str,
                        nargs=argparse.REMAINDER, action="append")
    args = parser.parse_args()
    caller = Caller(args.hosts, args.email, args.stype)
