# fooling around w/ a GUI

# need to boot up GTK first
try:
    import pgi
    pgi.install_as_gi()
except ImportError:
    pass
import gi
gi.require_version('Gtk', '3.0')

# ...then "really soon" (before any other twisted reactor imports) get
# the correct reactor

from twisted.internet import gtk3reactor
gtk3reactor.install()

# normal imports follow

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.internet.task import react

from twisted.internet.endpoints import TCP4ClientEndpoint
import txtorcon

from gi.repository import Gtk

def create_win():
    #win = Gtk.Window()
    win = Gtk.Dialog()
    win.connect("delete-event", lambda a, b: reactor.stop())#Gtk.main_quit)
    win.set_border_width(10)
    win.set_default_size(320, 220)

    def got_response(dialog, response_code):
        if response_code == 12:
            print("Cancelling; Tor not launched")
            reactor.stop()
    win.connect("response", got_response)

#    cancel = Gtk.Button.new_with_label("Cancel")

    #vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    vbox = win.get_content_area()
    win.add(vbox)
    win.add_button('Cancel', 12)
    progress = Gtk.ProgressBar()
    progress.set_property('show-text', True)
    progress.set_show_text(True)
    progress.set_text(None)
    label = Gtk.Label("Launching Tor")
    log = Gtk.Label("")

    messages = []
    def progress_updates(prog, tag, msg):
        progress.set_fraction(prog / 100.0)
        if len(messages) == 0 or msg != messages[0]:
            messages.insert(0, msg)
        markup = ''
        for n, msg in enumerate(messages[:6]):
            percent = n / 6.0
            val = '%x' % int(255 * percent)
            markup += '<span foreground="#{0}{0}{0}">{1}</span>\n'.format(val, msg)
        #log.set_text('\n'.join(messages))
        log.set_markup(markup)
    
    vbox.pack_start(label, expand=False, fill=False, padding=5)
    vbox.pack_start(progress, expand=False, fill=False, padding=0)
    vbox.pack_start(log, expand=False, fill=False, padding=0)
    vbox.pack_start(Gtk.Label(), expand=True, fill=True, padding=0)
    return win, progress_updates

@inlineCallbacks
def main(reactor):
    ep = TCP4ClientEndpoint(reactor, "localhost", 9051)
    win, prog = create_win()
    win.show_all()
    tor = yield txtorcon.launch(reactor, progress_updates=prog)
    print("tor launched", tor)
    win.destroy()
    yield Deferred()
react(main)
