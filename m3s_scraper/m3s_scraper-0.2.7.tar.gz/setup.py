from setuptools import setup

setup(name='m3s_scraper',
      version='0.2.7',
      description='A tool for exporting M3S data',
      url='https://github.com/themotionmachine/m3s_scrapert',
      author='RTW',
      author_email='ryan_t_w@utexas.edu',
      license='MIT',
      packages=['m3s_scraper','bin'],
      install_requires=['selenium', 'unicodecsv',],
      scripts=['bin/start-scrape'],
      zip_safe=False)

#'chromedriver-installer'