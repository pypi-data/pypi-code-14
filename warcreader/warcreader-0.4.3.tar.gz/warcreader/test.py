from warcreader import WarcFile
from gzip import GzipFile
from sys import argv

if __name__ == '__main__':
	with GzipFile(argv[1], mode='rb') as gzip_file:
		warc_file = WarcFile(gzip_file)
		for webpage in warc_file:
			print(webpage.uri)
