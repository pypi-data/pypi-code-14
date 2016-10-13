# -*- coding: utf-8 -*-

import argparse
from logging import getLogger
from logging import StreamHandler
from logging import INFO

import poetry
from poetry.haiku import Haiku
from poetry.data_constructor.words_data_constructor import WordsDataConstructor
from poetry.utils.data_reader import DataReader
from poetry.utils.data_exporter import DataExporter


logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

OUTPUT_DIR = poetry.__path__[0] + '/output/'
WORDS_FIVE_FILE_NAME = 'words_five.pickle'
WORDS_SEVEN_FILE_NAME = 'words_seven.pickle'


def cmd_prep(args):
    logger.info("Preprocessing")
    logger.info("Loading <- {0}".format(args.filename))

    read_data = DataReader.read_file(args.filename)

    wdc = WordsDataConstructor()
    words_data = wdc.construct_data(read_data)

    de = DataExporter(words_five_data=words_data['five'],
                      words_seven_data=words_data['seven'])
    de.export_pickle()

    logger.info("Exported")


def cmd_compose(args):
    Haiku.compose()


def main():
    parser = argparse.ArgumentParser(description='Haiku composer.')

    subparsers = parser.add_subparsers()

    # データ作成
    prep_parser = subparsers.add_parser('prep',
                                        help='Preprocessing for corpus.')
    prep_parser.add_argument('filename',
                             type=str,
                             help='Corpus file name.')
    prep_parser.set_defaults(func=cmd_prep)

    # 詠む
    compose_parser = subparsers.add_parser('compose',
                                           help='Compose rhyming haiku.')
    compose_parser.set_defaults(func=cmd_compose)

    args = parser.parse_args()

    try:
        # args.db = db
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    finally:
        # db.close()
        pass


if __name__ == '__main__':
    main()
