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


class DilbertFeed(object):
    name = 'dilbert'
    version = '0.1'
    description = ('This feed provider creates an ATOM feed similar to the '
                   'one provided by http://www.dilbert.com, but makes sure '
                   'the comic is included.')
    sample_conf = ('[feed:dilbert]\n'
                   'plugin=dilbert\n'
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
        return {
            'title': soup('span', {'class': 'comic-title-name'})[0].text,
            'content': cgi.escape(str(soup('img', {'class': 'img-comic'})[0]))
        }

    def run(self):
        url = 'http://www.dilbert.com/feed'
        self.logger.info('Using %s as an input feed.' % url)
        self.logger.info('Writing the output feed to %s.' % self.output)

        with open(self.output, 'w+') as f:
            d = feedparser.parse(url)

            # Top
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<feed xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">
    <id>tag:dilbert.com,2005:/feed</id>
    <link rel="alternate" type="text/html" href="http://dilbert.com"/>
    <link rel="self" type="application/atom+xml"
          href="http://dilbert.com/feed"/>
    <title>Dilbert Daily Strip</title>
    <updated>%s</updated>''' % d['feed']['updated'])

            for entry in d['entries']:
                contents = self._get_content(entry['link'])
                f.write('''    <entry>
        <id>%s</id>
        <updated>%s</updated>
        <link rel="alternate" type="text/html" href="%s"/>
        <title>%s</title>
        <content type="html">%s</content>
    </entry>''' % (entry['id'],
                    entry['updated'],
                    entry['link'],
                    contents['title'],
                    contents['content']))

            # Bottom
            f.write('</feed>')
