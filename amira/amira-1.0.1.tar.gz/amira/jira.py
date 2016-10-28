# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import logging

import requests
from jira.client import JIRA
from requests.exceptions import RequestException

from amira.results_uploader import ResultsUploader


class JiraResultsUploader(ResultsUploader):
    """Attaches the analysis results to a JIRA issue.

    :param jira_server: The JIRA server URL.
    :type jira_server: string
    :param jira_user: The JIRA user.
    :type jira_user: string
    :param jira_password: The JIRA password.
    :type jira_password: string
    :param jira_project: The JIRA project which will be used when
                         looking for the issue related to the
                         OSXCollector output.
    :type jira_project: string
    :param jira_initial_status: The JIRA status which will be used when
                                looking for the issue related to the
                                OSXCollector output.
    :type jira_initial_status: string
    :param jira_final_status: The JIRA status to which the issues will
                              be moved after the analysis.
    :type jira_final_status: string
    """

    def __init__(
            self, jira_server, jira_user, jira_password, jira_project,
            jira_initial_status, jira_final_status):
        self._jira = JIRA(
            jira_server, basic_auth=(jira_user, jira_password))

        self._server = jira_server
        self._project = jira_project
        self._initial_status = jira_initial_status
        self._final_status = jira_final_status

        # create the headers used when uploading the issue attachment
        authorization = base64.b64encode(
            '{0}:{1}'.format(jira_user, jira_password))
        self._headers = {
            'Authorization': 'Basic {0}'.format(authorization),
            'X-Atlassian-Token': 'nocheck'
        }

    def upload_results(self, results):
        """Attaches the analysis results to a JIRA issue determined by
        the file names of the analysis results,
        e.g. for ``name`` == "jdoe-2016_04_05-17_27_38_summary.txt",
        the JIRA issue will be found by looking for the issue in the
        ``jira_project`` project with the ``jira_initial_status``
        status which has the "Affected User" field set to "jdoe".

        :param results: The list containing the meta info (name,
                        content and content-type) of the files which
                        needs to be uploaded.
        :type results: list of ``FileMetaInfo`` tuples

        :raises: JiraIssueNotFoundError
        :raises: JiraFinalStatusNotFoundError
        """
        for file_meta_info in results:
            logging.info(
                'Attaching the file "{0}" to the JIRA issue.'
                .format(file_meta_info.name))
            self._add_attachment(
                file_meta_info.name,
                file_meta_info.content,
                file_meta_info.content_type)

        # as the for loop above will always iterate over few elements,
        # 'jira_issue_key' should be always initialized
        self._move_to_final_status()

    def _add_attachment(self, name, content, content_type):
        """Attaches the file-like object ``content`` to the JIRA issue
        under the name ``name``. ``name`` is also used to look up the
        JIRA issue to which the file will be attached.
        E.g. for ``name`` = "jdoe-2016_04_05-17_27_38_summary.txt",

        :param name: The attachment name.
        :type name: string
        :param content: The attachment as a file-like object.
        :type content: file
        :param content_type: MIME type of the attachment file,
                             e.g. ``text/html``
        :type content_type: string

        :raises: JiraIssueNotFoundError
        """
        # extract the affected user name from the attachment name
        affected_user = name.split('-', 1)[0]
        self._find_issue_by_affected_user(affected_user)

        # do not use jira Python module as it has some problems
        # with handling larger files
        url = '{0}/rest/api/2/issue/{1}/attachments'.format(
            self._server, self._jira_issue_key)
        files = {'file': (name, content.getvalue(), content_type)}

        try:
            requests.post(url, headers=self._headers, files=files)
        except RequestException:
            logging.exception(
                'Error occurred when adding the attachment file {0}'
                ' to the JIRA issue {1}'
                .format(name, self._jira_issue_key))

    def _find_issue_by_affected_user(self, affected_user):
        """Looks up the JIRA issue which "Affected User" field value
        equals `affected_user` parameter value. Only the issues
        belonging to the `jira_project` project and with the
        `jira_status` status will be considered when looking up the
        issue.

        :raises: JiraIssueNotFoundError
        """
        issues = self._jira.search_issues(
            'project={0} AND status={1} AND "Affected User"={2}'
            .format(self._project, self._initial_status, affected_user))

        if not issues:
            raise JiraIssueNotFoundError(
                'No JIRA issue found for the affected user "{0}".'.format(
                    affected_user))

        # return the first JIRA issue found, ignoring the others if any
        self._jira_issue_key = issues[0].key

    def _move_to_final_status(self):
        """Moves the issue to the final status.

        :raises: JiraFinalStatusNotFoundError
        """
        transition = self._find_transition()
        self._jira.transition_issue(self._jira_issue_key, transition)

    def _find_transition(self):
        """Finds the transition to the final status.

        :raises: JiraFinalStatusNotFoundError
        """
        transitions = self._jira.transitions(self._jira_issue_key)
        for transition in transitions:
            if self._final_status == transition['name']:
                return transition['id']

        # no transition found, raise an exception
        raise JiraFinalStatusNotFoundError(
            'Transition to final status "{0}" not found'.format(
                self._final_status))


class JiraIssueNotFoundError(Exception):
    """Raised if JIRA issue cannot be found."""

    pass


class JiraFinalStatusNotFoundError(Exception):
    """Raised if the final status to which the issue was supposed to be
    transitioned cannot be found.
    """

    pass
