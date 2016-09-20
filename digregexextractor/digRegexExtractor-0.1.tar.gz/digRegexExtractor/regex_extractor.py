from digExtractor.curry import curry
from digExtractor.extractor import extract
import re

@curry
def regex_extractor(input, regex):
    try:
        extracts = list()        
        extracts = regex.findall(input['text'])
        return extracts
    except:
        return list()

def get_regex_extractor(regex) :
	return extract(renamed_input_fields = ['text'], extractor =regex_extractor(regex=regex))
