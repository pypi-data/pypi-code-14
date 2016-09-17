from versiontracker.baseseekers import BaseSeeker
from . import xpath


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.project = data.get("project", data["id"])
        self.package = data.get("package",data["id"])

    def data(self):
        return xpath.Seeker({
            "id": self.id,
            "name": "xpath",
            "url": "https://alioth.debian.org/projects/{}/".format(
                self.project),
            "base": "//table[@summary='Latest file releases']//tr/td[1]"
                    "[re:test(., '\\b{}\\b')]".format(self.package),
            "version": "/following-sibling::td",
            "date": "/following-sibling::td/following-sibling::td",
        }).data()
