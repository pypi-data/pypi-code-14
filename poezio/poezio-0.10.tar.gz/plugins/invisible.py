"""
This plugin lets you manage your invisibility as defined in
XEP-0186_.

Commands
--------

.. glossary::

    /invisible
        **Usage:** ``/invisible``

        Set CSI state to ``active``.

    /visible
        **Usage:** ``/csi_inactive``

        Set CSI state to ``inactive``.

.. _XEP-0186: https://xmpp.org/extensions/xep-0186.html
"""

from plugin import BasePlugin
import tabs

class Plugin(BasePlugin):
    def init(self):
        self.api.add_command('invisible', self.command_invisible,
                             help='Become invisible (xep-0186)',
                             short='Become invisible')
        self.api.add_command('visible', self.command_visible,
                             help='Become visible (xep-0186)',
                             short='Become visible')

    def command_active(self, args):
        if not self.core.xmpp.plugin['xep_0352'].enabled:
            self.api.information('CSI is not enabled in this server', 'Warning')
        else:
            self.core.xmpp.plugin['xep_0352'].send_active()

    def command_inactive(self, args):
        if not self.core.xmpp.plugin['xep_0352'].enabled:
            self.api.information('CSI is not enabled in this server', 'Warning')
        else:
            self.core.xmpp.plugin['xep_0352'].send_inactive()
