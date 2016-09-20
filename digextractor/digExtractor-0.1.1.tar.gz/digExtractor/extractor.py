from curry import curry
import itertools

@curry
def extract(doc, output_field, input_fields, renamed_input_fields, extractor):
	inputs = dict(filter(lambda i:i[0] in input_fields, doc.iteritems()))
	renamed_inputs = dict()
	for input, renamed_input in itertools.izip(iter(input_fields), iter(renamed_input_fields)):
		renamed_inputs[renamed_input] = inputs[input]
	doc[output_field] = extractor(renamed_inputs)
	return doc
