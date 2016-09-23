import itertools
import types
from jsonpath_rw import jsonpath, parse
from jsonpath_rw.jsonpath import JSONPath


class ExtractorProcessor:

    def set_output_field(self, output_field):
        self.output_field = output_field
        return self

    def set_input_fields(self, input_fields):
        if not (isinstance(input_fields, basestring) or isinstance(input_fields, types.ListType)):
            raise ValueError("input_fields must be a string or a list")
        self.input_fields = input_fields
        self.generate_input_fields_json_paths(input_fields)
        return self

    def generate_input_fields_json_paths(self, input_fields):
        if isinstance(self.input_fields, basestring):
            self.jsonpaths = parse(self.input_fields)
            
        elif isinstance(self.input_fields, types.ListType):
            self.jsonpaths = list()
            for input_field in self.input_fields:
                self.jsonpaths.append(parse(input_field))

        

    def set_extractor(self, extractor):
        self.extractor = extractor
        return self

    def extract(self, doc):
        if isinstance(self.jsonpaths, JSONPath):
            renamed_inputs = dict()
            renamed_inputs[self.extractor.get_renamed_input_fields()] = [match.value for match in self.jsonpaths.find(doc)][0]
            
        elif isinstance(self.jsonpaths, types.ListType):
            renamed_inputs = dict()
            for jsonpath, renamed_input in itertools.izip(iter(self.jsonpaths), iter(self.extractor.get_renamed_input_fields())):
                renamed_inputs[renamed_input] = [match.value for match in jsonpath.find(doc)][0]
            
        else :
            raise ValueError("input_fields must be a string or a list")
        metadata = self.extractor.get_metadata()
        metadata['value'] = self.extractor.extract(renamed_inputs)
        metadata['source'] = self.input_fields
        if self.output_field in doc:
            output = doc[self.output_field]
            if isinstance(output, dict):
                output = [output, metadata]
            elif isinstance(output, types.ListType):
                output.append(metadata) 

        else:
            output = metadata
        doc[self.output_field] = output
        return doc

