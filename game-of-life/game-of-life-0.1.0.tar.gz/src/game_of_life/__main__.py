import argparse
import game_of_life
from game_of_life import __version__


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser('Game of Life')
    version = '%(prog)s ' + __version__
    parser.add_argument('--version', '-v', action='version', version=version)
    parser.add_argument('--size', '-s', type=int, help_text='Grid size')

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
    args = parser.parse_args()
    world = game_of_life.World(args.size,
                               alive_color=(0, 230, 0),
                               draw_grid=True)
    world.run()


if __name__ == '__main__':
    main()
