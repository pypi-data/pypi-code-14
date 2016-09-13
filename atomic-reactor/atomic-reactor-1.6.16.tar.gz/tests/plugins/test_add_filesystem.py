"""
Copyright (c) 2016 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import print_function, unicode_literals
from textwrap import dedent
from flexmock import flexmock

import re
import json
import pytest
import os.path
import responses

try:
    import koji
except ImportError:
    import inspect
    import sys

    # Find out mocked koji module
    import tests.koji as koji
    mock_koji_path = os.path.dirname(inspect.getfile(koji.ClientSession))
    if mock_koji_path not in sys.path:
        sys.path.append(os.path.dirname(mock_koji_path))

    # Now load it properly, the same way the plugin will
    del koji
    import koji

from dockerfile_parse import DockerfileParser
from atomic_reactor.inner import DockerBuildWorkflow
from atomic_reactor.plugin import PreBuildPluginsRunner
from atomic_reactor.plugins.pre_add_filesystem import AddFilesystemPlugin
from atomic_reactor.util import ImageName
from atomic_reactor.source import VcsInfo
from atomic_reactor import koji_util
from tests.constants import (MOCK_SOURCE, DOCKERFILE_GIT, DOCKERFILE_SHA1,
                             MOCK, IMPORTED_IMAGE_ID)
from tests.fixtures import docker_tasker
if MOCK:
    from tests.docker_mock import mock_docker

KOJI_HUB = 'https://koji-hub.com'


class MockSource(object):
    def __init__(self, tmpdir):
        tmpdir = str(tmpdir)
        self.dockerfile_path = os.path.join(tmpdir, 'Dockerfile')
        self.path = tmpdir

    def get_dockerfile_path(self):
        return self.dockerfile_path, self.path

    def get_vcs_info(self):
        return VcsInfo('git', DOCKERFILE_GIT, DOCKERFILE_SHA1)


class X(object):
    image_id = "xxx"
    base_image = ImageName.parse("koji/image-build")
    set_base_image = flexmock()


def mock_koji_session(koji_proxyuser=None, koji_ssl_certs_dir=None,
                      koji_krb_principal=None, koji_krb_keytab=None):
    session = flexmock()
    session.should_receive('buildImageOz').and_return(1234567)
    session.should_receive('taskFinished').and_return(True)
    session.should_receive('getTaskInfo').and_return({
        'state': koji_util.koji.TASK_STATES['CLOSED']
    })
    session.should_receive('listTaskOutput').and_return([
        'fedora-23-1.0.tar.gz',
    ])
    session.should_receive('getTaskChildren').and_return([
        {'id': 1234568},
    ])
    session.should_receive('downloadTaskOutput').and_return('tarball-contents')
    koji_auth_info = {
        'proxyuser': koji_proxyuser,
        'ssl_certs_dir': koji_ssl_certs_dir,
        'krb_principal': koji_krb_principal,
        'krb_keytab': koji_krb_keytab,
    }
    session.should_receive('krb_login').and_return(True)

    (flexmock(koji)
        .should_receive('ClientSession')
        .once()
        .and_return(session))


def mock_image_build_file(tmpdir, contents=None):
    file_path = os.path.join(tmpdir, 'image-build.conf')

    if contents is None:
        contents = dedent("""\
            [image-build]
            name = fedora-23
            version = 1.0
            target = guest-fedora-23-docker
            install_tree = http://install-tree.com/fedora23/
            arches = x86_64

            format = docker
            distro = Fedora-23
            repo = http://repo.com/fedora/x86_64/os/

            ksurl = git+http://ksrul.com/git/spin-kickstarts.git?fedora23#b232f73e
            ksversion = FEDORA23
            kickstart = fedora-23.ks

            [factory-parameters]
            create_docker_metadata = False

            [ova-options]
            ova_option_1 = ova_option_1_value
            """)

    with open(file_path, 'w') as f:
        f.write(dedent(contents))

    return file_path


def mock_workflow(tmpdir, dockerfile):
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image')
    mock_source = MockSource(tmpdir)
    setattr(workflow, 'builder', X)
    workflow.builder.source = mock_source
    flexmock(workflow, source=mock_source)

    df = DockerfileParser(str(tmpdir))
    df.content = dockerfile
    setattr(workflow.builder, 'df_path', df.dockerfile_path)

    return workflow


def create_plugin_instance(tmpdir, kwargs=None):
    tasker = flexmock()
    workflow = flexmock()
    mock_source = MockSource(tmpdir)
    setattr(workflow, 'builder', X)
    workflow.builder.source = mock_source
    workflow.source = mock_source

    if kwargs is None:
        kwargs = {}

    return AddFilesystemPlugin(tasker, workflow, KOJI_HUB, **kwargs)


def test_add_filesystem_plugin_generated(tmpdir, docker_tasker):
    if MOCK:
        mock_docker()

    dockerfile = dedent("""\
        FROM koji/image-build
        RUN dnf install -y python-django
        """)
    workflow = mock_workflow(tmpdir, dockerfile)
    mock_koji_session()
    mock_image_build_file(str(tmpdir))

    runner = PreBuildPluginsRunner(
        docker_tasker,
        workflow,
        [{
            'name': AddFilesystemPlugin.key,
            'args': {'koji_hub': KOJI_HUB}
        }]
    )

    results = runner.run()
    plugin_result = results[AddFilesystemPlugin.key]
    assert 'base-image-id' in plugin_result
    assert plugin_result['base-image-id'] == IMPORTED_IMAGE_ID
    assert 'filesystem-koji-task-id' in plugin_result


@pytest.mark.parametrize(('base_image', 'type_match'), [
    ('koji/image-build', True),
    ('KoJi/ImAgE-bUiLd  \n', True),
    ('spam/bacon', False),
    ('SpAm/BaCon  \n', False),
])
def test_base_image_type(tmpdir, base_image, type_match):
    plugin = create_plugin_instance(tmpdir)
    assert plugin.is_image_build_type(base_image) == type_match


def test_image_build_file_parse(tmpdir):
    plugin = create_plugin_instance(tmpdir)
    file_name = mock_image_build_file(str(tmpdir))
    image_name, config, opts = plugin.parse_image_build_config(file_name)
    assert image_name == 'fedora-23'
    assert config == [
        'fedora-23',
        '1.0',
        ['x86_64'],
        'guest-fedora-23-docker',
        'http://install-tree.com/fedora23/'
    ]
    assert opts['opts'] == {
        'disk_size': 10,
        'distro': 'Fedora-23',
        'factory_parameter': [('create_docker_metadata', 'False')],
        'ova_option': ['ova_option_1=ova_option_1_value'],
        'format': ['docker'],
        'kickstart': 'fedora-23.ks',
        'ksurl': 'git+http://ksrul.com/git/spin-kickstarts.git?fedora23#b232f73e',
        'ksversion': 'FEDORA23',
        'repo': ['http://repo.com/fedora/x86_64/os/'],
    }


def test_missing_yum_repourls(tmpdir):
    plugin = create_plugin_instance(tmpdir, {'repos': None})
    image_build_conf = dedent("""\
        [image-build]
        version = 1.0
        target = guest-fedora-23-docker

        distro = Fedora-23

        ksversion = FEDORA23
        """)

    file_name = mock_image_build_file(str(tmpdir), contents=image_build_conf)
    with pytest.raises(ValueError) as exc:
        plugin.parse_image_build_config(file_name)
    assert 'install_tree cannot be empty' in str(exc)

@responses.activate
def test_image_build_defaults(tmpdir):
    repos = [
        'http://install-tree.com/fedora23.repo',
        'http://repo.com/fedora/x86_64/os.repo',
    ]
    responses.add(responses.GET, 'http://install-tree.com/fedora23.repo',
                  body=dedent("""\
                    [fedora-23]
                    baseurl = http://install-tree.com/$basearch/fedora23
                    """))
    responses.add(responses.GET, 'http://repo.com/fedora/x86_64/os.repo',
                 body=dedent("""\
                    [fedora-os]
                    baseurl = http://repo.com/fedora/$basearch/os

                    [fedora-os2]
                    baseurl = http://repo.com/fedora/x86_64/os2
                    """))
    plugin = create_plugin_instance(tmpdir, {'repos': repos})
    image_build_conf = dedent("""\
        [image-build]
        version = 1.0
        target = guest-fedora-23-docker

        distro = Fedora-23

        ksversion = FEDORA23
        """)

    file_name = mock_image_build_file(str(tmpdir), contents=image_build_conf)
    image_name, config, opts = plugin.parse_image_build_config(file_name)
    assert image_name == 'default-name'
    assert config == [
        'default-name',
        '1.0',
        ['x86_64'],
        'guest-fedora-23-docker',
        'http://install-tree.com/x86_64/fedora23',
    ]
    assert opts['opts'] == {
        'disk_size': 10,
        'distro': 'Fedora-23',
        'factory_parameter': [('create_docker_metadata', 'False')],
        'format': ['docker'],
        'kickstart': 'kickstart.ks',
        'ksurl': '{}#{}'.format(DOCKERFILE_GIT, DOCKERFILE_SHA1),
        'ksversion': 'FEDORA23',
        'repo': [
            'http://install-tree.com/x86_64/fedora23',
            'http://repo.com/fedora/x86_64/os',
            'http://repo.com/fedora/x86_64/os2',
        ],
    }


@responses.activate
def test_image_build_overwrites(tmpdir):
    repos = [
        'http://default-install-tree.com/fedora23.repo',
        'http://default-repo.com/fedora/x86_64/os.repo',
    ]
    responses.add(responses.GET, 'http://default-install-tree.com/fedora23.repo',
                  body=dedent("""\
                    [fedora-23]
                    baseurl = http://default-install-tree.com/fedora23
                    """))
    responses.add(responses.GET, 'http://default-repo.com/fedora/x86_64/os.repo',
                 body=dedent("""\
                    [fedora-os]
                    baseurl = http://default-repo.com/fedora/x86_64/os.repo
                    """))
    plugin = create_plugin_instance(tmpdir, {'repos': repos})
    image_build_conf = dedent("""\
        [image-build]
        name = my-name
        version = 1.0
        arches = i386,i486
        target = guest-fedora-23-docker
        install_tree = http://install-tree.com/fedora23/
        format = locker,mocker
        disk_size = 20

        distro = Fedora-23
        repo = http://install-tree.com/fedora23/,http://repo.com/fedora/x86_64/os/

        ksurl = http://ksurl#123
        kickstart = my-kickstart.ks
        ksversion = FEDORA23

        [factory-parameters]
        create_docker_metadata = Maybe
        """)

    file_name = mock_image_build_file(str(tmpdir), contents=image_build_conf)
    image_name, config, opts = plugin.parse_image_build_config(file_name)
    assert image_name == 'my-name'
    assert config == [
        'my-name',
        '1.0',
        ['i386', 'i486'],
        'guest-fedora-23-docker',
        'http://install-tree.com/fedora23/',
    ]
    assert opts['opts'] == {
        'disk_size': 20,
        'distro': 'Fedora-23',
        'factory_parameter': [('create_docker_metadata', 'Maybe')],
        'format': ['locker', 'mocker'],
        'kickstart': 'my-kickstart.ks',
        'ksurl': 'http://ksurl#123',
        'ksversion': 'FEDORA23',
        'repo': [
            'http://install-tree.com/fedora23/',
            'http://repo.com/fedora/x86_64/os/',
        ],
    }


def test_build_filesystem_missing_conf(tmpdir):
    plugin = create_plugin_instance(tmpdir)
    with pytest.raises(RuntimeError) as exc:
        plugin.build_filesystem('image-build.conf')
    assert 'Image build configuration file not found' in str(exc)


@pytest.mark.parametrize('pattern', [
    'fedora-23-spam-.tar',
    'fedora-23-spam-.tar.gz',
    'fedora-23-spam-.tar.bz2',
    'fedora-23-spam-.tar.xz',
])
def test_build_filesystem_from_task_id(tmpdir, pattern):
    task_id = 987654321
    plugin = create_plugin_instance(tmpdir, {'from_task_id': task_id})
    plugin.session = flexmock()
    file_name = mock_image_build_file(str(tmpdir))
    task_id, filesystem_regex = plugin.build_filesystem('image-build.conf')
    assert task_id == task_id
    match = filesystem_regex.match(pattern)
    assert match is not None
    assert match.group(0) == pattern
