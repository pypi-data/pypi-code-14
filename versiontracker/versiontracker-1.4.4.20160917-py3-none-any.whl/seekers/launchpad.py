import re

from versiontracker.baseseekers import BaseSeeker, download_as_soup
from . import xpath


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.project = data.get("project", data["id"])

    def data(self):
        data = xpath.Seeker({
            "id": self.id,
            "name": "xpath",
            "url": "https://launchpad.net/{}".format(self.project),
            "base": "//div[@id='downloads']",
            "version": "//div[re:test(@class, '\\bversion\\b')]",
            "date": "//div[re:test(@class, '\\breleased\\b')]",
        }).data()
        data['version'] = re.search(
            "^Latest version is (.*)$", data['version']).group(1)
        data['date'] = re.search("^released on (.*)$", data['date']).group(1)
        return data
