"""Write your own seekers.

See :doc:`creating_seekers`.
"""

from datetime import datetime
import re
from time import sleep

from bs4 import BeautifulSoup
import dateutil.parser
import requests


_NUMBER_RE = re.compile('\\d+')


def highest_key_function(item):
    return tuple(int(i) for i in _NUMBER_RE.findall(item['name']))


_BREADCRUMB_KEYWORDS = {
    "latest": lambda k: parse_date(k['date']),
    "highest": highest_key_function,
}
_DATE_TRASH_RE = re.compile("(--|[()])")


def _get_and_compile_re(dictionary, key, default_value=None):
    value = dictionary.get(key, default_value)
    if value:
        value = re.compile(value)
    return value


def _resolve_path(path, entry_yielder, match_failure_count):
    resolvable_count = path.count("${latest") + path.count("${highest")
    resolvable_index = 0
    new_path = "/"
    breadcrumbs = path.strip("/").split("/")
    breadcrumb_count = len(breadcrumbs)
    for i, breadcrumb in enumerate(breadcrumbs, start=1):
        for keyword, key_function in _BREADCRUMB_KEYWORDS.items():
            if breadcrumb.startswith("${" + keyword):
                resolvable_index += 1
                entry_re = None
                if ":" in breadcrumb:
                    entry_re = re.compile(breadcrumb[len(keyword)+3:-1])
                skip = 0
                if (match_failure_count and
                        resolvable_index == resolvable_count-1):
                    skip = match_failure_count
                entries = [entry for entry in
                        entry_yielder(new_path)]
                for entry in sorted(entries, key=key_function, reverse=True):
                    match = None
                    if entry_re:
                        match = entry_re.search(entry["name"])
                        if not match:
                            continue
                    if skip > 0:
                        skip -= 1
                        continue
                    if i == breadcrumb_count:
                        return new_path, entry["name"], entry["date"], match
                    else:
                        new_path = new_path + entry['name'] + "/"
                    break
                else:
                    raise _MatchFailure
                break
        else:
            if i == breadcrumb_count:
                raise NotImplementedError()
            new_path += breadcrumb + "/"
    return new_path


class _MatchFailure(Exception):
    pass


def download(url):
    """Returns the content at the specified URL.

    The target content must be a text file, it cannot be binary content.

    This method retries downloads up to 3 times before it gives up and it
    raises an exception.

    Communications using this method do no check that the target server has a
    valid SSL certificate. You should never use this method if your URL
    includes sensitive information, such as passwords.
    """
    time_to_sleep = 15
    maximum_failed_attempts = 3
    failed_attempts = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:48.0) "
                      "Gecko/20100101 Firefox/48.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;"
                  "q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    while True:
        try:
            return requests.get(
                url, headers=headers, timeout=32, verify=False).text
        except (requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            failed_attempts += 1
            if failed_attempts >= maximum_failed_attempts:
                raise
            sleep(time_to_sleep)
            time_to_sleep *= 2


def download_as_soup(url):
    """Downloads the HTML file at the specified URL and returns an instance of
    BeautifulSoup that wraps it.

    This method retries downloads up to 3 times before it gives up and it
    raises an exception.

    Communications using this method do no check that the target server has a
    valid SSL certificate. You should never use this method if your URL
    includes sensitive information, such as passwords.
    """
    return html_to_soup(download(url))


def html_to_soup(html):
    """Returns a BeautifulSoup object for the specified HTML content.

    The `lxml` parser of BeautifulSoup is used.
    """
    return BeautifulSoup(html, "lxml")


# Note: The purpose of removing trash from the date string is to be
# able to handle dates such as ‘Mon, 6 Jun 2016 -- 11:00 (-0400)’,
# which you can see at
# http://download.eclipse.org/eclipse/downloads/
def parse_date(date_string):
    """Returns a `datetime` object created based on the specified date
    string."""
    if date_string is None or isinstance(date_string, datetime):
        return date_string
    return dateutil.parser.parse(_DATE_TRASH_RE.sub("", date_string))


def resolve_path(path, entry_yielder):
    """Resolves the specified path using the specified entry yielder.

    See :ref:`creating-path-seekers`.
    """
    match_failures = 0
    while True:
        try:
            return _resolve_path(path, entry_yielder, match_failures)
        except _MatchFailure:
            if match_failures > 3:
                # A single match failure should be enough. Anything more
                # may be an endless loop.
                raise NotImplementedError
            match_failures += 1


def value_from_match(match, fallback=None):
    """Returns the first capture group of `match`, the whole match if there are
    no capture groups, or `falback` if `match` is `None`.

    See :ref:`creating-path-seekers` for an example usage.
    """
    try:
        return match.group(1)
    except IndexError:
        return match.group(0)
    except AttributeError:
        return fallback


class BaseSeeker(object):
    """Base class for seekers.

    Its constructor must receive a dictionary containing at least an `id` field
    with the ID of the target software.

    Subclasses may access the ID of the target software using `self.id`.

    See :doc:`/creating_seekers`.
    """

    def __init__(self, data):
        self.id = data['id']

    def data(self):
        """Returns a dictionary containing the version information of the
        software whose ID was passed to the constructor.

        The documentation of :func:`version_info()
        <versiontracker.version_info>` describes the expected content of the
        returned dictionary.
        """
        raise NotImplementedError


class GitBaseSeeker(BaseSeeker):
    """Base class for :ref:`Git seekers <git-seekers>`.

    See :ref:`creating-git-seekers`.
    """

    def __init__(self, data):
        super(GitBaseSeeker, self).__init__(data)
        self.tag_re = _get_and_compile_re(data, 'tag')
        self.commit_re = _get_and_compile_re(data, 'commit')

    def iterate_commits(self):
        """Iterates the commits in the target Git repository, starting with the
        latest commit, and yields a dictionary containing a `message` key with
        the commit message, and optionally a `date` and a
        `url` key."""
        raise NotImplementedError

    def complete_data_from_commit_data(self, data, commit_data):
        """Adds any missing version information to the `data` dictionary based
        on the contents of `commit_data` dictionary."""
        pass

    def _data_from_commit_data(self, commit_data):
        message = commit_data['message']
        match = self.commit_re.search(message)
        if match:
            version = value_from_match(match)
            data = {
                'id': self.id,
                'version': version,
                'date': commit_data.get('date', None),
                'url': commit_data.get('url', None),
            }
            self.complete_data_from_commit_data(data, commit_data)
            return data
        return None

    def iterate_tags(self):
        """Iterates the tags in the target Git repository, starting with the
        latest tag, and yields a dictionary containing a `tag` key with the
        tag, and optionally a `date` and a `url` key."""
        raise NotImplementedError

    def complete_data_from_tag_data(self, data, tag_data):
        """Adds any missing version information to the `data` dictionary based
        on the contents of `tag_data` dictionary."""
        pass

    def _data_from_tag_data(self, tag_data):
        tag = tag_data['tag']
        version = None
        if self.tag_re:
            match = self.tag_re.search(tag)
            if match:
                version = value_from_match(match)
        elif tag.startswith(self.id + '-'):
            version = tag[len(self.id)+1:]
        elif tag.startswith("v"):
            version = tag[1:]
        else:
            version = tag
        if version:
            data = {
                "id": self.id,
                "version": version,
                'date': tag_data.get('date', None),
                'url': tag_data.get('url', None),
            }
            self.complete_data_from_tag_data(data, tag_data)
            return data
        return None

    def data(self):
        """Build version information data from the target Git repository.

        If the constructor received a commit regular expression (`commit`),
        version information is built from the latest matching commit.

        If the constructor received a tag regular expression (`tag`), version
        information is built from the latest matching tag.

        Otherwise, version information is built from the latest tag. If that
        tag starts with `v` or with the ID of the target entry followed by an
        hyphen (e.g. `mysoftware-`), that prefix is removed automatically.

        For more information, see :meth:`BaseSeeker.data()`.
        """
        if self.commit_re:
            for commit_data in self.iterate_commits():
                data = self._data_from_commit_data(commit_data)
                if data:
                    return data
        else:
            for tag_data in self.iterate_tags():
                data = self._data_from_tag_data(tag_data)
                if data:
                    return data


class GitServiceBaseSeeker(GitBaseSeeker):
    """Base class for :ref:`Git seekers <git-seekers>` that target a Git
    hosting service.

    See :ref:`creating-git-seekers`.

    The goal of this class is to centralize the handling of the `project` and
    `repository` parameters that are common to most Git hosting services,
    providing for all of them the same behavior of falling back to the target
    software ID when such values are not provided.

    It is simply a subclass of :class:`GitBaseSeeker` that receives a base URL
    template containing `{project}` and `{repository}` placeholders.

    The constructor of this class reads the project and repository values from
    the `data` dictionary, using the target software ID as a fallback, and
    builds `self.base_url` based on the received base URL template and data.

    Subclasses can then use `self.base_url` themselves.
    """

    def __init__(self, data, base_url_template):
        super(GitServiceBaseSeeker, self).__init__(data)
        self.base_url = base_url_template.format(
            project=data.get('project', data['id']),
            repository = data.get('repository', data['id']),)
