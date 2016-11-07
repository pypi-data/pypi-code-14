import click
import requests
from bs4 import BeautifulSoup

from jobs_detector import settings

DEFAULT_KEYWORDS = [
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas'
]

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
    # HINT: You will probably want to use the `BeautifulSoup` tool to
    # parse the HTML content of the website

    keywords = {k.capitalize(): [] for k in keywords.split(',')}
    combinations = {combination.title(): [] for combination in combinations} if combinations else {}

    content = requests.get('https://news.ycombinator.com/item', params={'id': post_id}).text
    soup = BeautifulSoup(content, 'html.parser')

    posts = soup.find_all("tr", class_="athing")
    job_posts = []
    for post in posts:
        if post.find("img", width="0") and post.find('span', class_='c00'):
            job_posts.append(post)

    for job in job_posts:
        for key in keywords:
            if key.lower() in job.get_text().lower():
                keywords[key].append(job)

    print('Total job posts: {}\n\nKeywords:'.format(len(job_posts)))
    for k, v in keywords.items():
        print('{}: {} ({}%)'.format(k, len(v), int(len(v)*100/len(job_posts))))

    if combinations:
        for job in job_posts:
            for combination in combinations:
                combination_keywords = [k.lower() for k in combination.split('-')]
                if len([c_k for c_k in combination_keywords if c_k in job.get_text().lower()]) == 2:
                    combinations[combination].append(job)

        print('\nCombinations:')
        for k, v in combinations.items():
            print('{}: {} ({}%)'.format(k, len(v), int(len(v)*100/len(job_posts))))

if __name__ == '__main__':
    jobs_detector()
