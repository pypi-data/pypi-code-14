# Copyright (c) 2016, Cyril Roelandt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import cgi

from bs4 import BeautifulSoup
import feedparser
import requests


class CyanideAndHappinessFeed(object):
    name = 'cyanideandhappiness'
    version = '0.1'
    description = ('This feed provider creates an ATOM feed similar to the '
                   'one provided by http://explosm.net, but makes sure the '
                   'comic is included.')
    sample_conf = ('[feed:cah]\n'
                   'plugin=cyanideandhappiness\n'
                   'output=/path/to/output.xml\n')

    def __init__(self, conf_section, logger):
        self.logger = logger
        try:
            self.output = conf_section['output']
        except:
            self.logger.error('You MUST specify an output file.')
            raise

    def _get_content(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            return 'Failed to get content from %s' % url

        soup = BeautifulSoup(r.text, 'lxml')
        img = str(soup('img', {'id': 'main-comic'})[0])
        img = img.replace('src="', 'src="http:')
        return cgi.escape(img)

    def run(self):
        url = 'http://www.explosm.net/rss.php'
        self.logger.info('Using %s as an input feed.' % url)
        self.logger.info('Writing the output feed to %s.' % self.output)
        with open(self.output, 'w+') as f:
            d = feedparser.parse(url)

            # Top
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Explosm.net</title>
    <link>http://www.explosm.net/rss.php</link>
    <description>Flash Animations, Daily Comics and more!</description>
''')
            # Entries
            for entry in d['entries']:
                f.write('''    <item>
      <title>%s</title>
      <link>%s</link>
      <description>%s</description>
      <category>Comics</category>
      <guid>%s</guid>
      <pubDate>%s</pubDate>
    </item>''' % (entry['title'],
                  entry['link'],
                  self._get_content(entry['link']),
                  entry['id'],
                  entry['published']))
            # Bottom
            f.write('''
  </channel>
</rss>''')
