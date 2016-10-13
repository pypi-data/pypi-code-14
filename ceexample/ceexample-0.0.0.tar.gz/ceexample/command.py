from celery.bin.base import Command


class ExampleCommand(Command):
    def run_from_argv(self, prog_name, argv=None, command=None):
        print "run_from_argv called...."
