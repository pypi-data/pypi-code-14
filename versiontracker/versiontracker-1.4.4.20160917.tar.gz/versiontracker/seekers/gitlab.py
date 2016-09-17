from versiontracker.baseseekers import download_as_soup, GitServiceBaseSeeker


class Seeker(GitServiceBaseSeeker):

    def __init__(self, data):
        url = data.get('url', 'https://gitlab.com/{project}/{repository}')
        super(Seeker, self).__init__(data, url)

    def iterate_commits(self):
        soup = download_as_soup(self.base_url + '/commits/master')
        for ul in soup.find_all('ul', 'commit-list'):
            for li in ul.find_all('li'):
                commit_link = li.find('a', 'commit-row-message')
                commit = commit_link['href'].split('/')[-1]
                message = commit_link.get_text().strip()
                yield {
                    'message': message,
                    'date': li.find('time')['datetime'],
                    'url': self.base_url + '/commit/' + commit,
                }

    def iterate_tags(self):
        soup = download_as_soup(self.base_url + '/tags')
        for tag in soup.find_all("span", { "item-title" }):
            code = tag.get_text().strip()
            date = tag.parent.parent.find_next_sibling(
                    "div").find("time")["datetime"]
            yield {
                'tag': code,
                'date': date,
                'url': self.base_url + '/tags/' + code,
            }
