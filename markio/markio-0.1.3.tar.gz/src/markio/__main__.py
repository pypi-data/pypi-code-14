import argparse
import markio
import ejudge


def make_parser():
    # Creates an argument parser.
    parser = argparse.ArgumentParser('markio')
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='valid commands',
        help='sub-command help',
    )

    # "markio run" command
    parser_run = subparsers.add_parser('run', help='run answer key code')
    parser_run.add_argument('input', help='input Markio file')
    parser_run.add_argument(
        '--debug', '-d',
        action='store_true',
        help='enable debugging mode'
    )
    parser_run.add_argument(
        '--lang', '-l',
        type=str,
        help='language of answer key'
    )
    parser_run.set_defaults(func=markio_run)

    return parser


def read_markio(path, debug=False):
    """
    Return a Markio AST from given args.
    """
    try:
        return markio.parse(path)
    except SyntaxError as ex:
        if debug:
            raise
        print('Error in markio file: ' + str(ex))
        raise SystemExit(1)


def markio_run(args):
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
    ejudge.exec(source, lang=lang)


def main(args=None):
    parser = make_parser()
    args = parser.parse_args(args)
    args.func(args)


# Executed with `python -m markio`
if __name__ == '__main__':
    main()