import argparse

import sys


def make_parser():
    def add_params(parser, input=False, debug=False, lang=False):
        if input:
            parser.add_argument('input', help='input Markio file')
        if debug:
            parser.add_argument(
                '--debug', '-d',
                action='store_true',
                help='enable debugging mode'
            )
        if lang:
            parser.add_argument(
                '--lang', '-l',
                type=str,
                help='language of answer key'
            )

    # Creates an argument parser.
    parser = argparse.ArgumentParser('markio')
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid commands',
        help='sub-command help',
    )

    # "markio run" sub-command
    parser_run = subparsers.add_parser('run',
                                       help='run answer key code')
    add_params(parser_run, input=True, debug=True, lang=True)
    parser_run.set_defaults(func=markio_run)

    # "markio src" sub-command
    parser_src = subparsers.add_parser('src',
                                       help='extract source code from files')
    add_params(parser_src, input=True, debug=True, lang=True)
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='output file'
    )
    parser_src.set_defaults(func=markio_src)

    return parser


def read_markio(path, debug=False):
    """
    Return a Markio AST from given args.
    """

    import markio
    try:
        return markio.parse(path)
    except SyntaxError as ex:
        if debug:
            raise
        print('Error in markio file: ' + str(ex))
        raise SystemExit(1)


def markio_extract_source(args):
    """
    Return source data from given arguments.

    Common functionality of run/src commands.
    """

    md = read_markio(args.input, args.debug)

    # Select language
    if not args.lang and not md.answer_key:
        print('Error: No answer key defined!')
        raise SystemExit(1)
    elif not args.lang and len(md.answer_key) != 1:
        langs = set(md.answer_key)
        print('Error: could not choose language. Select --lang=X for X in %s.' %
              langs)
        raise SystemExit(1)
    elif not args.lang:
        lang = next(iter(md.answer_key))
    else:
        lang = args.lang.lower()

    # Run source code
    source, = md.answer_key.values()
    return source, lang


def markio_run(args):
    """
    `markio run <file>` command.
    """

    import ejudge
    source, lang = markio_extract_source(args)
    ejudge.exec(source, lang=lang)


def markio_src(args):
    """
    `markio src <file>` command.
    """

    source, lang = markio_extract_source(args)
    if args.output:
        with open(args.output, 'w', encoding='utf8') as F:
            F.write(source)
    else:
        print(source)


def main(args=None):
    parser = make_parser()
    args = parser.parse_args(args)

    try:
        args.func(args)
    except AttributeError:
        raise SystemExit('Please select a command. Type `markio -h` for help.')

# Executed with `python -m markio`
if __name__ == '__main__':
    main()
