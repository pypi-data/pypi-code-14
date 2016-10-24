# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as publishged by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-saem-ref test for OAI-PMH export"""

from collections import namedtuple
from datetime import datetime, timedelta
from functools import wraps
import time

from dateutil.parser import parse as parse_date
from lxml import etree
import pytz

from logilab.common import tempattr

from cubicweb.devtools.testlib import CubicWebTC

from cubes.oaipmh.entities import OAIComponent
from cubes.oaipmh.views import OAIError, OAIRequest

import testutils


EntityInfo = namedtuple('EntityInfo', ['ark', 'url', 'eid'])


def publish_entity(entity):
    """Fire "publish" transition for `entity`."""
    entity.cw_adapt_to('IWorkflowable').fire_transition('publish')
    entity._cw.commit()


def deprecate_entity(entity):
    """Fire "deprecate" transition for `entity`."""
    entity.cw_adapt_to('IWorkflowable').fire_transition('deprecate')
    entity._cw.commit()


class OAITestMixin(object):

    def oai_component(self, cnx):
        """Return the "oai" component"""
        return self.vreg['components'].select('oai', cnx)


class OAIComponentTC(CubicWebTC, OAITestMixin):

    def test_registered(self):
        with self.admin_access.repo_cnx() as cnx:
            oai = self.oai_component(cnx)
            setspecs = oai.__setspecs__
            self.assertCountEqual(setspecs.keys(),
                                  ['agent', 'organizationunit',
                                   'authorityrecord',
                                   'conceptscheme', 'profile', 'concept'])
            self.assertCountEqual(setspecs['organizationunit'].keys(), ['role'])
            self.assertCountEqual(setspecs['profile'].keys(),
                                  ['transferring_agent'])
            self.assertEqual(setspecs['conceptscheme'].keys(), [])

    def test_setspecs(self):
        with self.admin_access.repo_cnx() as cnx:
            testutils.organization_unit(
                cnx, u'arch', archival_roles=[u'archival'])
            ark = testutils.organization_unit(
                cnx, u'dep', archival_roles=[u'deposit']).ark
            scheme = testutils.setup_scheme(cnx, u'test', u'lab')
            cnx.commit()
            publish_entity(scheme)
            expected = (
                'agent',
                'authorityrecord',
                'organizationunit',
                'organizationunit:role:producer',
                'organizationunit:role:deposit',
                'organizationunit:role:archival',
                'organizationunit:role:control',
                'organizationunit:role:enquirer',
                'organizationunit:role:seda-actor',
                'conceptscheme',
                'profile', 'profile:transferring_agent:%s' % ark,
                'concept', 'concept:in_scheme:%s' % scheme.ark
            )
            oai = self.oai_component(cnx)
            setspecs = [x[0] for x in oai.setspecs()]
            self.assertCountEqual(setspecs, expected)


def setup_agents(cnx):
    """Create three agents (alice, bobby and draft), publish alice and bobby but not draft, and return
    the (ark, url, eid) attributes of alice and bobby.
    """
    alice = testutils.organization_unit(cnx, u'alice',
                                        archival_roles=[u'producer'])
    cnx.commit()
    publish_entity(alice)
    bobby = testutils.organization_unit(cnx, u'bobby',
                                        archival_roles=[u'enquirer'])
    cnx.commit()
    publish_entity(bobby)
    testutils.organization_unit(cnx, u'draft', archival_roles=[u'enquirer'])
    cnx.commit()
    return (
        EntityInfo(alice.ark, alice.absolute_url(), alice.eid),
        EntityInfo(bobby.ark, bobby.absolute_url(), bobby.eid),
    )


class OAIRequestTC(CubicWebTC):

    def test_rset(self):
        """Test `rset` function for exceptions."""
        with self.admin_access.repo_cnx() as cnx:
            return setup_agents(cnx)
        with self.admin_access.web_request() as req:
            for setspec, msg in [
                ('organizationunit:zen', 'invalid set specifier organizationunit:zen'),
                ('organizationunit:role:control', (
                    'The combination of the values of the from, until, and '
                    'set arguments results in an empty list.')),
                ('conceptscheme:haha', 'invalid set specifier conceptscheme:haha'),
                ('scregneugneu', 'invalid set specifier scregneugneu'),
            ]:
                with self.subTest(setspec=setspec):
                    oairq = OAIRequest('http://testing.fr', setspec=setspec)
                    with self.assertRaises(OAIError) as cm:
                        oairq.rset_from_setspec(req)
                    self.assertEqual(cm.exception.errors, {'noRecordsMatch': msg})

    def test_rset_token(self):
        with self.admin_access.repo_cnx() as cnx:
            alice, bobby = setup_agents(cnx)

        def oairq(**kwargs):
            return OAIRequest('http://testing.fr', setspec='organizationunit', **kwargs)

        with self.admin_access.web_request() as req:
            with tempattr(OAIComponent, 'max_result_size', 1):
                rset, token = oairq().rset(req)
                self.assertEqual(len(rset), 1)
                self.assertEqual(token, str(bobby.eid))
                rset, token = oairq(resumption_token=str(bobby.eid)).rset(req)
                self.assertEqual(len(rset), 1)
                self.assertIsNone(token)
            # All results are returned, the resumptionToken is None.
            rset, token = oairq().rset(req)
            self.assertEqual(len(rset), 2)
            self.assertIsNone(token)
            # and this, even if the user specified an input token.
            rset, token = oairq(resumption_token='1').rset(req)
            self.assertEqual(len(rset), 2)
            self.assertIsNone(token)


def no_validate_xml(method):
    """Disable XML schema validation, often because the underlying metadata
    part of the response (RDF, XSD) is not validable (or we don't know how to
    do it).
    """
    @wraps(method)
    def wrapper(self):
        self._validate_xml = False
        self._debug_xml = True
        return method(self)
    return wrapper


class OAIPMHViewsTC(CubicWebTC, OAITestMixin, testutils.XmlTestMixin):

    _validate_xml = True
    _debug_xml = False

    def oai_request(self, req, **formparams):
        req.form.update(formparams)
        out = self.app_handle_request(req, 'oai')
        if self._validate_xml:
            self.assertXmlValid(out, self.datapath('OAI-PMH.xsd'), debug=self._debug_xml)
        return out

    def _setup_agents(self, **kwargs):
        with self.admin_access.repo_cnx() as cnx:
            return setup_agents(cnx, **kwargs)

    def test_xml_attributes_and_namespaces(self):
        """Check XML attributes and namespace declaration of the response."""
        with self.admin_access.web_request() as req:
            # simple request, generating an error but enough to get a properly
            # formatter response.
            result = self.oai_request(req)
            xml = etree.fromstring(result)
            nsmap = {None: 'http://www.openarchives.org/OAI/2.0/',
                     'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
            self.assertEqual(xml.nsmap, nsmap)
            attrib = {
                '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation': ' '.join(
                    ['http://www.openarchives.org/OAI/2.0/',
                     'http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd']),
            }
            self.assertEqual(xml.attrib, attrib)

    def _setup_agents_deleted(self):
        alice, bobby = self._setup_agents()
        with self.admin_access.repo_cnx() as cnx:
            entity = cnx.entity_from_eid(bobby.eid)
            # ensure transition date is greater by at least 1s
            time.sleep(1)
            date_before = entity.modification_date.replace(tzinfo=pytz.utc)
            deprecate_entity(entity)
        return alice, bobby, date_before

    def _setup_schemes(self):
        with self.admin_access.repo_cnx() as cnx:
            pscheme = testutils.setup_scheme(cnx, u'public',
                                             u'public label', u'other public label')
            # draft ConceptScheme
            dscheme = testutils.setup_scheme(cnx, u'draft',
                                             u'draft label', u'other draft label')
            cnx.commit()
            publish_entity(pscheme)
            return (
                EntityInfo(pscheme.ark, pscheme.absolute_url(), pscheme.eid),
                EntityInfo(dscheme.ark, dscheme.absolute_url(), dscheme.eid),
            )

    def test_noverb(self):
        with self.admin_access.web_request() as req:
            result = self.oai_request(req)
        self.assertIn('<request>http://testing.fr/cubicweb/oai</request>',
                      result)
        self.assertIn('<error code="badVerb">no verb specified</error',
                      result)

    def test_badverb(self):
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='coucou')
        self.assertIn('<request>http://testing.fr/cubicweb/oai</request>',
                      result)
        self.assertIn('<error code="badVerb">illegal verb "coucou"</error>',
                      result)

    # some of our setspecs (those with an ARK inside are not valid)
    @no_validate_xml
    def test_listsets(self):
        pscheme, dscheme = self._setup_schemes()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListSets')
        self.assertIn('<request verb="ListSets">http://testing.fr/cubicweb/oai</request>',
                      result)
        for spec in ('agent', 'organizationunit', 'conceptscheme', 'profile',
                     'concept'):
            self.assertIn('<setSpec>{0}</setSpec>'.format(spec),
                          result)
        self.assertIn(('<setSpec>organizationunit:role:deposit</setSpec>'
                       '<setName>An organization unit with deposit archival role</setName>'),
                      result)
        self.assertIn('<setSpec>concept:in_scheme:{0}</setSpec>'.format(pscheme.ark),
                      result)
        self.assertNotIn(dscheme.ark, result)

    def _setup_profile(self, **kwargs):
        """Create a "published" SEDAArchiveTransfer and return its identifier"""
        with self.admin_access.repo_cnx() as cnx:
            profile = testutils.setup_profile(cnx, **kwargs)
            cnx.commit()
            publish_entity(profile)
            return profile.ark

    def test_resumptiontoken_listidentifiers(self):
        alice, bobby = self._setup_agents()

        def check_request(expected_arks, token=None):
            with self.admin_access.web_request() as req:
                result = self.oai_request(
                    req, verb='ListIdentifiers', set='organizationunit',
                    metadataPrefix='rdf',
                    resumptionToken=token)
                # Ensure there are as many <identifier> tag than expected items.
                self.assertEqual(result.count('<identifier>'), len(expected_arks))
                for ark in expected_arks:
                    self.assertIn(
                        '<identifier>ark:/{0}</identifier>'.format(ark), result)
                return result

        # less results than pagination limit
        result = check_request([alice.ark, bobby.ark])
        # All results returned, no resumptionToken is request -> no
        # resumptionToken in response.
        self.assertNotIn('resumptionToken', result)
        with tempattr(OAIComponent, 'max_result_size', 1):
            # max_result_size = 1, 1st batch
            result = check_request([alice.ark])
            # token + expirationDate
            root = etree.fromstring(result)
            token = root.find('.//{%s}resumptionToken' % root.nsmap[None])
            date = parse_date(token.attrib['expirationDate'])
            self.assertLess(datetime.now(pytz.utc) + timedelta(hours=1) - date,
                            timedelta(seconds=1))
            self.assertEqual(token.text, str(bobby.eid))
            # max_result_size = 1, 2nd batch
            result = check_request([bobby.ark], token=str(bobby.eid))
            # max_result_size = 1, no more result
            # No more results -> empty resumptionToken.
            self.assertIn('<resumptionToken/>', result)
            # Empty result, probably a badResumptionToken.
            result = check_request([], token=str(bobby.eid + 1))
            self.assertIn('badResumptionToken', result)

    def test_listidentifiers(self):
        alice, bobby = [x.ark for x in self._setup_agents()]
        profile_id = self._setup_profile()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='organizationunit',
                                      metadataPrefix='rdf')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(bobby), result)
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(alice), result)
            draft = req.execute('Any A WHERE X ark A, X name "draft"')[0][0]
            self.assertNotIn(draft, result)
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='organizationunit:role:producer',
                                      metadataPrefix='rdf')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(alice),
                          result)
            self.assertNotIn('<identifier>ark:/{0}</identifier>'.format(bobby),
                             result)
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='organizationunit:role:producer',
                                      metadataPrefix='rdf')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(alice), result)
            self.assertNotIn('<identifier>ark:/{0}</identifier>'.format(bobby), result)
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='conceptscheme',
                                      metadataPrefix='rdf')
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='profile', metadataPrefix='seda02xsd')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(profile_id), result)

    def test_listidentifiers_setspec_wfstate(self):
        """Check workflow state condition is statisfied with a multi-level
        setspec `organizationunit:role:enquirer`.
        """
        alice, bobby = [x.ark for x in self._setup_agents()]
        self._setup_profile()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='organizationunit:role:enquirer',
                                      metadataPrefix='rdf')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(bobby), result)
            draft = req.execute('Any A WHERE X ark A, X name "draft"')[0][0]
            self.assertNotIn(draft, result)

    def test_listidentifiers_deleted(self):
        """Check <header> element (status attribute, datestamp) for deleted
        records in ListIdentifiers response.
        """
        alice, bobby, date_before = self._setup_agents_deleted()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='organizationunit',
                                      metadataPrefix='rdf')
            self.assertIn(
                '<identifier>ark:/{0}</identifier>'.format(bobby.ark), result)
            self.assertIn('<header status="deleted">', result)
            root = etree.fromstring(result)
            ns = root.nsmap[None]
            # only one <header status="..."> element
            header, = root.findall('.//{%s}header[@status]' % ns)
            datestamp = header.find('{%s}datestamp' % ns).text
            date = parse_date(datestamp)
            self.assertGreater(date, date_before.replace(microsecond=0))

    @no_validate_xml
    def test_listrecords(self):
        alice, bobby = self._setup_agents()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListRecords', set='organizationunit',
                                      metadataPrefix='rdf')
            self.assertIn(
                '<rdf:Description rdf:about="{0}">'.format(bobby.url), result)
            self.assertIn(
                '<rdf:Description rdf:about="{0}">'.format(alice.url), result)
            draft = req.execute('Any A WHERE X ark A, X name "draft"')[0][0]
            self.assertNotIn(draft, result)
            result = self.oai_request(
                req, verb='ListRecords', set='organizationunit:role:producer')
            self.assertIn(
                '<rdf:Description rdf:about="{0}">'.format(alice.url), result)
            self.assertNotIn(bobby.url, result)

    @no_validate_xml
    def test_listrecord_deleted(self):
        """Check absence of <metadata> or <about> elements for deleted
        records in ListRecords response.
        """
        alice, bobby, _ = self._setup_agents_deleted()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListRecords',
                                      set='organizationunit',
                                      metadataPrefix='rdf')
            # no metadata for bobby
            self.assertNotIn(
                '<rdf:Description rdf:about="{0}">'.format(bobby.url), result)
            # but record present
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(bobby.ark), result)
            self.assertIn(
                '<rdf:Description rdf:about="{0}">'.format(alice.url), result)

    @no_validate_xml
    def test_listrecords_profile(self):
        self._setup_profile()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListRecords', set='profile',
                                      metadataPrefix='seda02xsd')
        # Just ensure a SEDA profile (xsd) is present in response.
        self.assertIn('<metadata><xsd:schema', result)
        self.assertIn('fr:gouv:ae:archive:draft:standard_echange_v0.2', result)

    @no_validate_xml
    def test_listidentifiers_profile_setspec(self):
        """Check setspec restriction for SEDAArchiveTransfer."""
        profile_id = self._setup_profile()
        with self.admin_access.cnx() as cnx:
            tagent_eid = testutils.organization_unit(
                cnx, u'blah', archival_roles=[u'deposit']).eid
            cnx.commit()
        profile2_id = self._setup_profile(reverse_use_profile=tagent_eid)
        with self.admin_access.web_request() as req:
            transferring_agent_ark = req.entity_from_eid(tagent_eid).ark
            result = self.oai_request(
                req, verb='ListIdentifiers',
                set='profile:transferring_agent:' + transferring_agent_ark,
                metadataPrefix='seda02xsd')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(profile2_id), result)
            self.assertNotIn(profile_id, result)
        # Check that without a setspec, we get all profiles.
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='ListIdentifiers',
                                      set='profile', metadataPrefix='seda02xsd')
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(profile_id), result)
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(profile2_id), result)

    @no_validate_xml
    def test_getrecord_profile(self):
        profile_id = self._setup_profile()
        with self.admin_access.web_request() as req:
            with self.subTest(md_prefix='seda02xsd'):
                result = self.oai_request(req, verb='GetRecord',
                                          identifier='ark:/' + profile_id,
                                          metadataPrefix='seda02xsd')
                self.assertIn('<metadata><xsd:schema', result)
                self.assertIn('fr:gouv:ae:archive:draft:standard_echange_v0.2', result)
            for md_prefix, ns in [('seda02rng', 'fr:gouv:ae:archive:draft:standard_echange_v0.2'),
                                  ('seda1rng', 'fr:gouv:culture:archivesdefrance:seda:v1.0'),
                                  ('seda2rng', 'fr:gouv:culture:archivesdefrance:seda:v2.0')]:
                with self.subTest(md_prefix=md_prefix):
                    result = self.oai_request(req, verb='GetRecord',
                                              identifier='ark:/' + profile_id,
                                              metadataPrefix=md_prefix)
                    self.assertIn('<metadata><rng:grammar', result)
                    self.assertIn(ns, result)

    @no_validate_xml
    def test_getrecord_agent(self):
        self._debug_xml = True
        with self.admin_access.repo_cnx() as cnx:
            agent = testutils.agent(cnx, u'toto')
            cnx.commit()
            publish_entity(agent)
            ark = agent.ark
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='GetRecord',
                                      identifier='ark:/' + ark,
                                      metadataPrefix='rdf')
            self.assertIn('name>toto</', result)
            self.assertIn('<rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>',
                          result)

    @no_validate_xml
    def test_getrecord_organizationunit(self):
        self._debug_xml = True
        with self.admin_access.repo_cnx() as cnx:
            orgu = testutils.organization_unit(cnx, u'toto')
            cnx.commit()
            publish_entity(orgu)
            ark = orgu.ark
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='GetRecord',
                                      identifier='ark:/' + ark,
                                      metadataPrefix='rdf')
            self.assertIn('name>toto</', result)
            self.assertIn('<rdf:type rdf:resource="http://www.w3.org/ns/org#OrganizationUnit"/>',
                          result)

    @no_validate_xml
    def test_getrecord_authority_record(self):
        with self.admin_access.repo_cnx() as cnx:
            arecord = testutils.authority_record(cnx, u'M. Person')
            cnx.commit()
            arecord.cw_adapt_to('IWorkflowable').fire_transition('publish')
            cnx.commit()
            arecord_ark = arecord.ark
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='GetRecord',
                                      identifier='ark:/' + arecord_ark,
                                      metadataPrefix='eac')
            self.assertIn('<metadata><eac-cpf', result)
            self.assertIn('urn:isbn:1-931666-33-4', result)

    def test_getrecord_deleted(self):
        """Check absence of <metadata> or <about> elements for deleted
        records in GetRecord response.
        """
        alice, bobby, _ = self._setup_agents_deleted()
        with self.admin_access.web_request() as req:
            result = self.oai_request(req, verb='GetRecord',
                                      identifier='ark:/' + bobby.ark,
                                      metadataPrefix='rdf')
            # record is present
            self.assertIn('<identifier>ark:/{0}</identifier>'.format(bobby.ark), result)
            # but not data
            self.assertNotIn('metadata', result)
            self.assertNotIn('rdf', result)

    def test_getrecord_draft(self):
        self._setup_agents()
        with self.admin_access.web_request() as req:
            draft = req.execute('Any A WHERE X ark A, X name "draft"')[0][0]
            result = self.oai_request(req, verb='GetRecord',
                                      identifier='ark:/' + draft,
                                      metadataPrefix='rdf')
            self.assertIn('idDoesNotExist', result)


if __name__ == '__main__':
    import unittest
    unittest.main()
