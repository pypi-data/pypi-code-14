import shellish

class Hello(shellish.InteractiveCommand):
    """ I am a required docstring used to document the --help output! """

    name = 'hello'


class World(shellish.Command):
    """ Say something. """

    name = 'world'

    def run(self, args):
        print('Hello World')


hello = Hello()
hello.add_subcommand(World)
hello()
