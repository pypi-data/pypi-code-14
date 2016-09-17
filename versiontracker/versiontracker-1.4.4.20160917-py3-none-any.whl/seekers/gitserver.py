import re

from versiontracker.baseseekers import \
    BaseSeeker, GitBaseSeeker, download_as_soup


_CGIT_RE = re.compile(r"\bcgit\b")


class GitServerBaseSeeker(GitBaseSeeker):

    def __init__(self, data):
        super(GitServerBaseSeeker, self).__init__(data)
        self.url = data.get('url', None)


class CgitSeeker(GitServerBaseSeeker):

    def iterate_commits(self):
        soup = download_as_soup(self.url.rstrip("/") + "/log/")
        for tr in soup.find("table", "list").find_all("tr")[1:]:
            tds = tr.find_all('td')
            commit_link = tds[1].a
            commit = commit_link['href'].split('=')[-1]
            yield {
                'message': commit_link.get_text().strip(),
                'date': tds[0].span['title'],
                'url': self.url.rstrip('/') + '/commit/?id=' +
                                 commit,
            }

    def iterate_tags(self):
        soup = download_as_soup(self.url.rstrip("/") + "/refs/tags")
        for tr in soup.find("table", "list").find_all("tr")[1:]:
            tds = tr.find_all('td')
            tag = tds[0].get_text().strip()
            try:
                date_string = tds[3].span['title'].replace(
                    '(', '').replace(')', '')
                yield {
                    'tag': tag,
                    'date': date_string,
                    'url': self.url.rstrip('/') + '/tag/?h=' +
                                     tag,
                }
            except KeyError:
                yield {
                    'tag': tag,
                    'url': self.url.rstrip('/') + '/tag/?h=' +
                                     tag,
                }

    def complete_data_from_tag_data(self, data, tag_data):
        if 'date' not in tag_data:
            soup = download_as_soup(self.url.rstrip('/') + '/commit/?h=' +
                                    tag_data['tag'])
            date_string = soup.find('table', 'commit-info').find_all(
                'tr')[1].find_all('td')[1].string.replace('(', '').replace(
                    ')', '')
            data['date'] = date_string


class GitwebSeeker(GitServerBaseSeeker):

    def iterate_commits(self):
        soup = download_as_soup(self.url.rstrip('/') + '/shortlog')
        for tr in soup.find('table', 'shortlog').find_all('tr'):
            tds = tr.find_all('td')
            commit_link = tds[2].a
            commit = commit_link['href'].split('/')[-1]
            yield {
                'message': commit_link.get_text().strip(),
                'date': tds[0].get_text(),
                'url': self.url.rstrip('/') + '/commit/' + commit,
            }

    def iterate_tags(self):
        soup = download_as_soup(self.url.rstrip("/") + "/tags")
        for tr in soup.find("table", "tags").find_all("tr"):
            tds = tr.find_all('td')
            commit_link = tds[1].a
            tag_link = tds[3].a
            if tag_link:
                tag_hash = tag_link['href'].split('/')[-1]
                url = self.url.rstrip('/') + '/tag/' + tag_hash
            else:
                commit = commit_link['href'].split('/')[-1]
                url = self.url.rstrip('/') + '/commit/' + commit
            yield {
                'tag': commit_link.get_text().strip(),
                'url': url,
            }

    def complete_data_from_tag_data(self, data, tag_data):
        soup = download_as_soup(tag_data['url'])
        date = soup.find("span", "datetime")
        if not date:
            table = soup.find("table", "object_header")
            for tr in table.find_all("tr"):
                if not tr.td.get_text().strip():
                    date = tr.find_all("td")[1]
        date = date.string
        data["date"] = date


class ParametrizedGitwebSeeker(GitServerBaseSeeker):

    def iterate_commits(self):
        soup = download_as_soup(self.url + '&a=shortlog')
        for tr in soup.find('table', 'shortlog').find_all('tr'):
            tds = tr.find_all('td')
            commit_link = tds[2].a
            commit = commit_link['href'].split('/')[-1]
            yield {
                'message': commit_link.get_text().strip(),
                'date': tds[0].get_text(),
                'url': self.url + '&commit=' + commit,
            }

    def iterate_tags(self):
        soup = download_as_soup(self.url + "&a=tags")
        for tr in soup.find("table", "tags").find_all("tr"):
            tds = tr.find_all('td')
            commit_link = tds[1].a
            tag_link = tds[3].a
            if tag_link:
                tag_hash = tag_link['href'].split('/')[-1]
                url = self.url + '&tag=' + tag_hash
            else:
                commit = commit_link['href'].split('/')[-1]
                url = self.url + '&commit=' + commit
            yield {
                'tag': commit_link.get_text().strip(),
                'url': url,
            }

    def complete_data_from_tag_data(self, data, tag_data):
        soup = download_as_soup(tag_data['url'])
        date = soup.find("span", "datetime").string
        data["date"] = date


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        url = data["url"]
        if '?p=' in url:
            self.seeker = ParametrizedGitwebSeeker(data)
            return
        match = _CGIT_RE.search(url)
        if match:
            self.seeker = CgitSeeker(data)
            return
        soup = download_as_soup(url)
        generator = soup.find("meta", {"name": "generator"})["content"]
        if "cgit" in generator:
            self.seeker = CgitSeeker(data)
        elif "gitweb" in generator:
            self.seeker = GitwebSeeker(data)

    def data(self):
        return self.seeker.data()
