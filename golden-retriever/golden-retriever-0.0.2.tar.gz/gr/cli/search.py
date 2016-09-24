from ..cli import *
from ..api import *
import click
import datetime


@cli.command('search')
@click.argument('filter', default='')
@click.option('--period', help='search back this number of minutes', type=int, default=120)
def search(filter, period):
    """searches events"""
    start_date = datetime.datetime.now() - datetime.timedelta(minutes=period)
    end_date = datetime.datetime.now()
    events = get_events(url=context.settings['url'], bucket='syslog', start_date=start_date, end_date=end_date, filter=filter)
    for e in events['e']:
        print datetime.datetime.fromtimestamp(
            e['timestamp'] // 1000000000), \
            e['event']['host'], \
            e['event']['severity'], \
            e['event']['facility'], \
            e['event']['body']
