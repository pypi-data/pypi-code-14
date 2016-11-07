import click
import requests
import requests_cache
from bs4 import BeautifulSoup

from jobs_detector import exceptions
from jobs_detector.models import HackerNewsManager, HackerNewsJobPosting

requests_cache.install_cache('jobs_cache')

DEFAULT_KEYWORDS = [
    'Remote', 'Postgres', 'Python', 'Javascript', 'React', 'Pandas'
]

DEFAULT_COMBINATIONS = ['Remote-Python-Flask', 'Remote-Django']


def fetch_data(url):
    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        raise exceptions.RequestException('Timeout')
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        raise exceptions.RequestException('Too Many Redirects')
    except requests.exceptions.RequestException as e:
        print(e)
        raise e
    return r


@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords, combinations):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    URL_HACKER_NEWS = 'https://news.ycombinator.com/item?id={}'

    result = fetch_data(URL_HACKER_NEWS.format(post_id))
    soup = BeautifulSoup(result.text, 'html.parser')

    job_mgr = HackerNewsManager()

    for a_thing in soup.select('.athing'):
        if a_thing.find('img', width=0):
            try:
                posting_text = a_thing.find("span", class_="c00").get_text()

                hn_posting = HackerNewsJobPosting(posting_text,
                                                  URL_HACKER_NEWS,
                                                  keywords=keywords,
                                                  combinations=combinations)
                job_mgr.append(hn_posting)
            except AttributeError:
                pass

    print(job_mgr.print_summary())


if __name__ == '__main__':
    jobs_detector()
