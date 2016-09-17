import json
import re

import requests

from versiontracker.baseseekers import BaseSeeker, parse_date


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.package = data.get('package', data['id'])
        self.version_re = data.get('version', None)
        if self.version_re:
            self.version_re = re.compile(self.version_re)

    def data(self):
        response = requests.get("https://pypi.python.org/pypi/{}/json".format(
            self.package))
        data = json.loads(response.text)
        version = data["info"]["version"]
        if self.version_re and not self.version_re.search(version):
            versions_by_date = {}
            for candidate_version, version_data in data["releases"].items():
                if len(version_data):
                    date = parse_date(version_data[0]["upload_time"])
                    if date not in versions_by_date:
                        versions_by_date[date] = []
                    versions_by_date[date].append(candidate_version)
            version = None
            for date in sorted(versions_by_date.keys()):
                for candidate_version in versions_by_date[date]:
                    if self.version_re.match(candidate_version):
                        version = candidate_version
                        break
            if version is None:
                raise NotImplementedError
        date = data["releases"][version][0]["upload_time"]
        url = "https://pypi.python.org/pypi/{}/{}".format(
            self.package, version)
        return {
            "id": self.id,
            "version": version,
            "date": date,
            "url": url,
        }
