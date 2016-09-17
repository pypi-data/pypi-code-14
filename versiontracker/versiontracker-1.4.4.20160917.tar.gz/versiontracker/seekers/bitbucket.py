from urllib.parse import urljoin

from versiontracker.baseseekers import \
    download_as_soup, GitServiceBaseSeeker, parse_date


class Seeker(GitServiceBaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(
            data, 'https://bitbucket.org/{project}/{repository}')

    def iterate_commits(self):
        soup = download_as_soup(self.base_url + '/commits/branch/default')
        for row in soup.find_all('tr', 'iterable-item'):
            yield {
                'message': row.find("td", "text").get_text().strip(),
                'date': row.time['datetime'],
                'url': urljoin(self.base_url, row.find("a", "hash")['href']),
            }

    def iterate_tags(self):
        soup = download_as_soup(self.base_url + '/downloads?tab=tags')
        for row in soup.find_all('tr', 'iterable-item'):
            tag = row.find("td", "name").get_text().strip()
            if tag == "tip":
                continue
            yield {
                'tag': tag,
                'date': row.time['datetime'],
                'url': urljoin(self.base_url, row.find(
                    "td", "hash").a['href']),
            }
