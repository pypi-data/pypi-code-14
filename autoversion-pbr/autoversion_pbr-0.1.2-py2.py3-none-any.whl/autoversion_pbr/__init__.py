#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from __future__ import print_function
import errno
import os
import pbr.packaging
import subprocess
import sys
from packaging.version import Version, InvalidVersion
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser


def main():
    parser = ConfigParser()
    parser.readfp(open('setup.cfg'))
    cfg = {}
    for section in parser.sections():
        cfg[section] = dict(parser.items(section))
    try:
        ver = autoversion(cfg)
    except AutoVersionError as err:
        sys.exit(str(err))
    print(ver)


def autoversion(cfg):
    tag, branch, tags = git_info()
    if tag:
        return tag
    elif not branch:
        raise AutoVersionError("Unable to generate a package version unless "
                               "a branch is checked out in git.")
    buckets = get_version_buckets(cfg)
    tags_by_branch, tags_by_bucket = sort_tags(buckets, tags)
    if branch in tags_by_branch:
        # A release has already been cut from this branch so that is our
        # reference
        reference_tag = max(tags_by_branch[branch])
    else:
        reference_tag = find_reference(branch, buckets, tags_by_bucket)
    delta = count_commits(branch, reference_tag)
    print("autoversion: {} commits since reference point {}".format(
        delta, reference_tag), file=sys.stderr)
    if not delta:
        raise AutoVersionError(
                "Unable to generate version: no commits on branch {0} "
                "after reference {1}. Make sure {1} is merged into {0}"
                .format(branch, reference_tag))
    return make_version(branch, buckets, reference_tag, delta)


def git_info():
    try:
        current_commit = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD']).decode('utf8').strip()
    except OSError as err:
        if err.args[0] == errno.ENOENT:
            raise AutoVersionError(
                    "Not a git checkout or git is not installed")
        raise
    current_tag = None
    # Parse tags and check if the current commit matches one. Ignore tags that
    # don't match the PEP 440 scheme.
    tags = []
    for line in subprocess.check_output(
            ['git', 'ls-remote', '.']).splitlines():
        commit, ref = line.decode('utf8').strip().split(None, 1)
        if not ref.startswith('refs/tags/'):
            continue
        if not ref.endswith('^{}'):
            # ignore simple tags, same as pbr
            continue
        tag = ref[10:-3]
        if 'dev' in tag:
            continue
        try:
            tag = Version(tag.strip())
        except InvalidVersion:
            continue
        tags.append(tag)
        if commit == current_commit:
            current_tag = tag
    # Check what branch is currently checked out
    branch = os.getenv('GIT_BRANCH')
    if branch:
        # When running in jenkins, the checkout is in "detached HEAD" mode but
        # an environment variable holds the branch.
        branch = branch.split('/')[-1]
    else:
        try:
            branch = subprocess.check_output(
                    ['git', 'symbolic-ref', '--short', 'HEAD'],
                    stderr=open(os.devnull, 'wb')).decode('utf8').strip()
        except subprocess.CalledProcessError:
            branch = None
    return current_tag, branch, tags


def get_version_buckets(cfg):
    # Each branch is configured with one or more version "buckets" which
    # indicate which tags might be cut from that branch.
    buckets = []
    for name, value in cfg['autoversion'].items():
        if not name.startswith('branches.'):
            continue
        branch = name[9:]
        versions = value.replace(',', ' ').split()
        for version in versions:
            buckets.append((Version(version), branch))
    buckets.sort(reverse=True)
    return buckets


def sort_tags(buckets, tags):
    tags_by_branch = {}
    tags_by_bucket = {}
    for tag in tags:
        # Tags match to buckets using exact prefixes, not using greater-than or
        # less-than.
        for bucket, branch in buckets:
            if str(tag).startswith(str(bucket) + '.'):
                break
        else:
            # No bucket matched this tag so it can't be used as a reference
            continue
        tags_by_branch.setdefault(branch, []).append(tag)
        tags_by_bucket.setdefault(bucket, []).append(tag)
    for tags in tags_by_branch.values():
        tags.sort()
    for tags in tags_by_bucket.values():
        tags.sort()
    return tags_by_branch, tags_by_bucket


def find_reference(branch, buckets, tags_by_bucket):
    # Find the greatest bucket on any precending branch
    branch_buckets = [ver for (ver, x) in buckets if x == branch]
    if not branch_buckets:
        raise AutoVersionError("Unable to generate a package version: "
                               "no setting for branch {}".format(branch))
    branch_first_bucket = min(branch_buckets)
    preceding_buckets = [ver for (ver, x) in buckets
                         if ver < branch_first_bucket]
    if not preceding_buckets:
        # Most likely we're here because there is only one branch defined and
        # no tags have been cut. Count from the beginning.
        return None
    best_preceding_bucket = max(preceding_buckets)
    # The *least* tag in selected bucket is the reference
    tags = tags_by_bucket.get(best_preceding_bucket, ())
    if tags:
        return min(tags)
    else:
        return None


def count_commits(branch, reference):
    # Include merge commits
    # Exclude any commits that are not descended from the reference commit
    #  i.e. a commit whose parent precedes the tag but was later merged, is not
    #  counted
    #
    # This should guarantee that the number should always be greater than the
    # last time after a merge, without blowing it up if thousands of commits
    # got merged at the same time.
    if reference:
        ids = subprocess.check_output(
                ['git', 'rev-list', '--ancestry-path',
                    '{}..{}'.format(reference, branch)])
    else:
        ids = subprocess.check_output(['git', 'rev-list', '--all'])
    return ids.count(b'\n')


def make_version(branch, buckets, reference, delta):
    base = max(ver for (ver, x) in buckets if x == branch)
    if reference and reference >= base:
        base, patchlevel = reference.base_version.rsplit('.', 1)
        patchlevel = int(patchlevel) + 1
    else:
        base = str(base)
        patchlevel = 0
    ver = Version('{}.{}.dev{}'.format(base, patchlevel, delta))
    if reference:
        assert ver > reference
    return ver


class AutoVersionError(RuntimeError):
    pass


def hook(cfg):
    def _patched_getver(pre_version=None):
        try:
            return str(autoversion(cfg))
        except AutoVersionError as err:
            print("autoversion failed: {}".format(str(err)), file=sys.stderr)
            return ''
    pbr.packaging._get_version_from_git = _patched_getver


def distutils_keyword(dist, attr, value):
    # don't actually need to do anything, the monkeypatch does the work
    pass


if __name__ == '__main__':
    main()
