# coding: utf-8
# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
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
"""Tests for AuthorityRecord entities"""


from lxml import etree

from cubicweb import Binary
from cubicweb.devtools.testlib import CubicWebTC

from cubes.eac import testutils


class EACExportTC(CubicWebTC):
    """Unit tests for EAC-CPF exports."""

    def test_richstring_plain(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            desc = u'ding'
            mandate = cnx.create_entity(
                'Mandate', term=u'ding-girl',
                description=desc, description_format=u'text/plain',
                mandate_agent=alice)
            cnx.commit()
            serializer = alice.cw_adapt_to('EAC-CPF')
            tag, = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
        self.assertEqual(tag.tag, 'p')
        self.assertEqual(tag.text, desc)

    def test_richstring_html_simple(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            desc = u'<span>ding</span>'
            mandate = cnx.create_entity(
                'Mandate', term=u'ding-girl',
                description=desc, description_format=u'text/html',
                mandate_agent=alice)
            cnx.commit()
            serializer = alice.cw_adapt_to('EAC-CPF')
            tag, = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
        self.assertEqual(tag.tag, 'span')
        self.assertIn(desc, etree.tostring(tag))

    def test_richstring_html_multiple_elements(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            desc = [u'<h1>she <i>rules!</i></h1>', u'<a href="1">pif</a>']
            mandate = cnx.create_entity(
                'Mandate', term=u'chairgirl',
                description=u''.join(desc), description_format=u'text/html',
                mandate_agent=alice)
            cnx.commit()
            serializer = alice.cw_adapt_to('EAC-CPF')
            h1, a = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
        self.assertEqual(h1.tag, 'h1')
        self.assertEqual(a.tag, 'a')
        self.assertIn(etree.tostring(h1), desc[0])
        self.assertIn(etree.tostring(a), desc[1])

    def test_richstring_markdown(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            desc = u'[pif](http://gadget.com) is *red*'
            desc_html = (
                u'<a href="http://gadget.com">pif</a> '
                u'is <em>red</em>'
            )
            mandate = cnx.create_entity(
                'Mandate', term=u'w',
                description=desc, description_format=u'text/markdown',
                mandate_agent=alice)
            cnx.commit()
            serializer = alice.cw_adapt_to('EAC-CPF')
            tag, = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
        self.assertEqual(tag.tag, 'p')
        self.assertIn(desc_html, etree.tostring(tag))

    def test_richstring_rest(self):
        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            desc = u'`pif <http://gadget.com>`_ is *red*'
            desc_html = (
                u'<a class="reference" href="http://gadget.com">pif</a> '
                u'is <em>red</em>'
            )
            mandate = cnx.create_entity(
                'Mandate', term=u'w',
                description=desc, description_format=u'text/rest',
                mandate_agent=alice)
            cnx.commit()
            serializer = alice.cw_adapt_to('EAC-CPF')
            ptag, = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
        self.assertEqual(ptag.tag, 'p')
        self.assertIn(desc_html, etree.tostring(ptag))

    def test_richstring_empty(self):
        def check(authority_record):
            serializer = authority_record.cw_adapt_to('EAC-CPF')
            res = serializer._eac_richstring_paragraph_elements(
                mandate, 'description')
            self.assertEqual(res, [])

        with self.admin_access.cnx() as cnx:
            alice = testutils.authority_record(cnx, u'Alice')
            mandate = cnx.create_entity(
                'Mandate', term=u'w',
                description=None,
                mandate_agent=alice)
            cnx.commit()
            check(alice)
        with self.admin_access.cnx() as cnx:
            cnx.execute(
                'SET X description_format "text/rest" WHERE X is Mandate')
            cnx.commit()
            authority_record = cnx.find('AuthorityRecord', name=u'Alice').one()
            check(authority_record)


class AuthorityRecordExportTC(CubicWebTC, testutils.XmlTestMixin):
    """Functional test case for AuthorityRecord export in EAC-CPF."""

    def test_simple_export(self):
        with self.admin_access.client_cnx() as cnx:
            agent = testutils.authority_record(cnx, u'Charlie')
            agent_home_addr = cnx.create_entity('PostalAddress', street=u'Place du Capitole',
                                                postalcode=u'31000', city=u'Toulouse')
            cnx.create_entity('AgentPlace', name=u'1', role=u'home', place_agent=agent,
                              place_address=agent_home_addr)
            agent_work_addr = cnx.create_entity('PostalAddress', street=u'104 bd L.-A. Blanqui',
                                                postalcode=u'75013', city=u'Paris')
            cnx.create_entity('AgentPlace', name=u'2', role=u'work', place_agent=agent,
                              place_address=agent_work_addr)
            uri = cnx.create_entity('ExternalUri', uri=u'http://www.logilab.fr')
            cnx.create_entity('EACResourceRelation',
                              resource_relation_resource=uri,
                              resource_relation_agent=agent,
                              xml_wrap=Binary('<pif><paf>pouf</paf></pif>'))
            agent2 = testutils.authority_record(cnx, u'Super Service',
                                                kind=u'authority')
            cnx.create_entity('ChronologicalRelation',
                              chronological_predecessor=agent2,
                              xml_wrap=Binary('<plip>plop</plip>'),
                              chronological_successor=agent)
            cnx.commit()

            agent_eac = agent.cw_adapt_to('EAC-CPF').dump()
            agent2_url = agent2.cwuri
        # Then check that output XML is as expected
        with open(self.datapath('agent3_export.xml')) as f:
            expected_eac = f.read().format(agent=agent, agent2_url=agent2_url)
        self.assertXmlEqual(agent_eac, expected_eac)
        # XXX invalid because there is no activities
        # self.assertXmlValid(agent_eac, self.datapath('cpf.xsd'))

    def test_roundtrip(self):
        fpath = self.datapath('FRAD033_EAC_00001_simplified_export.xml')
        with self.admin_access.client_cnx() as cnx:
            created, updated = testutils.eac_import(cnx, fpath)
            record = cnx.find('AuthorityRecord', isni=u'22330001300016').one()
            generated_eac = record.cw_adapt_to('EAC-CPF').dump()
            child_record = cnx.find('AuthorityRecord',
                                    name=u"Gironde. Conseil général. Direction de l'administration "
                                    u"et de la sécurité juridique").one()
            child_record_url = child_record.cwuri
            cg32_record = cnx.find('AuthorityRecord', name=u"CG32").one()
            cg32_record_url = cg32_record.cwuri
            trash_record = cnx.find('AuthorityRecord', name=u"Trash").one()
            trash_record_url = trash_record.cwuri
        with open(fpath) as stream:
            expected_eac = stream.read().format(record=record,
                                                child_record_url=child_record_url,
                                                cg32_record_url=cg32_record_url,
                                                trash_record_url=trash_record_url)
        self.assertXmlEqual(generated_eac, expected_eac)
        self.assertXmlValid(generated_eac, self.datapath('cpf.xsd'))


if __name__ == '__main__':
    import unittest
    unittest.main()
