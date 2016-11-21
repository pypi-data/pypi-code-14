# -*- coding: utf-8 -*-
"""Stuff concerning xml"""
from lxml import objectify
import re
from lxml import etree as E

class XMLElement(object):
    """
    Base class from XML Elements
    """

    @staticmethod
    def xmlify(elementMaker, element, *args, **kwargs):
        """
        xmlifies
        """
        def makeElement(element, *args, **kwargs):
            """makes an element from args and kwargs"""
            return getattr(elementMaker, element)(*args, **kwargs)

        def python_to_xml(tag_name, values, attributes=None):
            """You can feed python_to_xml an imbricated python structure
            and it will recursively map it to a valid xml document"""
            args = []
            kwargs = attributes
            for value in values[0]:
                if isinstance(value, dict):
                    args_kwargs = list(value.values())[0]
                    try:
                        elem = python_to_xml(list(value.keys())[0], args_kwargs, args_kwargs[
                            1] if len(args_kwargs) > 1 else {})
                    except:
                        elem = None
                    args.append(elem)
                else:
                    args.append(value)

            cleaned_tag_name = re.sub('[^\w]', "_", tag_name)
            return makeElement(cleaned_tag_name, *args, **kwargs)

        return python_to_xml(element, *args, **kwargs)

    def pass_rng(self, rng):
        """
        matches the xml against an rng
        """
        relax_doc = E.parse(rng)
        relaxng = E.RelaxNG(relax_doc)
        return relaxng.validate(self()) or self.make_error_log(relaxng)

    def pass_xsd(self, xsd):
        """
        matches the xml against an xsd
        """
        xsd = E.parse(xsd)
        schema = E.XMLSchema(xsd)
        return schema.validate(self()) or self.make_error_log(schema)

    def make_error_log(self, schema):
        """makes an error log, and returns False"""
        self.error_log = schema.error_log
        return False

    def __init__(self, namespace="fr:gouv:culture:archivesdefrance:seda:v1.0", **kwargs):
        self.namespace = namespace
        self.cleanE = objectify.ElementMaker(
            annotate=False, namespace=self.namespace, nsmap={None: self.namespace})
        self.error_log = ""
        if kwargs:
            self.structure = kwargs

    def __call__(self):
        """
        call!
        """
        values = list(
            self.structure.values())[0]
        wot = self.xmlify(self.cleanE, list(self.structure.keys())[0], values, values[
            1] if len(values) > 1 else {})
        objectify.deannotate(wot, cleanup_namespaces=True)
        return wot
