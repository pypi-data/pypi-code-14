from setuptools import setup

setup(name='m3s_scraper',
      version='0.2.0',
      description='A tool for exporting M3S data',
      url='https://github.com/themotionmachine/m3s_scrapert',
      author='RTW',
      author_email='ryan_t_w@utexas.edu',
      license='MIT',
      packages=['m3s_scraper','bin'],
      install_requires=['selenium', 'unicodecsv', 'chromedriver-installer'],
      scripts=['bin/start-scrape.py'],
      zip_safe=False)