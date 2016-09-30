from setuptools import find_packages, setup

setup(
    name='jira_issue_recommender',
    packages=['jira_issue_recommender'],
    version='0.0.2',
    description='Find related issues',
    author='Quinn Weber',
    author_email='quinn@quinnweber.com',
    maintainer='Quinn Weber',
    maintainer_email='quinn@quinnweber.com',
    url='https://github.com/qsweber/jira-issue-recommender',
    install_requires=(
        'jira',
        'HTMLParser',
        'scikit-learn',
        'scipy'
    ),
    entry_points={
        'console_scripts': (
            'jira-issue-recommender = jira_issue_recommender.main:main'
        )
    }
)
