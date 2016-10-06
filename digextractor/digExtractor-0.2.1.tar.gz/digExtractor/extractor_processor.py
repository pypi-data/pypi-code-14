import itertools
import types
import re
from jsonpath_rw.jsonpath import JSONPath
from jsonpath_rw_ext import parse


class ExtractorProcessor(object):

    def __init__(self):
        self.output_field = None
        self.input_fields = None
        self.jsonpaths = None
        self.extractor = None
        self.name = None

    def set_name(self, name):
        self.name = name
        return self

    def get_name(self):
        return self.name

    def set_output_field(self, output_field):
        self.output_field = output_field
        return self

    @staticmethod
    def get_jp(extractor_processor):
        if extractor_processor.get_output_jsonpath_with_name() is not None:
            return extractor_processor.get_output_jsonpath_with_name()
        else:
            return extractor_processor.get_output_jsonpath()

    def set_extractor_processor_inputs(self, extractor_processors):
        if not (isinstance(extractor_processors, ExtractorProcessor) or
                isinstance(extractor_processors, types.ListType)):
            raise ValueError(
                "extractor_processors must be an ExtractorProcessor or a list")

        if isinstance(extractor_processors, ExtractorProcessor):
            extractor_processor = extractor_processors
            self.input_fields = ExtractorProcessor.get_jp(extractor_processor)
            
        elif isinstance(extractor_processors, types.ListType):
            self.input_fields = list()
            for extractor_processor in extractor_processors:
                self.input_fields.append(
                    ExtractorProcessor.get_jp(extractor_processor))

        self.generate_json_paths()
        return self

    def get_output_jsonpath_with_name(self):
        if self.name is None:
            return None
        extractor_filter = "name='{}'".format(self.name)
        output_jsonpath = "{}[?{}].value".format(\
            self.output_field, extractor_filter)

        return output_jsonpath

    def get_output_jsonpath(self):
        #metadata = self.extractor.get_metadata()
        metadata = dict()
        metadata['source'] = str(self.input_fields)
        extractor_filter = ""
        is_first = True
        for key, value in metadata.iteritems():
            if is_first:
                is_first = False
            else:
                extractor_filter = extractor_filter + " & "

            if isinstance(value, basestring):
                extractor_filter = extractor_filter\
                    + "{}=\"{}\"".format(key, re.sub('(?<=[^\\\])\"', "'", value))
                
            elif isinstance(value, types.ListType):
                extractor_filter = extractor_filter\
                    + "{}={}".format(key, str(value))
        output_jsonpath = "{}[?{}].value".format(
            self.output_field, extractor_filter)

        return output_jsonpath

    def set_input_fields(self, input_fields):
        if not (isinstance(input_fields, basestring) or
                isinstance(input_fields, types.ListType)):
            raise ValueError("input_fields must be a string or a list")
        self.input_fields = input_fields
        self.generate_json_paths()
        return self

    def generate_json_paths(self):
        if isinstance(self.input_fields, basestring):
            try:
                self.jsonpaths = parse(self.input_fields)
            except Exception as e:
                print "input_fields failed {}".format(self.input_fields)
                raise e

        elif isinstance(self.input_fields, types.ListType):
            self.jsonpaths = list()
            for input_field in self.input_fields:
                self.jsonpaths.append(parse(input_field))

    def set_extractor(self, extractor):
        self.extractor = extractor
        return self

    def extract_from_renamed_inputs(self, doc, renamed_inputs):
        extracted_value = self.extractor.extract(renamed_inputs)
        if not extracted_value:
            return doc
        metadata = self.extractor.get_metadata()
        metadata['value'] = extracted_value
        metadata['source'] = str(self.input_fields)
        if self.name is not None:
            metadata['name'] = self.name

        if self.output_field in doc:
            output = doc[self.output_field]
            if isinstance(output, dict):
                output = [output, metadata]
            elif isinstance(output, types.ListType):
                output.append(metadata)

        else:
            output = [metadata]
        doc[self.output_field] = output

    @staticmethod
    def add_tuple_to_doc(doc, tup):
        doc[tup[0]] = tup[1]
        return doc

    def extract(self, doc):
        if isinstance(self.jsonpaths, JSONPath):
            jsonpath = self.jsonpaths
            renamed_inputs = dict()
            for value in [match.value for match in jsonpath.find(doc)]:
                renamed_inputs[
                    self.extractor.get_renamed_input_fields()] = value
                self.extract_from_renamed_inputs(doc, renamed_inputs)

        elif isinstance(self.jsonpaths, types.ListType):

            renamed_inputs_lists = dict()
            for jsonpath, renamed_input in \
                    itertools.izip(\
                    iter(self.jsonpaths),\
                    iter(self.extractor.get_renamed_input_fields())):
                renamed_inputs_lists[renamed_input] = [
                    match.value for match in jsonpath.find(doc)]

            renamed_inputs_lists_lists = [
                [(x, z) for z in y]for x, y in renamed_inputs_lists.iteritems()]
            for i in itertools.product(*renamed_inputs_lists_lists):
                renamed_inputs = reduce(
                    ExtractorProcessor.add_tuple_to_doc, i, dict())
                self.extract_from_renamed_inputs(doc, renamed_inputs)
        else:
            raise ValueError("input_fields must be a string or a list")

        return doc
