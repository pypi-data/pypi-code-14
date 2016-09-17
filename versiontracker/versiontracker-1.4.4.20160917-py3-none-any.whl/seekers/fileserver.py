"""Seeker for a file server, either an HTTP server software such as Apache,
nginx, LightHTTPD, etc. that provides a relatively standard web interface to
browse files, or an FTP server."""

import re
from ftplib import FTP
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

from versiontracker.baseseekers import \
    BaseSeeker, download, resolve_path, parse_date, value_from_match

sorting_url_query = "?C=M;O=D"
ftp_entry_re = re.compile(
    r"^.{10}\s+\d+\s+(?P<user>\w+)\s+(?P<group>\w+)\s+\d+\s+"
    r"(?P<date>\w+\s+\d+\s+\d+(:\d+)?)\s+(?P<entry>.*)$")
img_pattern = "<img\s+(\S+\s+)*?src=\"[^\"]*\"\s*alt=\"[^\"]*\"(\s*/)?>"
a_start_patern = "<a\s+href=\"[^\"]*\"\s*>"
a_end_patern = "</a>"
pre_line_re = re.compile(
    r"^(?i)"
    r"(({img}|{a_start}{img}{a_end})\s*)?"
    r"<a\s+href=\"(?P<href>[^\"]*)\"\s*>[^<]*{a_end}\s*"
    r"(?P<date>\d{{2}}-\w{{3}}-\d{{4}} \d{{2}}:\d{{2}}|"
        r"\d{{4}}-\d{{2}}-\d{{2}}[T ]\d{{2}}:\d{{2}}(:\d{{2}}Z?)?)"
    r"\s*(?P<size>-|\d+(\.\d+)?k?\w?)".format(
        img=img_pattern, a_start=a_start_patern, a_end=a_end_patern))


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.url = data["url"]
        if not self.url.endswith("}"):
            self.url = self.url.rstrip("/") + "/" + \
                r"${latest:(\d+\.\d+(\.\d+(\.\d+)?)?)}"
        url_parts = urlparse(self.url)
        self.scheme = url_parts.scheme
        self.base_url = "{}://{}".format(url_parts.scheme, url_parts.netloc)
        self.path = self.url[len(self.base_url):]
        self.client = None
        self.requires_index = None

    def log_in(self):
        if self.scheme == "ftp":
            self.client = FTP(urlparse(self.url).netloc)
            self.client.login()

    def yielder_handle_ftp_entry(self, entry):
        match = ftp_entry_re.match(entry)
        if not match:  # e.g. 'total nnn'
            return
        date = parse_date(match.group("date"))
        name = match.group("entry")
        self.ftp_entries.append({"name": name, "date": date})

    def build_url(self, path):
        url = self.base_url + path
        while True:
            if self.requires_index == False:
                return url
            elif self.requires_index == True:
                return url + "index.html"
            elif self.scheme == "ftp":
                self.requires_index = False
            else:
                if download(url):
                    self.requires_index = False
                elif requests.head(url  + "index.html").status_code == 200:
                    self.requires_index = True
                else:
                    raise NotImplementedError

    def entry_yielder(self, path):
        if self.scheme == "ftp":
            self.client.cwd(path)
            self.ftp_entries = []
            self.client.dir(self.yielder_handle_ftp_entry)
            for entry in self.ftp_entries:
                yield entry
        elif self.scheme.startswith("http"):
            html = download(self.build_url(path))
            soup = BeautifulSoup(html, "lxml")
            # Check for pre must go first because of scenarios where there is
            # an unrelated table before the pre element, such as in
            # http://goo.gl/ZjLGEd
            pre = soup.find("pre")
            # KDE’s starts with a pre that contains no tags, and the actual
            # content is on a table afterwards.
            if pre and pre.a is not None:
                for line in html.splitlines():
                    match = pre_line_re.match(line.strip())
                    if not match:
                        continue
                    try:
                        date = parse_date(match.group("date"))
                    except:
                        continue
                    name = match.group("href").rstrip("/")
                    yield {"name": name, "date": date}
                return
            table = soup.find("table")
            if table:
                for row in soup.find("table").find_all("tr"):
                    cells = row.find_all("td")
                    if not cells:
                        continue
                    entry_column = 0
                    if (cells[entry_column].find("img") or
                            not cells[entry_column].get_text().strip()):
                        entry_column += 1
                    date_column = entry_column+1
                    date = None
                    while True:
                        try:
                            date_string = cells[date_column].string.strip()
                            if not date_string or date_string == "\xa0":
                                break
                            date = parse_date(date_string)
                            break
                        except ValueError:
                            date_column += 1
                        except IndexError:
                            break
                    if date is None:
                        continue
                    name = cells[entry_column].a["href"].rstrip("/")
                    if name[0] in ".?/":
                        continue
                    yield {"name": name, "date": date}
                return
            ul = soup.find("ul")
            if ul:
                for li in soup.find("ul", {"id": "files"}).find_all(
                        "li", recursive=False)[2:]:
                    date = parse_date(
                        li.find("span", "date").get_text())
                    name = li.find(
                        "span", "name").get_text().strip().rstrip("/")
                    yield {"name": name, "date": date}
                return
            raise NotImplementedError
        else:
            raise NotImplementedError

    def data(self):
        self.log_in()
        path, name, date, match = resolve_path(self.path, self.entry_yielder)
        version = value_from_match(match, name)
        return {
            "id": self.id,
            "version": version,
            "url": self.build_url(path),
            "date": date,
        }
