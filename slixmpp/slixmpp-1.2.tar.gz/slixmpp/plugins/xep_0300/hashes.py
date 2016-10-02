"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2016 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

from slixmpp import Message, Presence
from slixmpp.xmlstream import register_stanza_plugin
from slixmpp.plugins import BasePlugin
from slixmpp.plugins.xep_0300 import stanza
from slixmpp.plugins.xep_0300.stanza import Headers


class XEP_0300(BasePlugin):

    name = 'xep_0300'
    description = 'XEP-0300: Use of Cryptographic Hash Functions'
    dependencies = set(['xep_0030'])
    stanza = stanza

    def plugin_init(self):
        self.xmpp['xep_0030'].add_feature(Headers.namespace)

    def plugin_end(self):
        self.xmpp['xep_0030'].del_feature(feature=Headers.namespace)
        for header in self.supported_headers:
            self.xmpp['xep_0030'].del_feature(
                    feature='%s#%s' % (Headers.namespace, header))

    def session_bind(self, jid):
        self.xmpp['xep_0030'].add_feature(Headers.namespace)
        for header in self.supported_headers:
            self.xmpp['xep_0030'].add_feature('%s#%s' % (
                Headers.namespace,
                header))
