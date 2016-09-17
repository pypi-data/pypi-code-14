import re
from ftplib import FTP

import requests
from bs4 import BeautifulSoup

from versiontracker.baseseekers import BaseSeeker, download_as_soup


def apt_seeker():
    url = "https://tracker.debian.org/pkg/apt"
    soup = download_as_soup(url)
    target_url = "https://packages.debian.org/source/stable/apt"
    version = soup.find("a", {"href": target_url}).string.strip()
    from . import gitserver
    date = gitserver.Seeker({
        "id": "apt",
        "url": "https://anonscm.debian.org/cgit/apt/apt.git",
        "tag": "^(?P<version>{})$".format(re.escape(version)),
    }).data()["date"]
    return {
        "version": version,
        "url": url,
        "date": date,
    }


def cuda_seeker():
    url = "https://developer.nvidia.com/cuda-downloads"
    soup = download_as_soup(url)
    match = re.match(
        "CUDA (?P<version>\\d+(\\.\\d+)+) Downloads",
        soup.find("title").string)
    major_version = match.group("version")
    md5_url = "http://developer.download.nvidia.com/compute/cuda/" \
              "{}/Prod/docs/sidebar/md5sum.txt".format(major_version)
    md5 = requests.get(md5_url).text
    match = re.search(
        "cuda_(?P<version>\\d+(\\.\\d+)+)_linux\\.run", md5)
    version = match.group("version")
    file_url = "http://developer.download.nvidia.com/compute/cuda/" \
               "{}/Prod/local_installers/cuda_{}_linux.run".format(
                   major_version, version)
    response = requests.head(file_url)
    date = response.headers["Last-Modified"]
    return {
        "version": version,
        "url": url,
        "date": date
    }


def freedroid_seeker():
    url = "http://www.freedroid.org/"
    soup = download_as_soup(url)
    version_span = soup.find("span", {"id": "download_lastversion"})
    package_string = version_span.get_text().strip()
    package_folder = ".".join(package_string.split(".")[:2])
    package_sources_subdir = \
        "pub/freedroid/{package_folder}/{package}.tar.gz".format(
            package=package_string, package_folder=package_folder)
    version = "-".join(package_string.split("-")[1:])
    ftp_domain = "ftp.osuosl.org"
    ftp = FTP(ftp_domain)
    ftp.login()
    data = ftp.sendcmd("MDTM {}".format(package_sources_subdir))
    return {
        "version": version,
        "url": "ftp://{}/{}".format(
            ftp_domain, package_sources_subdir),
        "date": data.split(" ")[1]
    }


def grass_seeker():
    from . import xpath
    data = xpath.Seeker({
        "id": "grass",
        "name": "xpath",
        "url": "https://grass.osgeo.org/download/software/sources/",
        "base": "//a/@href[re:test(., '^grass\\d+/source/grass-\\d+(\\.\\d+)+"
                "\\.tar\\.gz$')]",
        "date-url": ""
    }).data()
    data['version'] = re.search("\\d+(?:\\.\\d+)+", data['version']).group(0)
    data['url'] = "http://trac.osgeo.org/grass/wiki/Release/{}-News".format(
        data['version'])
    return data


def mozjs_seeker():
    domain = "https://developer.mozilla.org"
    url = "{}/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases".format(
        domain)
    soup = download_as_soup(url)
    path = soup.find("h2", {"id": "Current_release"}).find_next_sibling(
        "ul").a["href"]
    url = "{}{}".format(domain, path)
    soup = download_as_soup(url)
    article_note = soup.find(
        "article", {"id": "wikiArticle"}).find("div", {"class": "note"})
    download_link = article_note.a["href"]
    mozjs_re = re.compile("mozjs-(\\d+(\\.\\d+)+)")
    version = mozjs_re.search(download_link).group(1)
    date = article_note.find("span", {"class": "gI"}).get_text()
    return {
        "version": version,
        "url": url,
        "date": date
    }


def openbsd_seeker():
    base_url = "http://www.openbsd.org/"
    soup = download_as_soup(base_url)
    file_url_re = re.compile("^\\d+\\.html$")
    link = soup.find("table").tr.find_all("td", recursive=False)[2].find(
        "a", {"href": file_url_re})
    url = base_url + link["href"]
    text = requests.get(url).text
    soup = BeautifulSoup(text, "lxml")
    version = soup.find("h2").get_text().strip().split()[-1]
    match = re.search("\nReleased (?P<date>.*)<br>", text)
    return {
        "version": version,
        "url": url,
        "date": match.group("date")
    }


def thunderbird_seeker():
    soup = download_as_soup("https://www.mozilla.org/en-US/thunderbird/all/")
    file_url_re = re.compile(
        "https://download\\.mozilla\\.org/\\?product=thunderbird-"
        "(?P<version>\\d+(\\.\\d+)+)-SSL&.*$")
    link = soup.find("a", {"href": file_url_re})
    match = file_url_re.match(link["href"])
    version = match.group("version")
    url = "https://ftp.mozilla.org/pub/thunderbird/releases/" \
          "{}/source/".format(version)
    filename = "thunderbird-{}.source.tar.xz".format(version)
    response = requests.head(url + filename)
    return {
        "version": version,
        "url": url,
        "date": response.headers["Last-Modified"]
    }


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)

    def data(self):
        data = globals()[self.id.replace("-", "_") + "_seeker"]()
        data["id"] = self.id
        return data
