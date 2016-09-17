import requests

from versiontracker.baseseekers import \
    download_as_soup, GitServiceBaseSeeker, html_to_soup, parse_date


class Seeker(GitServiceBaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(
            data, 'https://github.com/{project}/{repository}')
        self.ignore_latest = data.get("ignore-latest", False)

    def iterate_commits(self):
        soup = download_as_soup(self.base_url + '/commits')
        for li in soup.find_all('li', 'commit'):
            commit_link = li.find('a', 'message')
            commit = commit_link['href'].split('/')[-1]
            yield {
                'message': commit_link.get_text().strip(),
                'date': parse_date(li.find(
                    'relative-time')['datetime']),
                'url': self.base_url + '/commit/' + commit,
            }

    def latest_release(self):
        response = requests.get(self.base_url + '/releases/latest',
                                 allow_redirects=True)
        if not response.url.endswith("/releases"):
            soup = html_to_soup(response.text)
            return {
                'tag': response.url.split("/")[-1],
                'date': parse_date(
                    soup.find('relative-time')['datetime']),
                'url': response.url,
            }
        return {}

    def iterate_tags(self):
        if not self.ignore_latest:
            tag_data = self.latest_release()
            if tag_data:
                yield tag_data
        soup = download_as_soup(self.base_url + '/tags')
        for tr in soup.find('table', 'releases-tag-list').find_all('tr'):
            tag = tr.find('span', 'tag-name').get_text().strip()
            yield {
                'tag': tag,
                'date': parse_date(
                    tr.find('relative-time')['datetime']),
                'url': self.base_url + '/releases/tag/' + tag,
            }
