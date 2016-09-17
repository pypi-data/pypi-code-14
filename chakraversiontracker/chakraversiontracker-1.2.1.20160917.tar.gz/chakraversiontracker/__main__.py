from argparse import ArgumentParser, FileType
from collections import OrderedDict
from copy import deepcopy
import datetime
import json
import os
from os import path
from queue import Queue
import re
import requests
from sys import stderr, stdout
import tarfile
from tempfile import NamedTemporaryFile
from threading import Thread

import jinja2
from termcolor import colored

from versiontracker import iter_version_info
from versiontracker.baseseekers import download_as_soup

from chakraversiontracker._version import __version__


_folder_path = path.dirname(__file__)
_builtin_template_folder = os.path.join(_folder_path, 'templates')
_rolling_repositories = ('testing', 'desktop', 'gtk', 'lib32', 'ccr')
_version_re = re.compile("^(?P<epoch>\d+:)?(?P<pkgver>.*)-(?P<pkgrel>\d+)$")


def _ccr_package_number():
    soup = download_as_soup('https://chakralinux.org/ccr/index.php')
    pgbox = soup.find("div", {"id": "maincontent"}).find_all(
        "div", recursive=False)[1]
    tr = pgbox.find_all("div", recursive=False)[1].table.tr
    tr = tr.find_all("td", recursive=False)[1].table.find_all(
        "tr", recursive=False)[1]
    return int(tr.find_all("td", recursive=False)[1].get_text().strip())


def _ccr_version_from_pkgbuild(package_name):
    url = 'https://chakralinux.org/ccr/pkgbuild_view.php?p=' + package_name
    soup = download_as_soup(url)
    bash_pre = soup.find('pre', 'bash')
    for variable in bash_pre.find_all('span', style='color: #007800;'):
        if variable.string.strip() == 'pkgver':
            return str(variable.next_sibling).strip()


def _data():
    with open(path.join(_folder_path, 'data.json')) as f:
        return json.load(f)


def _termcolor_filter(value, *args, **kargs):
    return colored(value, *args, **kargs)


def _build_argument_parser():
    """Returns an instance of ArgumentParser.

    This is in a separate function to be able to use `sphinx-argparser`.
    """
    parser = ArgumentParser(description="Reports outdated Chakra packages "
                                        "from its rolling repositories.")
    parser.add_argument(
        '-e', '--exclude', metavar='KEYWORD', action='append', default=[],
        help="Ignore packages that are named KEYWORD or have the "
             "KEYWORD tag. It may be used multiple times. Use --list-tags to "
             "get a list of available tags.")
    parser.add_argument(
        '--list-tags', action='store_true', dest='list_tags',
        help="List available package tags that you can pass to -e.")
    parser.add_argument(
        '-r', '--repository', metavar='REPOSITORY', action='append',
        default=[], dest='repositories',
        help="Only check package versions in this repository. Can be used "
             "multiple times. If no repository is specified, package "
             "versions in rolling repositories ({}) are checked.".format(
            ', '.join(_rolling_repositories)))
    parser.add_argument(
        '--exclude-repository', metavar='REPOSITORY', action='append',
        default=[], dest='excluded_repositories',
        help="Do not check package versions in this repository. Can be used "
             "multiple times.")
    parser.add_argument(
        '--no-progress', action='store_false', dest='show_progress',
        help="Do not show the progress of the command while performing long "
             "operations.")
    parser.add_argument(
        '-o', '--output', type=FileType('w'), default=stdout,
        help="Output file. The standard output is used if no output file is "
             "specified.")
    parser.add_argument(
        '-t', '--template',
        default=os.path.join(_builtin_template_folder, 'repositories.cli'),
        help="Jinja2 template to generate the output. It can be either the "
             "name of one of the built-in templates (see --list-templates) "
             "or a path to a custom template.")
    parser.add_argument(
        '--list-templates', action='store_true', dest='list_templates',
        help="List available built-in templates.")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    return parser


def _list_tags(output):
    tags = []
    for data in _data().values():
        if 'tags' in data:
            for tag in data['tags']:
                if tag not in tags:
                    tags.append(tag)
    for tag in sorted(tags):
        print(colored(tag, attrs=['bold']), file=output)


def _list_templates(output):
    for filename in sorted(os.listdir(_builtin_template_folder)):
        print(filename, file=output)


class _CCRDataThread(Thread):
    def __init__(self, data, index, packages_per_page, counter):
        super(_CCRDataThread, self).__init__()
        self.data = data
        self.index = index
        self.packages_per_page = packages_per_page
        self.counter = counter

    def run(self):
        soup = download_as_soup(
            'https://chakralinux.org/ccr/packages.php'
            '?O={}&PP={}'.format(self.index, self.packages_per_page))
        for tr in soup.table.find_all('tr', recursive=False)[1:]:
            package, version = tr.td.get_text().strip().split(' ')
            try:
                pkgver, pkgrel = version.split('-')
            except ValueError:
                # If the version is too long, the CCR trims it. In
                # that case, we should try to extract it from the
                # PKGBUILD file.
                pkgver = _ccr_version_from_pkgbuild(package)
            self.data[package] = pkgver
        self.counter.put(1)


class _RepositoryDataThread(Thread):
    _FILENAME_RE = re.compile(
        r'^(?P<pkgname>.*)-(\d+:)?(?P<pkgver>[^-]*)-\d+$')

    def __init__(self, repository, data, show_progress):
        super(_RepositoryDataThread, self).__init__()
        self.repository = repository
        self.data = data
        self.show_progress = show_progress

    def run(self):
        if self.repository == 'ccr':
            total = _ccr_package_number()
            packages_per_page = 100  # Maximum
            index = 0
            threads = []
            count_queue = Queue()
            while index < total:
                thread = _CCRDataThread(self.data, index, packages_per_page,
                                        count_queue)
                thread.start()
                threads.append(thread)
                index += packages_per_page
            count = 0
            if self.show_progress:
                print("Querying CCR packages…")
                _print_versiontracker_progress(count, total)
            while True:
                count_queue.get()
                count += packages_per_page
                if self.show_progress:
                    _print_versiontracker_progress(min(count, total), total)
                count_queue.task_done()
                if count >= total:
                    break
            for thread in threads:
                thread.join()
            if self.show_progress:
                stdout.write('\n')
        else:
            response = requests.get(
                'http://rsync.chakraos.org/packages/{repository}/x86_64/'
                '{repository}.db'.format(repository=self.repository))
            if response.status_code != 200:
                print(colored("ERROR: Could not retrieve the database of the "
                              "‘{}’ repository.".format(self.repository)),
                      file=stderr)
                return
            f = NamedTemporaryFile(delete=False)
            f.write(response.content)
            f.close()
            tar = tarfile.open(f.name)
            for filename in tar.getnames():
                if '/' in filename:
                    continue
                match = self._FILENAME_RE.match(filename)
                if not match:
                    print(colored(
                            "ERROR: Unexpected content in the database of "
                            "the ‘{}’ repository.".format(
                                self.repository)),
                          file=stderr)
                    return
                pkgname = match.group('pkgname')
                pkgver = match.group('pkgver')
                self.data[pkgname] = pkgver


def _fetch_repository_data(repositories, show_progress=False):
    threads = []
    data = {}
    for repository in repositories:
        repository_data = {}
        data[repository] = repository_data
        thread = _RepositoryDataThread(repository, repository_data,
                                       show_progress)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return data

def _process_repository_data(repositories, input_data, show_progress=False):
    data = _fetch_repository_data(repositories, show_progress)
    output = []
    stable_repositories = [repository for repository in repositories
                           if repository != "testing"]
    testing_repositories = [repository for repository in repositories
                           if repository == "testing"]
    for input_item in input_data:
        pkgname = input_item['repository_pkgname']
        found_also_in = None
        for stage_repositories in (testing_repositories, stable_repositories):
            if found_also_in is not None:
                break
            for repository in stage_repositories:
                if pkgname in data[repository]:
                    if found_also_in is not None:
                        print("Warning: Found '{}' in both [{}] and [{}]."
                            "".format(pkgname, found_also_in, repository),
                            file=stderr)
                    else:
                        found_also_in = repository
                        output_item = deepcopy(input_item)
                        output_item['repository'] = repository
                        output_item['repository_version'] = \
                            data[repository][pkgname]
                        output.append(output_item)
    return output


def _print_versiontracker_progress(current, total):
    stdout.write('\rProgress: {}/{} ({}%){}'.format(
        current, total, int(float(current)/float(total)*100), ' '*5))
    stdout.flush()


def _process_versiontracker_data(input_list, show_progress):
    count = 0
    total = len(input_list)
    if show_progress:
        print("Querying the latest stable versions of tracked packages found "
              "in the specified repositories…")
        _print_versiontracker_progress(count, total)
    input_dictionary = {}
    for input_item in input_list:
        pkgname = input_item['versiontracker_name']
        if pkgname not in input_dictionary:
            input_dictionary[pkgname] = []
        input_dictionary[pkgname].append(input_item)
    output = []
    for data in iter_version_info(list(input_dictionary.keys())):
        pkgname = data['id']
        for input_item in input_dictionary[pkgname]:
            if data['version'] not in (input_item['repository_version'],
                                       input_item['skip']):
                # Outdated!
                output.append({
                    'name': input_item['repository_pkgname'],
                    'repository': input_item['repository'],
                    'repository_version': input_item['repository_version'],
                    'upstream_version': data['version'],
                })
            count += 1
            if show_progress:
                _print_versiontracker_progress(count, total)
    if show_progress:
        stdout.write('\n')
    return output


def _list_outdated_packages(repositories, excluded_keywords, template, output,
                            show_progress):
    # Detect early if the specified template path is not valid
    if os.path.isfile(template):
        template_path = os.path.abspath(template)
    else:
        template_path = os.path.join(_builtin_template_folder, template)
        if not os.path.isfile(template_path):
            print(colored('ERROR: Could not find the specified template.',
                          'red'),
                  file=stderr)
            exit(-1)
    # Obtain the data about outdated packages using threads and queues
    tracked_packages = []
    excluded_keywords = set(excluded_keywords)
    for package, config in _data().items():
        if package in excluded_keywords:
            continue
        if ('tags' in config and
                not excluded_keywords.isdisjoint(config['tags'])):
            continue
        if 'skip' in config and config['skip'] is True:
            continue
        tracked_packages.append({
            'repository_pkgname': package,
            'skip': config.get('skip', False),
            'versiontracker_name': config.get('versiontracker', package)
        })
    found_packages = _process_repository_data(repositories, tracked_packages,
                                              show_progress=show_progress)
    outdated_packages = _process_versiontracker_data(
        found_packages, show_progress=show_progress)
    # Fill template variables with data
    package_data = [package for package in
                    sorted(outdated_packages, key=lambda k: k['name'])]
    repository_data = OrderedDict(
        [(repository, []) for repository in repositories])
    for package in package_data:
        repository_data[package['repository']].append(
            {k: package[k] for k in
             ('name', 'repository_version', 'upstream_version')})
    for key in repository_data:
        if not repository_data[key]:
            del repository_data[key]
    # Load the output template
    loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
    environment = jinja2.Environment(loader=loader)
    environment.filters['cli'] = _termcolor_filter
    template = environment.get_template(os.path.basename(template_path))
    # Template rendering
    output.write(template.render(
        packages=package_data,
        repositories=repository_data,
        date={"local": datetime.datetime.now(),
              "utc": datetime.datetime.utcnow()},
    ))


def _main():
    config = _build_argument_parser().parse_args()
    if config.list_tags:
        return _list_tags(config.output)
    if config.list_templates:
        return _list_templates(config.output)
    if not config.repositories:
        config.repositories = _rolling_repositories
    repositories = [r for r in config.repositories
                    if r not in config.excluded_repositories]
    return _list_outdated_packages(
        repositories, config.exclude, config.template, config.output,
        config.show_progress)
