"""
canat plugin: replicate the html <canat/> tag with message corrections.

Usage of this plugin is not recommended.

Commands
--------

.. glossary::

    /canat
        Send canat with <marquee/> behavior

Configuration
-------------

.. glossary::
    :sorted:

    refresh
        **Default:** ``1``

        Interval between each correction (the closest to 0 is the fastest)

    total_duration
        **Default:** ``30``

        Total duration of the animation.

    padding
        **Default:** ``20``

        Padding to use to move the text.


"""
from plugin import BasePlugin
import tabs
from decorators import command_args_parser

def move(text, step, spacing):
    new_text = text + (" " * spacing)
    return new_text[-(step % len(new_text)):] + new_text[:-(step % len(new_text))]

class Plugin(BasePlugin):
    default_config = {"canat": {"refresh": 1.0, "total_duration": 30, "padding": 20}}

    def init(self):
        self.add_tab_command(tabs.MucTab, 'canat', self.command_canat, 'Replicate the <marquee/> behavior in a message')

    @command_args_parser.raw
    def command_canat(self, args):
        tab = self.api.current_tab()
        msg_id = tab.last_sent_message["id"]
        jid = tab.name
        if not args.strip():
            args = 'CANAT'

        self.api.add_timed_event(self.api.create_delayed_event(self.config.get("refresh"), self.delayed_event, jid, args, msg_id, 0, 0))

    def delayed_event(self, jid, body, msg_id, step, duration):
        if duration >= self.config.get("total_duration"):
            return
        message = self.core.xmpp.make_message(jid)
        message["type"] = "groupchat"
        message["body"] = move(body, step, self.config.get("padding"))
        message["replace"]["id"] = msg_id
        message.send()
        self.api.add_timed_event(self.api.create_delayed_event(self.config.get("refresh"), self.delayed_event, jid, body, message["id"], step + 1, duration + self.config.get("refresh")))


