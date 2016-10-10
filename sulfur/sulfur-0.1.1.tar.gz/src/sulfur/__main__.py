import argparse
import sulfur


# Create an argument parser.
parser = argparse.ArgumentParser('sulfur')


def main(args=None):
    """
    Main entry point for your project.

    Parameters:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None use sys.argv.
    """

    args = parser.parse_args(args)

    print('Not implemented yet! ;)')
    raise SystemExit


if __name__ == '__main__':
    main()