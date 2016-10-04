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

def draw_area(widget, cr):
    print("ding", widget, cr)
    for x in dir(widget):
        print(x)
    print("ddd", widget.get_size_request())
    print("XXX", dir(widget.get_allocation()))
    w, h = widget.get_allocation().width, widget.get_allocation().height
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(1.0)

    for lng in range(0, 360, 5):
        for lat in range(-160, 160, 5):
            x, y = lng * 2, (lat + 160) * 2
            cr.rectangle(x + 10, y + 10, 6, 6)
            cr.stroke()

def create_win():
    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)

    area = Gtk.DrawingArea()
    area.set_size_request(320, 240)
    area.connect('draw', draw_area)
    win.add(area)
    return win

app = Gtk.Application()
reactor.registerGApplication(app)

@inlineCallbacks
def main(reactor):
    ep = TCP4ClientEndpoint(reactor, "localhost", 9051)
    tor = yield txtorcon.connect(reactor, ep)
    win = create_win()
    win.show_all()
    app.add_window(win)
    yield Deferred()
react(main)
