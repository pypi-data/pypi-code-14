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
    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    win.add(vbox)
    progress = Gtk.ProgressBar()
    label = Gtk.Label("no progress yet")
    vbox.pack_start(progress, True, True, 0)
    vbox.pack_start(label, True, True, 0)
    return win

app = Gtk.Application()
reactor.registerGApplication(app)

@inlineCallbacks
def main(reactor):
    ep = TCP4ClientEndpoint(reactor, "localhost", 9051)
    tor = yield txtorcon.connect(reactor, ep)
#    win = create_main(tor)
#    win.show_all()
#    app.add_window(win)
#    yield Deferred()
react(main)
