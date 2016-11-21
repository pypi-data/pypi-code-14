"""
Huzz.

Usage:
    huzz [--seed=<randomseed>]
    huzz -h | --help

Options:
    -h --help               Show this screen.
    -s --seed=<randomseed>  Use <randomseed> to initialise RNG.
"""
from docopt import docopt
from random import randint

from .version import VERSION
from .namers import DefaultNamer
from .function_generator import generate_functions
from .code_gen import codeify_functions


def huzzer(seed):
    # get random tree
    functions = generate_functions(seed)

    # get naming generator
    namer = DefaultNamer()
    print(codeify_functions(functions, namer))


def main():
    arguments = docopt(__doc__, version=VERSION)
    randomseed_str = arguments.get('--seed')

    if randomseed_str is not None:
        try:
            randomseed = int(randomseed_str)
        except Exception:
            print('error: randomseed needs to be an integer, got: ' + randomseed_str)
    else:
        randomseed = randint(0, 1 << 16)

    huzzer(randomseed)


if __name__ == '__main__':
    main()
