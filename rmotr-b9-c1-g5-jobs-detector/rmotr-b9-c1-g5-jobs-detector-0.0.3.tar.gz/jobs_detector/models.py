class BaseJobPosting(object):
    def __init__(self, description, scrape_url, keywords=None, combinations=None):
        self.scrape_url = scrape_url
        self.description = description
        self.keywords = []
        self._process_keywords(keywords)
        self.combinations = []
        if combinations:
            for cmb in combinations:
                if all([c.lower() in self.description.lower() for c in cmb.split('-')]):
                    words = [w.capitalize() for w in cmb.split('-')]
                    self.combinations.append('-'.join(words))

    def _process_keywords(self, keywords):
        for kw in keywords.split(','):
            if kw.lower() in self.description.lower():
                self.keywords.append(kw)


class HackerNewsJobPosting(BaseJobPosting):
    pass


class BaseJobManager(object):
    def __init__(self):
        self.jobs = []
        self._keyword_count = {}
        self._combinations_count = {}

    def __len__(self):
        return len(self.jobs)

    def append(self, job):
        self.jobs.append(job)

    def update_keywords(self, keywords):
        for job in self.jobs:
            job.update_keywords(keywords)

    def get_keyword_count(self):
        for job in self.jobs:
            for kw in job.keywords:
                try:
                    self._keyword_count[kw] += 1
                except KeyError:
                    self._keyword_count[kw] = 1
        return self._keyword_count

    def get_combination_count(self):
        for job in self.jobs:
            for kw in job.combinations:
                try:
                    self._combinations_count[kw] += 1
                except KeyError:
                    self._combinations_count[kw] = 1
        return self._combinations_count

    def keywords_to_string(self):
        ret_val = ''
        for k, v in self.get_keyword_count().items():
            ret_val += '{}: {} ({}%)\n'.format(k.capitalize(), v, int((float(v) / len(self)) * 100))
        return ret_val

    def combinations_to_string(self):
        ret_val = ''
        for k, v in self.get_combination_count().items():
            ret_val += '{}: {} ({}%)\n'.format(k, v, int((float(v) / len(self)) * 100))
        return ret_val

    def print_summary(self):
        template = '''
Total job posts: {}

Keywords:
{}

Combinations:
{}
'''
        return template.format(len(self), self.keywords_to_string(), self.combinations_to_string())


class HackerNewsManager(BaseJobManager):
    pass
