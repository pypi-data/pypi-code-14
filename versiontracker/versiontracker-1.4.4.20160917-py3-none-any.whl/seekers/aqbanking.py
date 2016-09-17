from versiontracker.baseseekers import BaseSeeker, download_as_soup
from . import xpath


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.package = data['package']

    def data(self):
        return xpath.Seeker({
            "id": self.id,
            "name": "xpath",
            "url": "http://www.aquamaniac.de/sites/download/packages.php"
                   "?package={}&showall=1".format(self.package),
            "base": "//body/table[3]//tr[1]/td[3]/table[2]/"
                    "tr[position() mod 2 = 1 and position() > 3]/td[2]"
                    "//a[1][not(re:test(@name, 'beta$'))]",
            "version": "/@name",
            "date": "/parent::b/text()",
            "url-xpath": "/@href",
        }).data()
