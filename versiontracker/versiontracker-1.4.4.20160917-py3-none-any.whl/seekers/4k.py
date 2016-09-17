from versiontracker.baseseekers import BaseSeeker
from . import xpath


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)

    def data(self):
        return xpath.Seeker({
            "id": self.id,
            "name": "xpath",
            "url": "https://www.4kdownload.com/download",
            "base": "//a[re:test(@href, '/app/{}_')]/parent::td"
                    "/following-sibling::td".format(self.id),
            "date": "/following-sibling::td",
        }).data()
