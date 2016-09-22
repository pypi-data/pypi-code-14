import itertools
import types

class ExtractorProcessor:

	def set_output_field(self, output_field):
		self.output_field = output_field
		return self

	def set_input_fields(self, input_fields):
		if not (isinstance(input_fields, basestring) or isinstance(input_fields, types.ListType)):
			raise ValueError("input_fields must be a string or a list")
		self.input_fields = input_fields
		return self

	def set_extractor(self, extractor):
		self.extractor = extractor
		return self

	def extract(self, doc):
		if isinstance(self.input_fields, basestring):
			renamed_inputs = dict()
			renamed_inputs[self.extractor.get_renamed_input_fields()] = doc[self.input_fields]
			
		elif isinstance(self.input_fields, types.ListType):
			inputs = dict(filter(lambda i:i[0] in self.input_fields, doc.iteritems()))
			renamed_inputs = dict()
			for input, renamed_input in itertools.izip(iter(self.input_fields), iter(self.extractor.get_renamed_input_fields())):
				renamed_inputs[renamed_input] = inputs[input]
			
		else :
			raise ValueError("input_fields must be a string or a list")
		metadata = self.extractor.get_metadata()
		metadata['value'] = self.extractor.extract(renamed_inputs)
		doc[self.output_field] = metadata
		return doc

