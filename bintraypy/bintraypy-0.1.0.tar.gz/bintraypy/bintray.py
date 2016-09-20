import os

import requests


class Bintray(object):
  default_url = "https://bintray.com/api/v1"

  def __init__(self, username=None, key=None, url=default_url):
    self.username = username
    self.key = key
    self.url = url

  def upload_generic(self, local_file_path, organization, repo, package, version, remote_file_path=None, publish=False,
      override=False, explode=False):
    if not remote_file_path:
      remote_file_path = os.path.basename(local_file_path)
    path = '{}/{}/{}/{}/{}'.format(organization, repo, package, version, remote_file_path)
    url = '{}/content/{}?publish={}?override={}?explode={}'.format(self.url, path, _bool_to_int(publish),
      _bool_to_int(override), _bool_to_int(explode))
    with open(local_file_path, "rb") as file:
      print('Uploading file {} to {}'.format(local_file_path, path))
      if self.username and self.key:
        response = requests.put(url, auth=(self.username, self.key), data=file)
      else:
        response = requests.put(url, data=file)
      if response.status_code != 201:
        raise Exception('Failed to upload file: {0}\n{1}'.format(response.status_code, response.text))
    print('Uploaded successfully')


def _bool_to_int(b):
  return 1 if b else 0
