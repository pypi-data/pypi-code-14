from ..cli import *
from ..api import *
import click
import datetime


@cli.command('search')
@click.argument('filter', default='')
@click.option('--format', help='return specific fields', type=str)
@click.option('--period', help='search back this number of minutes', type=int, default=120)
def search(filter, format, period):

    """searches events"""
    start_date = datetime.datetime.now() - datetime.timedelta(minutes=period)
    end_date = datetime.datetime.now()
    events = get_events(url=context.settings['url'], bucket='syslog', start_date=start_date, end_date=end_date, filter=filter)

    # users can specify any fields they want
    if format:
        fields = format.split(",")
        missing_field = False
        for e in events['e']:
            line = ''
            for field in fields:
                try:
                    line += e['event'][field] + ' '
                except KeyError:
                    missing_field = True
            print line
        if missing_field:
            print "\nWarning! One of more fields missing\n"

    # by default print out the syslog ones
    else:
        for e in events['e']:
            print datetime.datetime.fromtimestamp(
                e['timestamp'] // 1000000000), \
                e['event']['host'], \
                e['event']['severity'], \
                e['event']['facility'], \
                e['event']['body']
