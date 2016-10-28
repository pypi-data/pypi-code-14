import os
import base.version.ttypes


def build_git_version():
    if os.environ.get('GIT_COMMIT'):
        return base.version.ttypes.GitVersion(
            os.environ.get('GIT_COMMIT'),
            os.environ.get('GIT_REMOTE'),
            os.environ.get('GIT_BRANCH'))
    else:
        return None


def build_semver_version():
    if os.environ.get('SEMVER_VERSION'):
        major, minor, patch = os.environ.get('SEMVER_VERSION').split('.')
        return base.version.ttypes.SemanticVersion(
            int(major[1:]), int(minor), int(patch))
    else:
        return None


version = base.version.ttypes.Version(build_semver_version(),
                                      build_git_version())
