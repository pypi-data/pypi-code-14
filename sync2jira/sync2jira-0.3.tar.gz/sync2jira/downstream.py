# This file is part of sync2jira.
# Copyright (C) 2016 Red Hat, Inc.
#
# sync2jira is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# sync2jira is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with sync2jira; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110.15.0 USA
#
# Authors:  Ralph Bean <rbean@redhat.com>

import json
import operator

import logging

import jira.client

log = logging.getLogger(__name__)


jira_cache = {}
def get_existing_jira_issues_legacy(downstream, config):
    """ This is our old way of matching issues: get all, search by title.

    This will be phased out and removed in a future release.
    """

    key = json.dumps(downstream)
    if not key in jira_cache:
        kwargs = sorted(downstream.items(), key=operator.itemgetter(0))
        client = jira.client.JIRA(**config['sync2jira']['jira'])
        query = " AND ".join([
            "=".join([k, v]) for k, v in kwargs
            if v is not None
        ]) + " AND (resolution is null OR resolution = Duplicate)"
        results = client.search_issues(query)
        # TODO -- handle pagination here...
        jira_cache[key] = results
    return jira_cache[key]


def get_existing_jira_issue(issue, config):
    """ This is the supported way of matching issues.

    Use the upstream url to uniquely grab individual downstream issues.
    """

    kwargs = dict(issue.downstream.items())
    kwargs["'External issue URL'"] = "'%s'" % issue.url
    kwargs = sorted(kwargs.items(), key=operator.itemgetter(0))

    client = jira.client.JIRA(**config['sync2jira']['jira'])
    query = " AND ".join([
        "=".join([k, v]) for k, v in kwargs
        if v is not None
    ]) + " AND (resolution is null OR resolution = Duplicate)"
    results = client.search_issues(query)
    if results:
        return results[0]
    else:
        return None


def upgrade_jira_issue(downstream, issue, config):
    """ Given an old legacy-style downstream issue...
    ...upgrade it to a new-style issue.

    Simply mark it with an external-url field value.
    """
    log.info("    Upgrading %r issue for %r" % (issue.downstream, issue))
    if config['sync2jira']['testing']:
        log.info("      Testing flag is true.  Skipping actual upgrade.")
        return

    # Do it!
    external_url_field = config['sync2jira']['jira_opts']['external_url_field']
    downstream.update(**{external_url_field: issue.url})


def create_jira_issue(issue, config):
    log.info("    Creating %r issue for %r" % (issue.downstream, issue))
    if config['sync2jira']['testing']:
        log.info("      Testing flag is true.  Skipping actual creation.")
        return

    client = jira.client.JIRA(**config['sync2jira']['jira'])
    kwargs = dict(
        summary=issue.title,
        description=issue.url,
        issuetype=dict(name="Bug"),  # TODO - make this configurable per stream
    )
    if issue.downstream['project']:
        kwargs['project'] = dict(key=issue.downstream['project'])
    if issue.downstream['component']:
        kwargs['components'] = [dict(name=issue.downstream['component'])] # TODO - make this a list in the config

    external_url_field = config['sync2jira']['jira_opts']['external_url_field']
    kwargs[external_url_field] = issue.url

    return client.create_issue(**kwargs)


def sync_with_jira(issue, config):
    log.info("Considering upstream %s", issue.url)

    # First, check to see if we have a matching issue using the new method.
    # If we do, then just bail out.  No sync needed.
    if get_existing_jira_issue(issue, config):
        log.info("   Found existing, matching issue downstream.")
        return

    # If we're *not* configured to do legacy matching (upgrade mode) then there
    # is nothing left to do than to but to create the issue and return.
    if not config['sync2jira'].get('legacy_matching', True):
        log.debug("   Legacy matching disabled.")
        create_jira_issue(issue, config)
        return

    # Otherwise, if we *are* configured to do legacy matching, then try and
    # find this issue the old way.
    # - If we can't find it, create it.
    # - If we can find it, upgrade it to the new method.
    log.info("  Looking for matching downstream issue via legacy method.")
    existing_issues = get_existing_jira_issues_legacy(issue.downstream, config)
    existing_summaries = [i.fields.summary for i in existing_issues]
    if issue.title not in existing_summaries:
        create_jira_issue(issue, config)
    else:
        downstream = [
            i for i in existing_issues
            if i.fields.summary == issue.title
        ][0]
        upgrade_jira_issue(downstream, issue, config)
