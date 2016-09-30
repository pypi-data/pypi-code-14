from operator import itemgetter
from re import sub

from html.parser import HTMLParser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class MLStripper(HTMLParser):
    '''
    From http://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
    '''
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def clean_text(text):
    return ' '.join(sub(
        r'[^\x00-\x7F]+',
        ' ',
        strip_tags(text)).split()
    ).encode('utf-8') if text else ''


def get_issues(client, search_param):
    start = 0
    issues = {}
    while True:
        issues_sub = client.search_issues(search_param, start, fields=['summary', 'description', 'assignee', 'timespent'])
        if len(issues_sub)  == 0:
            break
        start = start + len(issues_sub)
        issues.update({
            issue.key: {
                'title': issue.fields.summary,
                'description': clean_text(issue.fields.description),
                'assignee': getattr(issue.fields.assignee, 'displayName', None),
                'timespent': issue.fields.timespent,
            }
            for issue in issues_sub
        })

    return issues


def get_issues_tfidf(issues):
    return TfidfVectorizer().fit_transform([
        '{} {}'.format(info['title'], info['description'])
        for issue, info in issues.items()
    ])


def get_most_similar(issue_key, all_issues, new_issues, tfidf):
    index_of_search_doc = list(all_issues.keys()).index(issue_key)

    cosine_similarities = linear_kernel(
        tfidf[index_of_search_doc:(index_of_search_doc + 1)],
        tfidf
    ).flatten()

    indicies_excluded = [index for index, key in enumerate(list(all_issues.keys())) if key in new_issues]
    indicies = [index for index in cosine_similarities.argsort() if index not in indicies_excluded]

    most_similar = indicies[:-5:-1]
    most_similar_keys = itemgetter(*most_similar)(list(all_issues.keys()))

    return [
        (key, info)
        for key, info in all_issues.items()
        if key in most_similar_keys
    ]


def get_comment(comment_preface, issues):
    return '{}\n{}'.format(
        comment_preface,
        '\n'.join([
            '{} {} - {} hours'.format(key, info['title'], round((info['timespent'] or 0) / 3600.0, 1))
            for key, info in issues
        ])
    )
