import re

from versiontracker.baseseekers import \
    BaseSeeker, download_as_soup, resolve_path, value_from_match

latest_re = re.compile(r"^(?P<path>.*):\s+released\s+on\s+(?P<date>.*)$")


class SourceForgeInvalidData(Exception):
    def __init__(self, url):
        self.url = url


class UndefinedLatestFile(Exception):
    pass


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        default_path = r"${latest:(\d+\.\d+(\.\d+(\.\d+)?)?)}"
        self.path = data.get("path", default_path)
        if not self.path.endswith("}"):
            self.path = self.path.rstrip("/") + "/" + default_path
        self.base_url = "http://sourceforge.net/projects/{}/files".format(
            data.get("project", self.id))


    def _row_date(self, row):
        return row.find_all("td")[0].find("abbr")["title"]


    def latest_data(self):
        if self.path.count("/") > 0:
            raise UndefinedLatestFile
        name_re = re.compile(":".join(self.path[:-1].split(":")[1:]))
        soup = download_as_soup(self.base_url)
        download_bar = soup.find("div", "download-bar")
        if not download_bar:
            raise UndefinedLatestFile
        link = download_bar.find("a")
        if not link:
            raise UndefinedLatestFile
        match = latest_re.match(link["title"])
        if not match:
            raise UndefinedLatestFile
        path_parts = match.group("path").split("/")
        date = match.group("date")
        path = "/".join(path_parts[:-1]) + "/"
        name = path_parts[-1]
        match = name_re.search(name)
        if not match:
            raise UndefinedLatestFile
        return path, name, date, match


    def entry_yielder(self, path):
        soup = download_as_soup(self.base_url + path)
        table_body = soup.find("table", { "id": "files_list" }).tbody
        for table_row in table_body.find_all("tr"):
            if table_row.has_attr("class") and "empty" in table_row["class"]:
                return
            name = table_row["title"]
            date = self._row_date(table_row)
            yield {"name": name, "date": date}


    def data(self):
        try:
            path, name, date, match = self.latest_data()
        except UndefinedLatestFile:
            path, name, date, match = resolve_path(
                self.path, self.entry_yielder)
        version = value_from_match(match, name)
        return {
            "id": self.id,
            "version": version,
            "url": self.base_url + path,
            "date": date,
        }
