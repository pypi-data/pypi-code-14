from celery import shared_task
import requests

from django.conf import settings


# ----------------------------------------------------------------------
# Liveblog Firebase Strategy
#
# Firebase is used only as a messaging channel, to update clients when new entries are available.
#
# The idea is to cache a dictionary of {ENTRY_ID: PULBISH TIME} values for each LiveBlog, so clients
# will know when new content is available. Clients will then request only those Entry IDs that are
# currently published and they don't already have.
#
# Necessary to explicitly list each entry b/c future publish dates may roll over without triggering
# Firebase updates. This way our firebase logic can be dumb and only trigger on save/delete.
# ----------------------------------------------------------------------


def _get_entry_url(liveblog_id, entry_id):
    endpoint = getattr(settings, 'LIVEBLOG_FIREBASE_NOTIFY_ENTRY_ENDPOINT', None)
    if endpoint:
        return endpoint.format(liveblog_id=liveblog_id,
                               entry_id=entry_id)


@shared_task(default_retry_delay=5)
def firebase_update_entry(liveblog_id, entry_id, published):

    url = _get_entry_url(liveblog_id, entry_id)
    if url:
        entry = {'id': entry_id}
        if published:
            entry['published'] = published.isoformat()

        resp = requests.patch(url, json=entry)
        resp.raise_for_status()


@shared_task(default_retry_delay=5)
def firebase_delete_entry(liveblog_id, entry_id):

    url = _get_entry_url(liveblog_id, entry_id)
    if url:

        resp = requests.delete(url)

        resp.raise_for_status()


@shared_task(default_retry_delay=5)
def firebase_delete_liveblog(liveblog_id):
    endpoint = getattr(settings, 'LIVEBLOG_FIREBASE_NOTIFY_ENTRIES_ENDPOINT', None)
    if endpoint:
        url = endpoint.format(liveblog_id=liveblog_id)

        resp = requests.delete(url)

        resp.raise_for_status()
