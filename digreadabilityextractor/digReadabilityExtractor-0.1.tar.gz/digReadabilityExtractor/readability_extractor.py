from digExtractor.curry import curry
from digExtractor.extractor import extract
from itertools import ifilter

@curry
def readability_extractor(input, 
	recallPriority=True,
	htmlPartial=False):
  from digReadabilityExtractor.readability.readability import Document
  from bs4 import BeautifulSoup
  try:
        if 'html' in input:
            html = input['html']
            readable = Document(html,recallPriority=recallPriority).summary(html_partial=htmlPartial)
            cleantext = BeautifulSoup(readable.encode('utf-8'), 'lxml').strings
            readability_text = ' '.join(cleantext)
            return readability_text
        else:
            return ''
  except Exception, e:
        print 'Error in extracting readability %s' % e
        return ''


def get_readability_extractor(recallPriority=True,
	htmlPartial=False):
	return extract(renamed_input_fields = ['html'], 
			extractor =readability_extractor(recallPriority=recallPriority,
				htmlPartial=htmlPartial))

