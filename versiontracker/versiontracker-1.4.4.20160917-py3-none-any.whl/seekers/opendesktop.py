import re
from datetime import datetime, timedelta

from versiontracker.baseseekers import BaseSeeker, download_as_soup
from versiontracker import parse_date

_RELATIVE_TIME_RE = re.compile(
    r"^(?P<hours>\d+) hours? ago|(?P<days>\d+) days? ago$")


def get_value(row_soup):
    return row_soup.find("span", {"class": "value"}).text.strip()


def timedelta_from_string(string):
    match = _RELATIVE_TIME_RE.match(string)
    kwargs = {k: -int(v) for k, v in match.groupdict().items()
              if v is not None}
    return timedelta(**kwargs)


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        project = data['project']
        site = data.get("site", "linux-apps")
        top_domain = "com" if site == "linux-apps" else "org"
        self.url = "https://www.{}.{}/p/{}/".format(
            site, top_domain, project)

    def data(self):
        soup = download_as_soup(self.url)
        version = None
        date = None
        for row in soup.find("div", class_="details").find_all(
                "div", {"class": "row"}):
            field_label = row.find("span").text.strip()
            if field_label == "version":
                version = get_value(row)
            elif (field_label == "updated" or
                    not date and field_label == "added"):
                date_string = get_value(row).strip()
                try:
                    date =  parse_date(date_string)
                except ValueError:
                    date = datetime.now() + timedelta_from_string(date_string)
        return {
            "id": self.id,
            "version": version,
            "url": self.url,
            "date": date
        }
