#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tools to export data from elasticsearch"""
import six
import os
import sys
import re
import logging
import argparse
import json
import warnings
from six.moves import reduce
from datetime import datetime, timedelta
from contextlib import contextmanager
from elasticsearch import Elasticsearch, helpers, NotFoundError
from elasticsearch.client import IndicesClient

__version__ = '0.0.14'
MAX_TIME_SPAN = timedelta(hours=2)


# ##############################
# types  command

def types_command(env):
    """top level command associated with the 'types' command line argument"""
    try:
        with elasticsearch_config(env) as es_config:
            doc_types = get_doc_types(es_config, env.index)
            rows = [[mapping, ", ".join(fmt_interval(s, e) for s, e in intervals)]
                    for mapping, intervals in six.iteritems(doc_types)]
            with env.output_file as out:
                out.write(fmt_table(rows, "><"))
    except NotFoundError:
        logging.error("Index Not Found")
        sys.exit(4)


def get_doc_types(es_config, base_name):
    """returns a dictionary with document types as keys and the days of the indices they are present"""
    mappings = get_mappings(es_config, base_name + "_*")
    by_doc_type = group_by(mappings, lambda x: x[0], lambda x: x[1])
    intervals_by_doc_type = {k: list(to_intervals(set(v))) for k, v in six.iteritems(by_doc_type)}
    return intervals_by_doc_type


def get_mappings(es_config, base_name):
    """returns the elasticsearch mappings in form of a generator of (mapping name, date) tuples"""
    client = IndicesClient(es_config)
    doc = client.get_mapping(base_name)

    for index, conf in six.iteritems(doc):
        match = re.search(r'([a-z_]+)_(v[0-9]+)-([0-9]{4}\.[0-9]{2}\.[0-9]{2})', index)
        _base, _version, date = match.group(1, 2, 3)
        for mapping, _ in six.iteritems(conf['mappings']):
            if mapping == '_default_':
                continue
            yield mapping, datetime.strptime(date, "%Y.%m.%d")


def to_intervals(items):
    """converts a list of individual dates into a list of time intervals of these dates."""
    one = timedelta(days=1)
    sorted_items = sorted(items)
    previous = start = sorted_items[0]
    for item in sorted_items[1:]:
        if item != previous + one:
            yield start, previous
            start = item
        previous = item
    yield start, previous


def fmt_interval(interval_start, interval_end):
    """string formatting for pairs of dates"""
    if interval_start == interval_end:
        return "{0:%Y.%m.%d}".format(interval_start)
    else:
        return "{0:%Y.%m.%d}-{1:%Y.%m.%d}".format(interval_start, interval_end)


# ##############################
# export command

def export_command(env):
    """top level command associated with the 'export' command line argument"""
    try:
        with elasticsearch_config(env) as es_config:
            for start, end in daily_interval_sequence(env.start, env.end):
                query = 'header.indexTimestamp:[{0} TO {1}}}{2}'.format(
                    start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    end.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    " AND " + env.query if env.query else "")
                index = "{0}-{1}".format(env.index, start.strftime("%Y.%m.%d"))

                logging.info("querying %s  %s", start, end)

                if env.fields:
                    query_fields(env, es_config, index, query)
                else:
                    query_source(env, es_config, index, query)
    except NotFoundError:
        logging.error("Index Not Found")
        sys.exit(4)


def query_source(env, es_config, index, query):
    """issue the query and return the json source message"""
    results = helpers.scan(es_config, index=index, doc_type=env.doc_type, q=query, scroll='1m')
    if env.top:
        results = (item for item, _ in zip(results, range(env.top)))
    with env.output_file as out:
        for item in results:
            source = item['_source']
            out.write(json.dumps(source, separators=(',', ':')).replace('\n', '\\n'))
            out.write('\n')


def query_fields(env, es_config, index, query):
    """issue the query with a fields parameter and return the values in the 'fields' json property"""
    results = helpers.scan(es_config, index=index, doc_type=env.doc_type,
                           q=query, fields=env.fields, scroll='1m')
    if env.top:
        results = (item for item, _ in zip(results, range(env.top)))
    with env.output_file as out:
        for item in results:
            fields = item.get('fields', {})
            row = [escape(fields.get(field, [""])[0]) for field in env.fields]
            out.write("\t".join(row))
            out.write('\n')


def daily_interval_sequence(start, end):
    """a sequence of time intervals between start and end, broken down into days
    the first day might be partial and starts at the given start
    the last day might be partial and ends at the given end
    """
    delta = timedelta(days=1)
    current = start
    while current < end:
        next_midnight = (current + delta).replace(hour=0, minute=0, second=0, microsecond=0)
        yield current, next_midnight if next_midnight < end else end
        current = next_midnight


# ##############################
# utility functions

def escape(text):
    """replace tabs and line feeds with escaped"""
    return str(text).replace('\n', '\\n').replace('\t', '\\t')


def group_by(items, get_key, get_value):
    """simple group by that doesn't require the input to be sorted"""
    result = {}
    for item in items:
        result.setdefault(get_key(item), []).append(get_value(item))
    return result


def fmt_table(rows, columns):
    """given a list of list of strings it formats them into a table
    format with fixed column widths
    :param rows: a list of lists of strings to be formatted
    :param columns format specifier, on character per column, each one of < ^ > as in string.format"""
    widths = reduce(lambda xs, ys: [max(x, len(y)) for x, y in zip(xs, ys)], rows, [1 for _ in columns])
    return "\n".join(
        " ".join("{0:{1}{2}}".format(c, a, w)
                 for c, a, w in zip(row, columns, widths)) for row in rows) + "\n"


@contextmanager
def elasticsearch_config(env):
    """context manager that suppresses urllib warnings and return an elasticsearch config"""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        urls = [env.url]
        auth = (env.username, env.password)
        config = Elasticsearch(urls, http_auth=auth, use_ssl=True, verify_certs=False)
        yield config


# ##############################
# command line

def main():
    """main program that parses command line and invokes the specified command"""
    try:
        # create parser
        parser = argparse.ArgumentParser(
            fromfile_prefix_chars='@',
            description="A tool to export data from elasticsearch",
            epilog="Please contact #analytics for questions and feedback. Version {0}".format(__version__))

        parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(__version__))
        add_common_options(parser)

        subparsers = parser.add_subparsers(title='commands')
        add_types_parser(subparsers)
        add_export_parser(subparsers)

        # parse
        env = parser.parse_args()

        # setup logging
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%m%:%S",
                            level=env.loglevel or logging.INFO)

        logging.getLogger('urllib3').setLevel(logging.CRITICAL)
        logging.getLogger('requests.packages.urllib3').setLevel(logging.WARN)
        logging.getLogger('elasticsearch.trace').addHandler(logging.NullHandler())
        logging.debug("%s", dict((k, v if k is not 'password' else '<???>') for k, v in six.iteritems(vars(env))))

        # verify some requirements not easily expressible in argparse
        if not env.username:
            logging.error("username is required and can be set via --username or ELASTICSEARCH_USERNAME.\n\n%s",
                          parser.format_help())
            parser.exit(2, "username is required\n")

        if not env.password:
            logging.error("password is required and can be set via --password or ELASTICSEARCH_PASSWORD.\n\n%s",
                          parser.format_help())
            parser.exit(3, "password is required\n")

        if not env.url:
            logging.error("elasticsearch URL is required and can be set via --url or ELASTICSEARCH_URL\n\n%s",
                          parser.format_help())
            parser.exit(3, "url is required\n")

        if env.command == export_command and env.end - env.start > MAX_TIME_SPAN:
            if env.force:
                logging.warn("querying for long time span %s.", env.end - env.start)
            else:
                logging.error("time span %s is longer than maximum of %s. Add --force to run",
                              env.end - env.start, MAX_TIME_SPAN)
                parser.exit(4, "time span too long\n")

        # run the selected command
        return env.command(env)
    except KeyboardInterrupt:
        logging.exception('Keyboard interrupt')
        sys.exit(2)
    except Exception as ex:
        logging.exception('internal error\n%s', ex)
        sys.exit(1)


def add_common_options(parser):
    """create sub parser for common options"""
    common_group = parser.add_argument_group('common')
    common_group.add_argument('--username', default=os.environ.get('ELASTICSEARCH_USERNAME'),
                              help="user name, defaults to ELASTICSEARCH_USERNAME")
    common_group.add_argument('--password', default=os.environ.get('ELASTICSEARCH_PASSWORD'),
                              help="password, defaults to ELASTICSEARCH_PASSWORD")
    common_group.add_argument('--output', type=argparse.FileType('w'), default=sys.stdout, dest='output_file',
                              metavar='FILE',
                              help="output file. defaults to stdout")
    common_group.add_argument('--force', default=False, action='store_true',
                              help="allow to query for time span over %s" % MAX_TIME_SPAN)
    common_group.add_argument('--url',
                              default=os.environ.get('ELASTICSEARCH_URL'),
                              help="elasticsearch url. Defaults to ELASTICSEARCH_URL")
    #  DEBUG lines will be printed/logged if --verbose (-v) command line argument is used.
    #  WARN log entries should be printed even if the --quiet (-q) command line flag is used.
    group = common_group.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_const', const=logging.DEBUG, dest='loglevel',
                       help='Verbose (debug) logging')
    group.add_argument('-q', '--quiet', action='store_const', const=logging.WARN, dest='loglevel',
                       help='Silent mode, only log warnings')


def add_export_parser(subparsers):
    """create sub parser for export command options"""
    def valid_date(datetime_string, date_format="%Y-%m-%d %H:%M:%S"):
        """string parser for dat command line arguments"""
        try:
            return datetime.strptime(datetime_string, date_format)
        except ValueError:
            msg = "Not a valid date: '{0}'. Required format is {1}".format(datetime_string, format)
            raise argparse.ArgumentTypeError(msg)

    def top_of_hour():
        """round down to top of hour of the current time"""
        return datetime.now().replace(minute=0, second=0, microsecond=0)

    def hour_before_top_of_hour():
        """return the hour before top of hour"""
        return top_of_hour() - timedelta(hours=1)

    export_parser = subparsers.add_parser('export', help='export the data from a query')
    export_parser.set_defaults(command=export_command)
    export_parser.add_argument('index',
                               help="index pattern (without the appended date)")
    export_parser.add_argument('doc_type',
                               help="full document type (including version)")
    export_parser.add_argument('query', nargs='?', default='',
                               help="query in lucence syntax. See https://goo.gl/n9zJSx")
    export_parser.add_argument('-f', '--fields', default=None, nargs='+',
                               help="list of fields")
    export_parser.add_argument('-s', '--start', default=hour_before_top_of_hour(), type=valid_date,
                               help="start time for query")
    export_parser.add_argument('-e', '--end', default=top_of_hour(), type=valid_date,
                               help="end time for query")
    export_parser.add_argument('-t', '--top', default=None, type=int,
                               help="only return the first TOP items")
    return export_parser


def add_types_parser(subparsers):
    """create sub parser for 'types' command options"""
    types_parser = subparsers.add_parser('types', help='return a list of document types')
    types_parser.set_defaults(command=types_command)
    types_parser.add_argument('index',
                              help="index pattern (without the appended date)")
    return types_parser
