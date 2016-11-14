__author__ = 'Sharon Lev'
__email__ = 'sharon_lev@yahoo.com'
__date__ = '10/11/16'

from json import load, loads
from urlparse import urlparse
from requests import get
from plistlib import readPlist, readPlistFromString


def DataSource(source):
  """
  A mechanism for providing a DataProvider data from an external resource (external to test class module)

  :param source: url or file name containing test data content
  :return: lambda representing the file content
  """
  return lambda: (_json_source(source) if 'json' in source else _plist_source(source))

def _json_source(source):
  """
  :param source: filename (local or remote) containing test data in json format.
  :return: list of sets of data from json file
  """
  source = urlparse(source)
  content = []
  if source.netloc:
    content = loads(get(source.geturl(), headers={"Accepts":"application/json"}).json())
  else:
    with open(source.path,'r') as file:
      content = load(file)

  return content if isinstance(content, list) else content.values()


def _plist_source(source):
  """

  :param source: url or file name containing test data content in plist format.
  :return: list of sets of data from plist file
  """
  source = urlparse(source)
  content = readPlistFromString(get(source.geturl()).content) if source.netloc else readPlist(source.path)
  return content
