import argparse
import hope_of_ropes
from hope_of_ropes import __version__

light = False

class LightAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        global light
        light = True

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Hope of Ropes')
    version = '%(prog)s ' + __version__
    parser.add_argument('--version', '-v', action='version', version=version)
    parser.add_argument('--light', '-l', action=LightAction)
    return parser

def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """
    parser = get_parser()
    args = parser.parse_args(args)

    # Put your main script logic here
    if light:
        from .light_simul import start_simul
        start_simul()
    else:
        from .elastic import start_simul
        start_simul()    


if __name__ == '__main__':
    main()