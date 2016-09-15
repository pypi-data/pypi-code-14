# coding=utf-8
"""Utility functions for RPM API tests."""
from __future__ import unicode_literals

import gzip
import io
from xml.etree import ElementTree

from pulp_smash import api, cli, selectors, utils
from pulp_smash.compat import urljoin
from pulp_smash.constants import RPM_NAMESPACES


def gen_repo():
    """Return a semi-random dict for use in creating an RPM repository."""
    return {
        'id': utils.uuid4(),
        'importer_config': {},
        'importer_type_id': 'yum_importer',
        'notes': {'_repo-type': 'rpm-repo'},
    }


def gen_repo_group():
    """Return a semi-random dict for use in creating a RPM repository group."""
    return {
        'id': utils.uuid4(),
    }


def gen_distributor():
    """Return a semi-random dict for use in creating a YUM distributor."""
    return {
        'auto_publish': False,
        'distributor_id': utils.uuid4(),
        'distributor_type_id': 'yum_distributor',
        'distributor_config': {
            'http': True,
            'https': True,
            'relative_url': utils.uuid4() + '/',
        },
    }


def get_repomd_xml_href(repomd_xml, repomd_type):
    """Parse a ``repomd.xml`` string. Find and return a path.

    Given a ``repomd.xml`` file as a string, use an XPath selector (with
    namespace from :data:`pulp_smash.constants.RPM_NAMESPACES`) to find a path.
    The XML should have this general form::

        <data type="…"><location href="…" /></data>

    Return the "href" attribute.

    :param repomd_xml: A ``repomd.xml`` file, as a string.
    :param repomd_type: A "type" attribute of a "data" element. For example:
        "updateinfo".
    :returns: A path.
    :raises: ``ValueError`` if more than one "location" element is found.
    """
    xpath = (
        "{{{namespace}}}data[@type='{type}']/{{{namespace}}}location"
        .format(namespace=RPM_NAMESPACES['metadata/repo'], type=repomd_type)
    )
    location_elements = ElementTree.fromstring(repomd_xml).findall(xpath)
    if len(location_elements) != 1:
        raise ValueError(
            'The XML tree repomd_xml should only contain one matching '
            '"location" element, but {} were found with the XPath selector {}'
            .format(len(location_elements), xpath)
        )
    return location_elements[0].get('href')


def get_repomd_xml(server_config, repo_path, repomd_type):
    """Retrieve XML of a particular type from a repo.

    Given a URL, fetch, parse and return the repository XML of type
    ``repomd_type``.

    :param pulp_smash.config.ServerConfig server_config: Information about the
        Pulp server being targeted.
    :param repo_path: The path to (or URL of) a repomd repository. This path
        should not include any segments past the repository itself, such as a
        path to a particular ``repodata`` directory.
    :param repomd_type: The name of a type of repomd data, as found in the
        top-level ``repomd.xml`` file of a repository. Valid values might be
        "updateinfo" or "group".
    :returns: An ``xml.etree.ElementTree.Element`` instance containing the
        parsed repository metadata of the requested type.
    """
    # Fetch and parse repomd.xml
    client = api.Client(server_config)
    repomd_xml = client.get(urljoin(repo_path, 'repodata/repomd.xml')).text
    repomd_xml_href = get_repomd_xml_href(repomd_xml, repomd_type)

    # Fetch, parse and return updateinfo.xml or updateinfo.xml.gz
    client.response_handler = xml_handler
    return client.get(urljoin(repo_path, repomd_xml_href))


def get_unit_unassociate_criteria(unit_name):
    """Create a criteria document to unassociate an unit from a repository.

    Check the documentation for more information on how to `unassociate content
    units from a repository`_.

    ..  _unassociate content units from a repository:
        http://pulp.readthedocs.io/en/latest/dev-guide/integration/rest-api/content/associate.html#unassociating-content-units-from-a-repository

    :param unit_name: The name of the unit that will be unassociated from the
        repository.
    """
    return {
        'fields': {
            'unit': [
                'arch',
                'checksum',
                'checksumtype',
                'epoch',
                'name',
                'release',
                'version',
            ]
        },
        'type_ids': ['rpm'],
        'filters': {
            'unit': {'name': unit_name},
        }
    }


def xml_handler(_, response):
    """API response handler for fetching XML generated by yum distributor.

    Check the status code of ``response``, decompress the response if the
    request URL ended in ``.gz``, and return an ``xml.etree.Element`` instance
    built from the response body.

    Note:

    * The entire response XML is loaded and parsed before returning, so this
      may be unsafe for use with large XML files.
    * The ``Content-Type`` and ``Content-Encoding`` response headers are
      ignored due to https://pulp.plan.io/issues/1781.
    """
    response.raise_for_status()
    if response.request.url.endswith('.gz'):  # See bug referenced in docstring
        with io.BytesIO(response.content) as compressed:
            with gzip.GzipFile(fileobj=compressed) as decompressed:
                xml_bytes = decompressed.read()
    else:
        xml_bytes = response.content
    # A well-formed XML document begins with a declaration like this:
    #
    #     <?xml version="1.0" encoding="UTF-8"?>
    #
    # We are trusting the parser to handle this correctly.
    return ElementTree.fromstring(xml_bytes)


class DisableSELinuxMixin(object):  # pylint:disable=too-few-public-methods
    """A mixin providing the ability to temporarily disable SELinux."""

    def maybe_disable_selinux(self, cfg, pulp_issue_id):
        """Disable SELinux if appropriate.

        If the given Pulp issue is unresolved, and if SELinux is installed and
        enforcing on the target Pulp system, then disable SELinux and schedule
        it to be re-enabled. (Method ``addCleanup`` is used for the schedule.)

        :param pulp_smash.config.ServerConfig cfg: Information about the Pulp
            server being targeted.
        :param pulp_issue_id: The (integer) ID of a `Pulp issue`_. If the
            referenced issue is fixed in the Pulp system under test, this
            method immediately returns.
        :returns: Nothing.

        .. _Pulp issue: https://pulp.plan.io/issues/
        """
        # Abort if the Pulp issue is resolved, if SELinux is not installed or
        # if SELinux is not enforcing.
        #
        # NOTE: Hard-coding the absolute path to a command is a Bad Idea™.
        # However, non-login non-root shells may have short PATH environment
        # variables. For example:
        #
        #     /usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin
        #
        # We cannot execute `PATH=${PATH}:/usr/sbin which getenforce` because
        # Plumbum does a good job of preventing shell expansions. See:
        # https://github.com/PulpQE/pulp-smash/issues/89
        if selectors.bug_is_testable(pulp_issue_id, cfg.version):
            return
        client = cli.Client(cfg, cli.echo_handler)
        cmd = 'test -e /usr/sbin/getenforce'.split()
        if client.run(cmd).returncode != 0:
            return
        client.response_handler = cli.code_handler
        cmd = ['/usr/sbin/getenforce']
        if client.run(cmd).stdout.strip().lower() != 'enforcing':
            return

        # Temporarily disable SELinux.
        sudo = '' if utils.is_root(cfg) else 'sudo '
        cmd = (sudo + 'setenforce 0').split()
        client.run(cmd)
        cmd = (sudo + 'setenforce 1').split()
        self.addCleanup(client.run, cmd)
