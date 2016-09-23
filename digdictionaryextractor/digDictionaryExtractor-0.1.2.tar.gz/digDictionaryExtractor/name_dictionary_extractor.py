from dictionary_extractor import DictionaryExtractor
import re

# already lower cased 
valid_token_re = re.compile('[a-z].*[a-z]')

def get_name_dictionary_extractor(t):

    return DictionaryExtractor()\
        .set_trie(t)\
        .set_pre_filter(lambda x:valid_token_re.match(x))\
        .set_pre_process(lambda x:x.lower())\
        .set_metadata({'extractor':'dig_name_dictionary_extractor'})

