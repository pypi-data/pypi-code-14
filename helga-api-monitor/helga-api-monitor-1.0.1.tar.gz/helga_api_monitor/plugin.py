""" Plugin entry point for helga """
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from helga import settings
from helga.db import db
from helga.plugins import command
import requests


_HELP_TEXT = """Please refer to README for usage"""
_client = None


@command('api_monitor', help=_HELP_TEXT, shlex=True)
def monitor(client, channel, nick, message, cmg, args):
    if not hasattr(settings, 'API_MONITOR_URL') or not hasattr(settings, 'API_MONITOR_CHANNEL'):
        return 'Settings not configured, please see README and set API_MONITOR_* settings!'
    global _client
    _client = client
    last_error_count = error_count()
    set_last_error_count(last_error_count)
    return generate_response(last_error_count)


def detect():
    global _client
    if not _client:
        return
    new_error_count = error_count()
    if get_last_error_count() != new_error_count:
        channel = getattr(settings, 'API_MONITOR_CHANNEL', '#bots')
        _client.msg(channel, generate_response(new_error_count))
        set_last_error_count(new_error_count)


def generate_response(error_count):
    """ Generate an IRC friendly return string """
    if error_count > 0:
        dashboard_url = settings.API_MONITOR_URL
        operators = ', '.join(['@' + op for op in settings.OPERATORS])
        return "{}: There are {} errors, please visit {}".format(operators, error_count, dashboard_url)
    return "No Errors!"


def error_count():
    """ See how many errors there are in the endpoint via api """
    endpoint = settings.API_MONITOR_ENDPOINT
    try:
        response = requests.get(endpoint).json()
        return len(response['errors'])
    except:
        return 0


def get_last_error_count():
    doc = db.api_monitor.find_one({'name': 'last_error_count'})
    if doc:
        return doc['value']
    return 0


def set_last_error_count(error_count):
    db.api_monitor.update_one({'name': 'last_error_count'}, {'$set': {'value': error_count}}, upsert=True)


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=detect,
    trigger=IntervalTrigger(minutes=getattr(settings, 'API_MONITOR_INTERVAL', 2)),
    id='detect',
    name='Hit endpoint to detect if there is an error',
    replace_existing=True)
atexit.register(lambda: scheduler.shutdown())
