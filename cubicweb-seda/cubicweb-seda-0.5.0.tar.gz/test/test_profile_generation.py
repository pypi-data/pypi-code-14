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
"""cubicweb-seda unit tests for XSD profile generation"""

from doctest import Example
from itertools import chain, izip, repeat

from six import binary_type

from lxml import etree
from lxml.doctestcompare import LXMLOutputChecker

from logilab.common.decorators import cached

from cubicweb.devtools.testlib import CubicWebTC

from cubes.seda.xsd2yams import XSDMMapping
from cubes.seda.entities.profile_generation import _path_target_values

from testutils import create_archive_unit, create_data_object, scheme_for_rtype, scheme_for_type


class XmlTestMixin(object):
    """Mixin class provinding additional assertion methods for checking XML data."""
    NAMESPACES = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'seda': 'fr:gouv:culture:archivesdefrance:seda:v2.0',
        'rng': 'http://relaxng.org/ns/structure/1.0',
        'a': 'http://relaxng.org/ns/compatibility/annotations/1.0',
    }
    # TBD in concret implementation
    schema_class = None
    schema_file = None
    adapter_id = None

    @classmethod
    @cached
    def schema(cls, xsd_filename):
        with open(xsd_filename) as stream:
            return cls.schema_class(etree.parse(stream))

    def xpath(self, element, expression):
        return element.xpath(expression, namespaces=self.NAMESPACES)

    def get_element(self, profile, name):
        """Return etree element definition for 'name' (there should be only one)"""
        elements = self.get_elements(profile, name)
        self.assertEqual(len(elements), 1)
        return elements[0]

    def get_elements(self, profile, name):
        """Return etree element definitions for 'name'"""
        raise NotImplementedError()

    def get_attribute(self, profile, name):
        """Return etree attribute definition for 'name' (there should be only one)"""
        attributes = self.get_attributes(profile, name)
        self.assertEqual(len(attributes), 1)
        return attributes[0]

    def get_attributes(self, profile, name):
        """Return etree attribute definitions for 'name'"""
        raise NotImplementedError()

    def profile_etree(self, transfer_entity):
        """Return etree representation of profile's XSD for the given transfer entity."""
        adapter = transfer_entity.cw_adapt_to(self.adapter_id)
        root = adapter.dump_etree()
        self.assertXmlValid(root)
        return root

    def assertXmlValid(self, root):
        """Validate an XML etree according to an XSD file (.xsd)."""
        schema = self.schema(self.datapath(self.schema_file))
        schema.assert_(root)

    def assertXmlEqual(self, actual, expected):
        """Check that both XML strings represent the same XML tree."""
        checker = LXMLOutputChecker()
        if not checker.check_output(expected, actual, 0):
            message = checker.output_difference(Example("", expected), actual, 0)
            self.fail(message)


class XMLSchemaTestMixin(XmlTestMixin):
    """Mixin extending XmlTestMixin with implementation of some assert methods for XMLSchema."""

    schema_class = etree.XMLSchema
    schema_file = 'XMLSchema.xsd'
    adapter_id = 'SEDA-2.0.xsd'

    def get_elements(self, profile, name):
        return self.xpath(profile, '//xs:element[@name="{0}"]'.format(name))

    def get_attributes(self, profile, name):
        return self.xpath(profile, '//xs:attribute[@name="{0}"]'.format(name))

    def assertElementDefinition(self, element, expected):
        edef = dict(element.attrib)
        types = self.xpath(element, 'xs:complexType/xs:simpleContent/xs:extension')
        assert len(types) <= 1
        if types:
            edef['type'] = types[0].attrib['base']
        self.assertEqual(edef, expected)

    def assertAttributeDefinition(self, element, expected):
        edef = dict(element.attrib)
        edef.setdefault('use', 'required')
        self.assertEqual(edef, expected)

    def assertXSDAttributes(self, element, expected_attributes):
        # attributes for regular elements
        attrs = [x.attrib for x in self.xpath(element, 'xs:complexType/xs:attribute')]
        # attributes for simple elements
        attrs += [x.attrib for x in self.xpath(
            element, 'xs:complexType/xs:simpleContent/xs:extension/xs:attribute')]
        self.assertEqual(sorted(attrs), expected_attributes)


class RelaxNGTestMixin(XmlTestMixin):
    """Mixin extending XmlTestMixin with implementation of some assert methods for RelaxNG."""

    schema_class = etree.RelaxNG
    schema_file = 'relaxng.rng'
    adapter_id = 'SEDA-2.0.rng'

    def get_elements(self, profile, name):
        return self.xpath(profile, '//rng:element[@name="{0}"]'.format(name))

    def get_attributes(self, profile, name):
        return self.xpath(profile, '//rng:attribute[@name="{0}"]'.format(name))

    def assertElementDefinition(self, element, expected):
        edef = dict(element.attrib)  # {name: element name}
        if element.getparent().tag == '{http://relaxng.org/ns/structure/1.0}optional':
            edef['minOccurs'] = '0'
        elif element.getparent().tag == '{http://relaxng.org/ns/structure/1.0}oneOrMore':
            edef['maxOccurs'] = 'unbounded'
        elif element.getparent().tag == '{http://relaxng.org/ns/structure/1.0}zeroOrMore':
            edef['minOccurs'] = '0'
            edef['maxOccurs'] = 'unbounded'
        refs = self.xpath(element, 'rng:ref')
        if refs:
            assert len(refs) == 1
            edef['type'] = refs[0].attrib['name']
        self._element_fixed_value(edef, element)
        self.assertEqual(edef, expected)

    def assertAttributeDefinition(self, element, expected):
        edef = dict(element.attrib)  # {name: element name}
        if element.getparent().tag == '{http://relaxng.org/ns/structure/1.0}optional':
            edef['use'] = 'optional'
        else:
            edef['use'] = 'required'
        self._element_fixed_value(edef, element)
        self.assertEqual(edef, expected)

    def assertXSDAttributes(self, element, expected_attributes):
        adefs = []
        optattrs = self.xpath(element, 'rng:optional/rng:attribute')
        attrs = self.xpath(element, 'rng:attribute')
        for use, adef_element in chain(izip(repeat('optional'), optattrs),
                                       izip(repeat('required'), attrs)):
            adef = dict(adef_element.attrib)
            adef['use'] = use
            data_elements = self.xpath(adef_element, 'rng:data')
            if data_elements:
                assert len(data_elements) == 1
                adef['type'] = 'xsd:' + data_elements[0].attrib['type']
            self._element_fixed_value(adef, adef_element)
            adefs.append(adef)
        return sorted(adefs)

    def _element_fixed_value(self, edef, element):
        values = self.xpath(element, 'rng:value')
        if values:
            assert len(values) == 1
            value = values[0]
            edef['fixed'] = value.text
            if value.attrib.get('type'):
                edef['type'] = 'xsd:' + value.attrib['type']
        else:
            datatypes = self.xpath(element, 'rng:data')
            if datatypes:
                assert len(datatypes) == 1
                datatype = datatypes[0]
                edef['type'] = 'xsd:' + datatype.attrib['type']


class PathTargetValuesTC(CubicWebTC):

    def test_path(self):
        element_defs = iter(XSDMMapping('Keyword'))
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity
            kw = create('SEDAKeyword', user_cardinality=u'0..n')
            kt = create('SEDAKeywordType', seda_keyword_type_from=kw)
            kc = create('SEDAKeywordContent', reverse_seda_keyword_content=kw)

            edef = next(element_defs)
            # self.assertEqual(
            #  readable_edef(edef),
            #  ('Keyword', 'SEDAKeyword', [
            #      ('id', [('seda_id', 'object', 'SEDAid'),
            #              ('id', 'subject', 'String')]),
            #      ('KeywordContent', [('seda_keyword_content', 'subject', 'SEDAKeywordContent')]),
            #      ('KeywordReference',
            #       [('seda_keyword_reference_from', 'object', 'SEDAKeywordReference'),
            #        ('seda_keyword_reference_to', 'subject', 'Concept')]),
            #      ('KeywordType', [('seda_keyword_type_from', 'object', 'SEDAKeywordType'),
            #                       ('seda_keyword_type_to', 'subject', 'Concept')]),
            #  ]))
            path = edef[-1][0][1]
            target_values = _path_target_values(kw, path)
            self.assertEqual(len(target_values), 1)
            target_value = target_values[0]
            self.assertEqual(target_value[0], None)
            self.assertEqual(target_value[1], None)

            path = edef[-1][1][1]
            target_values = _path_target_values(kw, path)
            self.assertEqual(len(target_values), 1)
            target_value = target_values[0]
            self.assertEqual(target_value[0].eid, kc.eid)
            self.assertEqual(target_value[1].eid, kc.eid)

            path = edef[-1][2][1]
            target_values = _path_target_values(kw, path)
            self.assertEqual(len(target_values), 0)

            path = edef[-1][3][1]
            target_values = _path_target_values(kw, path)
            self.assertEqual(len(target_values), 1)
            target_value = target_values[0]
            self.assertEqual(target_value[0].eid, kt.eid)
            self.assertEqual(target_value[1], None)

            kt_scheme = scheme_for_rtype(cnx, 'seda_keyword_type_to', u'theme')
            kw_type = kt_scheme.reverse_in_scheme[0]
            kt.cw_set(seda_keyword_type_to=kw_type)
            path = edef[-1][3][1]
            target_values = _path_target_values(kw, path)
            self.assertEqual(len(target_values), 1)
            target_value = target_values[0]
            self.assertEqual(target_value[0].eid, kt.eid)
            self.assertEqual(target_value[1].eid, kw_type.eid)

            edef = next(element_defs)
            # self.assertEqual(
            #     readable_edef(edef),
            #     ('KeywordContent', 'SEDAKeywordContent', [
            #         ('KeywordContent', [('keyword_content', 'subject', 'String')]),
            #     ]))
            path = edef[-1][0][1]
            target_values = _path_target_values(kc, path)
            self.assertEqual(len(target_values), 1)
            target_value = target_values[0]
            self.assertEqual(target_value[0], None)
            self.assertEqual(target_value[1], None)


class SEDA2ExportTCMixIn(object):

    def test_skipped_mandatory_simple(self):
        with self.admin_access.client_cnx() as cnx:
            profile = self.profile_etree(cnx.create_entity('SEDAArchiveTransfer',
                                                           title=u'test profile'))
            date = self.get_element(profile, 'Date')
            self.assertElementDefinition(date, {'name': 'Date',
                                                'type': 'xsd:dateTime'})
            self.assertXSDAttributes(date, [])
            identifier = self.get_element(profile, 'MessageIdentifier')
            self.assertElementDefinition(identifier, {'name': 'MessageIdentifier',
                                                      'type': 'xsd:token'})
            self.assertXSDAttributes(
                identifier,
                [{'name': 'schemeAgencyID', 'use': 'optional', 'type': 'xsd:token'},
                 {'name': 'schemeAgencyName', 'use': 'optional', 'type': 'xsd:string'},
                 {'name': 'schemeDataURI', 'use': 'optional', 'type': 'xsd:anyURI'},
                 {'name': 'schemeID', 'use': 'optional', 'type': 'xsd:token'},
                 {'name': 'schemeName', 'use': 'optional', 'type': 'xsd:string'},
                 {'name': 'schemeURI', 'use': 'optional', 'type': 'xsd:anyURI'},
                 {'name': 'schemeVersionID', 'use': 'optional', 'type': 'xsd:token'}])

    def test_skipped_mandatory_complex(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            create_data_object(transfer, id=u"bdo1", filename=u'fixed.txt')
            profile = self.profile_etree(transfer)
            fname = self.get_element(profile, 'Filename')
            self.assertElementDefinition(fname, {'name': 'Filename',
                                                 'fixed': 'fixed.txt',
                                                 'type': 'xsd:string'})
            self.assertXSDAttributes(fname, [])
            attachment = self.get_element(profile, 'Attachment')
            self.assertElementDefinition(attachment, {'name': 'Attachment',
                                                      'type': 'xsd:base64Binary'})
            self.assertXSDAttributes(attachment,
                                     [{'name': 'filename', 'use': 'optional',
                                       'type': 'xsd:string'},
                                      {'name': 'uri', 'use': 'optional',
                                       'type': 'xsd:anyURI'}])

    def test_fileinfo_card(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            bdo = cnx.create_entity('SEDABinaryDataObject', id=u"bdo1",
                                    seda_binary_data_object=transfer)
            appname = cnx.create_entity('SEDACreatingApplicationName',
                                        seda_creating_application_name=bdo)

            profile = self.profile_etree(transfer)
            fileinfo = self.get_element(profile, 'FileInfo')
            self.assertElementDefinition(fileinfo, {'name': 'FileInfo', 'minOccurs': '0'})

            appname.cw_set(user_cardinality=u'1')
            profile = self.profile_etree(transfer)
            fileinfo = self.get_element(profile, 'FileInfo')
            self.assertElementDefinition(fileinfo, {'name': 'FileInfo'})

            appname.cw_set(user_cardinality=u'0..1')
            bdo.cw_set(filename=u'fixed.txt')
            profile = self.profile_etree(transfer)
            fileinfo = self.get_element(profile, 'FileInfo')
            self.assertElementDefinition(fileinfo, {'name': 'FileInfo'})

    def test_transfer_annotation(self):
        with self.admin_access.client_cnx() as cnx:
            profile = self.profile_etree(cnx.create_entity('SEDAArchiveTransfer',
                                                           title=u'test profile',
                                                           user_annotation=u'some description'))
            docs = self.xpath(profile, '///xs:documentation')
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].text, 'some description')

    def test_transfer_signature(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            cnx.create_entity('SEDASignature', seda_signature=transfer)
            profile = self.profile_etree(transfer)
            signature = self.get_element(profile, 'Signature')
            self.assertElementDefinition(signature, {'name': 'Signature', 'type': 'OpenType',
                                                     'minOccurs': '0'})
            self.assertOpenTypeIsDefined(profile)

    def test_keyword(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity

            scheme = scheme_for_rtype(cnx, 'seda_keyword_type_to', u'theme')
            kw_type = scheme.reverse_in_scheme[0]

            transfer = create('SEDAArchiveTransfer', title=u'test profile')
            unit, unit_alt, unit_alt_seq = create_archive_unit(transfer, user_cardinality=u'0..n')
            content = create('SEDAContent', seda_content=unit_alt_seq)
            kw = create('SEDAKeyword', seda_keyword=content)
            create('SEDAKeywordContent', reverse_seda_keyword_content=kw,
                   keyword_content=u'kwick')
            kwr_e = create('SEDAKeywordReference', seda_keyword_reference_from=kw)
            create('SEDAKeywordType', seda_keyword_type_from=kw,
                   seda_keyword_type_to=kw_type)

            profile = self.profile_etree(transfer)

            kwc = self.get_element(profile, 'KeywordContent')
            self.assertElementDefinition(kwc, {'name': 'KeywordContent',
                                               'type': 'xsd:string',
                                               'fixed': 'kwick'})
            kwt = self.get_element(profile, 'KeywordType')
            self.assertElementDefinition(kwt, {'name': 'KeywordType',
                                               'type': 'xsd:token',
                                               'fixed': 'theme',
                                               'minOccurs': '0'})
            self.assertXSDAttributes(
                kwt,
                [{'name': 'listVersionID', 'fixed': 'seda_keyword_type_to/None vocabulary'}])
            kwr = self.get_element(profile, 'KeywordReference')
            self.assertElementDefinition(kwr, {'name': 'KeywordReference',
                                               'type': 'xsd:token',
                                               'minOccurs': '0'})
            self.assertXSDAttributes(
                kwr,
                [{'name': 'schemeAgencyID', 'type': 'xsd:token', 'use': 'optional'},
                 {'name': 'schemeAgencyName', 'type': 'xsd:string', 'use': 'optional'},
                 {'name': 'schemeDataURI', 'type': 'xsd:anyURI', 'use': 'optional'},
                 {'name': 'schemeID', 'type': 'xsd:token', 'use': 'optional'},
                 {'name': 'schemeName', 'type': 'xsd:string', 'use': 'optional'},
                 {'name': 'schemeURI', 'type': 'xsd:anyURI', 'use': 'optional'},
                 {'name': 'schemeVersionID', 'type': 'xsd:token', 'use': 'optional'}])

            kwr_e.cw_set(seda_keyword_reference_to_scheme=scheme)
            profile = self.profile_etree(transfer)
            kwr = self.get_element(profile, 'KeywordReference')
            self.assertElementDefinition(kwr, {'name': 'KeywordReference',
                                               'type': 'xsd:token',
                                               'minOccurs': '0'})
            self.assertXSDAttributes(
                kwr,
                [{'name': 'schemeURI', 'fixed': scheme.absolute_url()}])

            kwr_e.cw_set(seda_keyword_reference_to=kw_type)
            profile = self.profile_etree(transfer)
            kwr = self.get_element(profile, 'KeywordReference')
            self.assertElementDefinition(kwr, {'name': 'KeywordReference',
                                               'type': 'xsd:token',
                                               'fixed': 'theme',
                                               'minOccurs': '0'})
            self.assertXSDAttributes(
                kwr,
                [{'name': 'schemeURI', 'fixed': scheme.absolute_url()}])

    def test_code_list(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            scheme = cnx.create_entity('ConceptScheme', title=u'Keyword Types')
            cnx.create_entity('SEDAMimeTypeCodeListVersion',
                              seda_mime_type_code_list_version_from=transfer,
                              seda_mime_type_code_list_version_to=scheme)

            profile = self.profile_etree(transfer)
            mt_clv = self.get_element(profile, 'MimeTypeCodeListVersion')
            self.assertElementDefinition(mt_clv, {'name': 'MimeTypeCodeListVersion',
                                                  'fixed': scheme.absolute_url(),
                                                  'type': 'xsd:token',
                                                  'minOccurs': '0'})
            # XXX also fix listSchemeURI ?
            sample_clv = self.get_element(profile, 'ReplyCodeListVersion')
            self.assertXSDAttributes(
                sample_clv,
                [{'name': 'listAgencyID', 'use': 'optional', 'type': 'xsd:token'},
                 {'name': 'listAgencyName', 'use': 'optional', 'type': 'xsd:string'},
                 {'name': 'listID', 'use': 'optional', 'type': 'xsd:token'},
                 {'name': 'listName', 'use': 'optional', 'type': 'xsd:string'},
                 {'name': 'listSchemeURI', 'use': 'optional', 'type': 'xsd:anyURI'},
                 {'name': 'listURI', 'use': 'optional', 'type': 'xsd:anyURI'},
                 {'name': 'listVersionID', 'use': 'optional', 'type': 'xsd:token'}])

    def test_seda2_concept(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity
            scheme = create('ConceptScheme', title=u'Digest algorithm')
            some_concept = scheme.add_concept(label=u'md5 algorithm', language_code=u'en')
            transfer = create('SEDAArchiveTransfer', title=u'test profile',
                              seda_message_digest_algorithm_code_list_version=scheme)
            create('SEDABinaryDataObject', id=u"bdo1", user_cardinality=u'0..n',
                   seda_binary_data_object=transfer,
                   seda_algorithm=some_concept)

            profile = self.profile_etree(transfer)
            algo = self.get_attribute(profile, 'algorithm')
            self.assertAttributeDefinition(algo, {'name': 'algorithm',
                                                  'use': 'required',
                                                  'type': 'xsd:token',
                                                  'fixed': 'md5 algorithm'})

            create('Label', label_of=some_concept, kind=u'preferred',
                   language_code=u'seda-2', label=u'md5')

            some_concept.cw_clear_all_caches()
            profile = self.profile_etree(transfer)
            algo = self.get_attribute(profile, 'algorithm')
            self.assertAttributeDefinition(algo, {'name': 'algorithm',
                                                  'use': 'required',
                                                  'type': 'xsd:token',
                                                  'fixed': 'md5'})


class SEDA2XSDExportTC(SEDA2ExportTCMixIn, XMLSchemaTestMixin, CubicWebTC):

    def assertOpenTypeIsDefined(self, profile):
        open_types = self.xpath(profile, '//xs:complexType[@name="OpenType"]')
        self.assertEqual(len(open_types), 1)

    def test_organization(self):
        """Check that an agent is exported as expected in a SEDA profile."""
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            archival_org = cnx.create_entity('Agent', name=u'Archival inc.',
                                             reverse_seda_archival_agency=transfer)
            profile = self.profile_etree(transfer)
            enum_elts = self.xpath(profile,
                                   '//xs:element[@name="ArchivalAgency"]/xs:complexType'
                                   '/xs:sequence/xs:element/xs:simpleType/xs:restriction'
                                   '/xs:enumeration')
            self.assertEqual(len(enum_elts), 1)
            self.assertEqual(enum_elts[0].attrib['value'], archival_org.absolute_url())


class SEDA2RNGExportTC(SEDA2ExportTCMixIn, RelaxNGTestMixin, CubicWebTC):

    def assertOpenTypeIsDefined(self, profile):
        open_types = self.xpath(profile, '//rng:define[@name="OpenType"]')
        self.assertEqual(len(open_types), 1)

    def test_data_duplicates(self):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.create_entity('SEDAArchiveTransfer', title=u'test profile')
            unit, unit_alt, unit_alt_seq = create_archive_unit(transfer, user_cardinality=u'0..n')
            content = cnx.create_entity('SEDAContent', seda_content=unit_alt_seq)
            cnx.create_entity('SEDATitle', seda_title=content)
            profile = self.profile_etree(transfer)
            title = self.get_element(profile, 'Title')
            self.assertEqual(len(self.xpath(title, 'rng:data')), 1)


class SEDAExportFuncTCMixIn(object):
    """Test that SEDA profile export works correctly."""

    def setup_database(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity
            scheme = create('ConceptScheme', title=u'Keyword Types')
            some_concept = scheme.add_concept(label=u'md5')

            transfer = create('SEDAArchiveTransfer', title=u'test profile',
                              seda_message_digest_algorithm_code_list_version=scheme)
            create('SEDAMimeTypeCodeListVersion', seda_mime_type_code_list_version_from=transfer,
                   seda_mime_type_code_list_version_to=scheme)
            access_rule = create('SEDAAccessRule', seda_access_rule=transfer)
            access_rule_seq = create('SEDASeqAccessRuleRule',
                                     reverse_seda_seq_access_rule_rule=access_rule)
            create('SEDAStartDate', user_cardinality=u'0..1', seda_start_date=access_rule_seq)
            # binary data object
            bdo = create_data_object(transfer, id=u"bdo1", user_cardinality=u'0..n',
                                     seda_algorithm=some_concept)
            create('SEDAFormatLitteral', seda_format_litteral=bdo)
            create('SEDAEncoding', seda_encoding_from=bdo)
            create('SEDAUri', seda_uri=bdo.seda_alt_binary_data_object_attachment)
            # first level archive unit
            unit, unit_alt, unit_alt_seq = create_archive_unit(transfer, user_cardinality=u'0..n',
                                                               user_annotation=u'Composant ISAD(G)')
            # sub archive unit
            # create_archive_unit(unit_alt_seq, user_cardinality=u'0..n')
            # management
            appraisal_rule = create('SEDAAppraisalRule', seda_appraisal_rule=unit_alt_seq)
            appraisal_rule_seq = create('SEDASeqAppraisalRuleRule',
                                        reverse_seda_seq_appraisal_rule_rule=appraisal_rule)
            create('SEDAStartDate', user_cardinality=u'0..1', seda_start_date=appraisal_rule_seq)
            access_rule = create('SEDAAccessRule', seda_access_rule=unit_alt_seq)
            create('SEDADisseminationRule', seda_dissemination_rule=unit_alt_seq)
            create('SEDAReuseRule', seda_reuse_rule=unit_alt_seq)
            create('SEDANeedAuthorization', seda_need_authorization=unit_alt_seq)
            # content
            content = create('SEDAContent', seda_content=unit_alt_seq)
            kw = create('SEDAKeyword', user_cardinality=u'0..n', seda_keyword=content)
            create('SEDAKeywordType', seda_keyword_type_from=kw)
            create('SEDAKeywordReference', seda_keyword_reference_from=kw)
            create('SEDAKeywordContent', reverse_seda_keyword_content=kw)
            history_item = create('SEDACustodialHistoryItem', seda_custodial_history_item=content)
            create('SEDAwhen', seda_when=history_item)
            version_of = create('SEDAIsVersionOf', seda_is_version_of=content)
            alt2 = create('SEDAAltIsVersionOfArchiveUnitRefId',
                          reverse_seda_alt_is_version_of_archive_unit_ref_id=version_of)
            create('SEDADataObjectReference', seda_data_object_reference=alt2)
            create('SEDAOriginatingAgencyArchiveUnitIdentifier',
                   seda_originating_agency_archive_unit_identifier=content)
            create('SEDATransferringAgencyArchiveUnitIdentifier',
                   seda_transferring_agency_archive_unit_identifier=content)
            create('SEDATitle', seda_title=content)
            create('SEDADescription', seda_description=content)
            create('SEDALanguage', seda_language_from=content)
            create('SEDADescriptionLanguage', seda_description_language_from=content)
            create('SEDACreatedDate', seda_created_date=content)
            create('SEDAEndDate', seda_end_date=content)
            create('SEDADataObjectReference', user_cardinality=u'0..n',
                   seda_data_object_reference=unit_alt_seq,
                   seda_data_object_reference_id=bdo)

            cnx.commit()
        self.transfer_eid = transfer.eid

    def check_xsd_profile(self, root, sample_file, **substitutions):
        """Check that the SEDA profile can be used to validate a sample XML document."""
        profile = self.schema_class(root)
        with open(sample_file) as f:
            sample_xml_string = f.read().format(**substitutions)
        profile.assert_(etree.fromstring(sample_xml_string))

    def test_profile1(self):
        """Check a minimal SEDA profile validating BV2.0_min.xml."""
        with self.admin_access.client_cnx() as cnx:
            mda_scheme = cnx.execute('ConceptScheme X').one()
            transfer = cnx.entity_from_eid(self.transfer_eid)
            root = self.profile_etree(transfer)
        self.check_xsd_profile(root, self.datapath('BV2.0_min.xml'),
                               mda_scheme_url=mda_scheme.absolute_url())
        # ensure jumped element without content are not there
        self.assertEqual(len(self.get_elements(root, 'Gps')), 0)
        # ensure element with skipped value are not there
        self.assertEqual(len(self.get_elements(root, 'TransactedDate')), 0)
        self.assertProfileDetails(root)


class SEDAXSDExportFuncTC(SEDAExportFuncTCMixIn, XMLSchemaTestMixin, CubicWebTC):

    def assertProfileDetails(self, root):
        # ensure profile's temporary id are exported in custom seda:profid attribute
        self.assertEqual(len(self.xpath(root, '//xs:attribute[@seda:profid]')), 2)
        # ensure they are properly referenced using 'default' attribute
        references = self.xpath(root, '//xs:element[@default="bdo1"]')
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0].attrib['name'], 'DataObjectReferenceId')
        # ensure optional id are properly reinjected
        references = self.xpath(root,
                                '//xs:element[@name="Keyword"]'
                                '//xs:attribute[@name="id" and @use="optional"]')
        self.assertEqual(len(references), 1)
        # ensure custodial item content type is properly serialized
        chi = self.xpath(root, '//xs:element[@name="CustodialHistoryItem"]')
        self.assertEqual(len(chi), 1)
        self.assertXSDAttributes(
            chi[0],
            [{'name': 'when', 'use': 'optional', 'type': 'datedateTime'}])
        # ensure types union handling
        ddt = self.xpath(root, '//xs:simpleType[@name="datedateTime"]')
        self.assertEqual(len(ddt), 1)
        self.assertEqual(ddt[0][0].tag, '{http://www.w3.org/2001/XMLSchema}union')
        self.assertEqual(ddt[0][0].attrib, {'memberTypes': 'xsd:date xsd:dateTime'})


class SEDARNGExportFuncTC(SEDAExportFuncTCMixIn, RelaxNGTestMixin, CubicWebTC):

    def assertProfileDetails(self, root):
        # ensure profile's temporary id are exported in custom seda:profid attribute
        self.assertEqual(len(self.xpath(root, '//rng:attribute[@seda:profid]')), 2)
        # ensure they are properly referenced using 'default' attribute
        references = self.xpath(root, '//rng:element[@a:defaultValue="bdo1"]')
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0].attrib['name'], 'DataObjectReferenceId')
        # ensure optional id are properly reinjected
        references = self.xpath(root,
                                '//rng:element[@name="Keyword"]/rng:optional'
                                '/rng:attribute[@name="id"]')
        self.assertEqual(len(references), 1)
        # ensure custodial item content type is properly serialized
        chi = self.xpath(root, '//rng:element[@name="CustodialHistoryItem"]')
        self.assertEqual(len(chi), 1)
        self.assertXSDAttributes(
            chi[0],
            [{'name': 'when', 'use': 'optional', 'type': 'datedateTime'}])
        # ensure types union handling
        ddt = self.xpath(root, '//rng:element[@name="CreatedDate"]/rng:choice/rng:data')
        self.assertEqual(len(ddt), 2)
        self.assertEqual(set(elmt.attrib['type'] for elmt in ddt), set(['date', 'dateTime']))


class OldSEDAExportMixin(object):
    def setup_database(self):
        with self.admin_access.client_cnx() as cnx:
            create = cnx.create_entity

            concepts = {}
            for rtype, etype, value in [
                    ('seda_format_id_to', None, u'fmt/123'),
                    ('seda_encoding_to', None, u'6'),
                    ('seda_type_to', None, u'CDO'),
                    ('seda_description_level', None, u'file'),
                    ('seda_rule', 'SEDASeqAppraisalRuleRule', u'P10Y'),
                    ('seda_rule', 'SEDASeqAccessRuleRule', u'AR038'),
                    ('seda_final_action', 'SEDAAppraisalRule', u'detruire'),
            ]:
                scheme = scheme_for_type(cnx, rtype, etype, value)
                concepts[value] = scheme.reverse_in_scheme[0]

            transfer = create('SEDAArchiveTransfer', title=u'my profile title &&',
                              simplified_profile=True)

            create('SEDAComment',
                   user_cardinality=u'1',
                   comment=u'my profile description &&',
                   seda_comment=transfer)

            _, _, unit_alt_seq = create_archive_unit(transfer, id=u'au1',
                                                     user_cardinality=u'1..n')
            create('SEDAAccessRule',  # XXX mandatory for seda 1.0
                   user_cardinality=u'1',
                   seda_access_rule=unit_alt_seq,
                   seda_seq_access_rule_rule=create(
                       'SEDASeqAccessRuleRule', reverse_seda_start_date=create('SEDAStartDate')))

            content = create('SEDAContent',
                             user_cardinality=u'1',
                             seda_content=unit_alt_seq,
                             seda_description_level=concepts['file'],
                             reverse_seda_start_date=create('SEDAStartDate',
                                                            user_cardinality=u'0..1'),
                             reverse_seda_end_date=create('SEDAEndDate'),
                             # XXX, value=date(2015, 2, 24)),
                             reverse_seda_description=create('SEDADescription'))
            cnx.create_entity('SEDATitle', seda_title=content)

            kw = create('SEDAKeyword',
                        user_cardinality=u'0..n',
                        seda_keyword=content,
                        seda_keyword_content=create('SEDAKeywordContent'))  # XXX
            create('SEDAKeywordReference',
                   seda_keyword_reference_from=kw,
                   seda_keyword_reference_to=concepts['file'],
                   seda_keyword_reference_to_scheme=concepts['file'].scheme)

            appraisal_rule_rule = create('SEDASeqAppraisalRuleRule',
                                         seda_rule=concepts['P10Y'],
                                         user_annotation=u"C'est dans 10ans je m'en irai",
                                         reverse_seda_start_date=create('SEDAStartDate'))
            create('SEDAAppraisalRule',
                   seda_appraisal_rule=unit_alt_seq,
                   seda_final_action=concepts['detruire'],
                   seda_seq_appraisal_rule_rule=appraisal_rule_rule,
                   user_annotation=u'detruire le document')

            cnx.create_entity('SEDAType', seda_type_from=content,
                              seda_type_to=concepts['CDO'])

            # Add sub archive unit
            _, _, subunit_alt_seq = create_archive_unit(unit_alt_seq, id=u'au2',
                                                        user_cardinality=u'1..n')
            content = create('SEDAContent', seda_content=subunit_alt_seq)
            cnx.create_entity('SEDATitle', seda_title=content)

            create('SEDAAppraisalRule',
                   seda_appraisal_rule=subunit_alt_seq,
                   seda_seq_appraisal_rule_rule=create(
                       'SEDASeqAppraisalRuleRule', reverse_seda_start_date=create('SEDAStartDate')))

            create('SEDAAccessRule',
                   user_cardinality=u'1',
                   user_annotation=u'restrict',
                   seda_access_rule=subunit_alt_seq,
                   seda_seq_access_rule_rule=create('SEDASeqAccessRuleRule',
                                                    reverse_seda_start_date=create('SEDAStartDate'),
                                                    seda_rule=concepts['AR038']))

            # Add minimal document to first level archive
            ref = create('SEDADataObjectReference', seda_data_object_reference=unit_alt_seq)
            bdo = create_data_object(transfer, id=u"bdo1", user_cardinality=u'0..n',
                                     reverse_seda_data_object_reference_id=ref)

            create('SEDAFormatId',
                   user_cardinality=u'1',
                   seda_format_id_from=bdo,
                   seda_format_id_to=concepts['fmt/123'])
            create('SEDAEncoding',
                   user_cardinality=u'1',
                   seda_encoding_from=bdo,
                   seda_encoding_to=concepts['6'])

            # Add another sub archive unit
            _, _, subunit2_alt_seq = create_archive_unit(unit_alt_seq, id=u'au3',
                                                         user_cardinality=u'1..n')
            content = create('SEDAContent', seda_content=subunit2_alt_seq)
            cnx.create_entity('SEDATitle', seda_title=content)

            cnx.commit()

        self.transfer_eid = transfer.eid
        self.file_concept_eid = concepts['file'].eid

    def _test_profile(self, adapter_id, expected_file):
        with self.admin_access.client_cnx() as cnx:
            transfer = cnx.entity_from_eid(self.transfer_eid)
            adapter = transfer.cw_adapt_to(adapter_id)
            generated_xsd = adapter.dump()
            open('/tmp/x.xml', 'w').write(generated_xsd)
            root = etree.fromstring(generated_xsd)
            self.assertXmlValid(root)
            file_concept = cnx.entity_from_eid(self.file_concept_eid)
            with open(self.datapath(expected_file)) as expected:
                self.assertXmlEqual(expected.read()
                                    % {'concept-uri': binary_type(file_concept.cwuri),
                                       'scheme-uri': binary_type(file_concept.scheme.cwuri)},
                                    generated_xsd)
            return adapter, root


class OldSEDAXSDExportTC(XMLSchemaTestMixin, OldSEDAExportMixin, CubicWebTC):

    def test_seda_1_0(self):
        self._test_profile('SEDA-1.0.xsd', 'seda_1_export.xsd')

    def test_seda_0_2(self):
        self._test_profile('SEDA-0.2.xsd', 'seda_02_export.xsd')

    def _test_profile(self, adapter_id, expected_file):
        adapter, root = super(OldSEDAXSDExportTC, self)._test_profile(adapter_id, expected_file)
        # ensure there is no element with @type but a complex type
        namespaces = adapter.namespaces.copy()
        namespaces.pop(None)
        dates = root.xpath('//xsd:element[@name="Date"]/xsd:complexType/xsd:sequence',
                           namespaces=namespaces)
        self.assertEqual(len(dates), 0)


class OldSEDARNGExportTC(RelaxNGTestMixin, OldSEDAExportMixin, CubicWebTC):

    def test_seda_1_0(self):
        self._test_profile('SEDA-1.0.rng', 'seda_1_export.rng')

    def test_seda_0_2_rng(self):
        self._test_profile('SEDA-0.2.rng', 'seda_02_export.rng')


if __name__ == '__main__':
    import unittest
    unittest.main()
