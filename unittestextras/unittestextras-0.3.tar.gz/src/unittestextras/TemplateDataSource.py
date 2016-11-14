__author__ = 'Sharon Lev'
__email__ = 'slev@apple.com'
__date__ = '11/10/16'

from json import loads, dumps

def TemplateDataSource(template, replacements_dict):
  """

  :param template:
  :param replacements_dict:
  :return:
  """
  string_template = dumps(template)

  string_template.replace()