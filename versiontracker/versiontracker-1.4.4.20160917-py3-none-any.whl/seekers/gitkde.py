import re

from versiontracker.baseseekers import download_as_soup, GitServiceBaseSeeker


class Seeker(GitServiceBaseSeeker):

    def __init__(self, data):
        # Default to a tag regular expression that skips pre-releases (x.y.9n)
        if data.get('commit', data.get('tag', None)) is None:
            data['tag'] = '^(?:v|{}-)(\\d+(?:\\.\\d+)*' \
                          '(?:\\.(?:\\d|[0-8]\\d+)))$'.format(
                re.escape(data['id']))
        super(Seeker, self).__init__(
            data, 'https://quickgit.kde.org/?p={project}.git')

    def iterate_commits(self):
        soup = download_as_soup(self.base_url + '&a=shortlog')
        for tr in soup.find('table').find_all('tr'):
            tds = tr.find_all('td')
            commit_link = tds[2].a
            commit = commit_link['href'].split('=')[-1]
            yield {
                'message': commit_link.get_text().strip(),
                'date': tds[0].find('time')['datetime'],
                'url': self.base_url + '&a=commit&h=' + commit,
            }

    def iterate_tags(self):
        soup = download_as_soup(self.base_url + '&a=tags')
        for tr in soup.find("table").find_all("tr"):
            tds = tr.find_all('td')
            commit_link = tds[1].a
            tag_link = tds[3].a
            if tag_link:
                tag = tag_link['href'].split('=')[-1]
                url = self.base_url + '&a=tag&t=' + tag
            else:
                commit = commit_link['href'].split('/')[-1]
                url = self.base_url + '&a=commit&h=' + commit
            yield {
                'tag': commit_link.get_text().strip(),
                'date': tds[0].find('time')['datetime'],
                'url': url,
            }
