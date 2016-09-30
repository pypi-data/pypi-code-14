from argparse import ArgumentParser
import sys

from jira import JIRA

from jira_issue_recommender.util import get_issues, get_issues_tfidf, get_most_similar


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = ArgumentParser(
        description='Add issue recommendations to issues'
    )

    parser.add_argument(
        '--jira-server-url',
        help='JIRA server url',
        required=True,
    )

    parser.add_argument(
        '--username',
        help='JIRA username',
        required=True,
    )

    parser.add_argument(
        '--password',
        help='JIRA password',
        required=True,
    )

    parser.add_argument(
        '--finished-issues-query',
        help='JQL query for finding issues that will be used in recommendations',
        required=True,
    )

    parser.add_argument(
        '--new-issues-query',
        help='JQL query for finding issues that need recommendations',
        required=True,
    )

    parser.add_argument(
        '--comment-preface',
        help='String added to beginning of recommendations comment',
        required=False,
    )

    cli_args = parser.parse_args(argv)

    client = JIRA(cli_args.jira_server_url, basic_auth=(cli_args.username, cli_args.password))

    finished_issues = get_issues(client, cli_args.finished_issues_query)
    new_issues = get_issues(client, cli_args.new_issues_query)
    all_issues = dict(list(finished_issues.items()) + list(new_issues.items()))

    tfidf = get_issues_tfidf(all_issues)

    for issue_key in new_issues.keys():
        similar = get_most_similar(issue_key, all_issues, new_issues, tfidf)

        new_comment = '{}\n{}'.format(
            cli_args.comment_preface,
            '\n'.join([
                '{} {} - {} hours'.format(key, info['title'], round((info['timespent'] or 0) / 60.0 / 60.0, 1))
                for key, info in similar.items()
            ])
        )

        existing_comments = [comment for comment in client.comments(issue_key) if comment.body.startswith(cli_args.comment_preface)]
        if len(existing_comments) > 0:
            if len(existing_comments) == 1:
                existing_comment = existing_comments[0]
                if existing_comment.body == new_comment:
                    print('skipping {}'.format(issue_key))
                    continue
                else:
                    import ipdb
                    ipdb.set_trace()
                    print('deleting {}'.format(issue_key))
                    existing_comment.delete()
            else:
                raise Exception('more than one comment was added to {}. this should not happen!'.format(issue_key))

        client.add_comment(issue_key, new_comment)
