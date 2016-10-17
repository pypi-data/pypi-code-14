import logging

from umodules.command import ICommand


class Install(ICommand):

    def run(self, project):
        pass

    def build(self, subparser):
        super().build(subparser)
        cmd = subparser.add_parser("new", help="...")
        cmd.set_defaults(func=self.run)
        logging.debug("- command [new] has been added to argparse")

    def activate(self):
        super().activate()

