from digExtractor.curry import curry
from digExtractor.extractor import extract
from dictionary_extractor import dictionary_extractor
import re

# already lower cased 
valid_token_re = re.compile('[a-z].*[a-z]')

def get_name_dictionary_extractor(t, 
	preProcess= lambda x: x.lower(), 
	preFilter = lambda x: valid_token_re.match(x), 
	postFilter = lambda x: isinstance(x,basestring)):

	return extract(renamed_input_fields = ['tokens'], 
			extractor =dictionary_extractor(t=t, 
				preProcess=preProcess,
				preFilter=preFilter,
				postFilter=postFilter))


