import re

from versiontracker.baseseekers import BaseSeeker, download_as_soup


_DATE_RE = re.compile("^(.*?) by .*$")


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.package = data.get('package', self.id)

    def data(self):
        url = "http://hackage.haskell.org/package/{}".format(self.package)
        soup = download_as_soup(url)
        version = None
        date = None
        for tr in soup.find("table", "properties").tbody.find_all(
                "tr", recursive=False):
            header = tr.th.string.strip()
            if header == "Versions":
                version = tr.td.strong.string
                url += "-" + version
            elif header == "Uploaded":
                match = _DATE_RE.match(tr.td.get_text().strip())
                date = match.group(1)
                break
        if not version or not date:
            raise Exception
        return {
            "id": self.id,
            "version": version,
            "url": url,
            "date": date,
        }

