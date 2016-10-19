# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='intercity-tickets',
    version='0.0.1',
    description='It gets the details of your intercity tickets.',
    author='Adam Bogdał',
    author_email='adam@bogdal.pl',
    url='https://github.com/bogdal/intercity-tickets',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'dj-email-url',
        'emails',
        'python-slugify>=1.2.0',
        'requests',
        'tqdm>=3.4.0',
    ],
    entry_points={
        'console_scripts': [
            'download_tickets = intercity_tickets:download_tickets',
            'send_reminders = intercity_tickets:send_reminders']},
    zip_safe=False)
