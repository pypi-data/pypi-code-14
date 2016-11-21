from unittest import TestCase, main
from element_maker.utils import XMLElement
from lxml import etree as E


class UtilsTest(TestCase):
    """ Test utils """

    def setUp(self):
        self.structure = {'ArchiveTransferRequest':
                          [
                              [
                                  {'Comment': [
                                      ['baz'], {"foo": "bar"}
                                  ]
                                  },
                                  {'Date': [
                                      ["2014-05-12T00:00:00Z"]
                                  ]
                                  }
                              ],
                              {"cars": "pizza"}
                          ]
                          }
        self.namespace = "fr:gouv:culture:archivesdefrance:seda:v1.0"
        self.rng_test_file = "./tests/data/test.rng"
        self.xsd_test_file = "./tests/data/test.xsd"

    def test_xmlify(self):
        xml_element = XMLElement(namespace=self.namespace, **self.structure)()
        self.assertEqual(E.tostring(xml_element),
            '<ArchiveTransferRequest xmlns="fr:gouv:culture:archivesdefrance:seda:v1.0" cars="pizza"><Comment foo="bar">baz</Comment><Date>2014-05-12T00:00:00Z</Date></ArchiveTransferRequest>'.encode('utf-8'))
        self.assertEqual(xml_element.attrib, {'cars': "pizza"})
        self.assertEqual(xml_element.Comment.attrib, {'foo': "bar"})

    def test_pass_rng_ok(self):
        xml_element = XMLElement(namespace=self.namespace, **self.structure)
        result = xml_element.pass_rng(self.rng_test_file)
        self.assertTrue(result)

    def test_pass_rng_wrong(self):
        wrong_structure = {'ArchiveTransferRequest':
                          [
                              [
                                  {'Comment': [
                                      ['baz'], {"wrong": "bar"}
                                  ]
                                  },
                                  {'Date': [
                                      ["2014-05-12T00:00:00Z"]
                                  ]
                                  }
                              ],
                              {"cars": "pizza"}
                          ]
                          }
        xml_element = XMLElement(namespace=self.namespace, **wrong_structure)
        result = xml_element.pass_rng(self.rng_test_file)
        self.assertFalse(result)
        self.assertEqual(str(xml_element.error_log), "<string>:0:0:ERROR:RELAXNGV:RELAXNG_ERR_ATTRVALID: Element Comment failed to validate attributes")

    def test_pass_xsd_ok(self):
        xml_element = XMLElement(namespace=self.namespace, **self.structure)
        result = xml_element.pass_xsd(self.xsd_test_file)
        self.assertTrue(result)

    def test_pass_xsd_wrong(self):
        wrong_structure = {'ArchiveTransferRequest':
                          [
                              [
                                  {'Comment': [
                                      ['baz'], {"wrong": "bar"}
                                  ]
                                  },
                                  {'Date': [
                                      ["2014-05-12T00:00:00Z"]
                                  ]
                                  }
                              ],
                              {"cars": "pizza"}
                          ]
                          }
        xml_element = XMLElement(namespace=self.namespace, **wrong_structure)
        result = xml_element.pass_xsd(self.xsd_test_file)
        self.assertFalse(result)
        self.assertEqual(str(xml_element.error_log), "<string>:0:0:ERROR:SCHEMASV:SCHEMAV_CVC_COMPLEX_TYPE_3_2_1: Element '{fr:gouv:culture:archivesdefrance:seda:v1.0}Comment', attribute 'wrong': The attribute 'wrong' is not allowed.")

if __name__ == '__main__':
    main()
