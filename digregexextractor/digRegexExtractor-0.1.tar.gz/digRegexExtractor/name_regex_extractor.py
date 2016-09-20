import re
from regex_extractor import get_regex_extractor

name_regex = re.compile('(?:my[\s]+name[\s]+is[\s]+([-a-z0-9@$!]+))', re.IGNORECASE)

def get_name_regex_extractor():
	return get_regex_extractor(name_regex)