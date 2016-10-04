# coding: utf-8
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

from gi.repository import Gtk, Gdk

def draw_area(widget, cr, state):

    w, h = widget.get_allocation().width, widget.get_allocation().height
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(1.0)

    if False:
        for lng in range(0, 360, 5):
            for lat in range(-160, 160, 5):
                x, y = lng * 2, (lat + 160) * 2
                cr.rectangle(x + 10, y + 10, 6, 6)
                cr.stroke()


    cr.set_source_rgb(0, 0, 0)
    cr.select_font_face('Source Code Pro')
    cr.set_font_size(22.0)
    size = cr.font_extents()
    height = size[2]

    y = height
    x = 50
    for circ in state.circuits.values():
        cr.move_to(x, y)
        msg = '{circuit.id}: {path}'.format(
            circuit=circ,
            path='→'.join([r.location.countrycode for r in circ.path]),
        )
        cr.show_text(msg)
        y += height
        x = 50


def create_win(tor):
    win = Gtk.Window()
    win.connect("delete-event", Gtk.main_quit)

    area = Gtk.DrawingArea()
    area.set_size_request(320, 240)
    area.connect('draw', draw_area, tor)
#    win.connect("motion-notify-event", motion)
    win.add(area)
    return win

app = Gtk.Application()
reactor.registerGApplication(app)

@inlineCallbacks
def main(reactor):
    ep = TCP4ClientEndpoint(reactor, "localhost", 9051)
    tor = yield txtorcon.connect(reactor, ep)
    state = yield tor.create_state()

    win = create_win(state)
    win.show_all()
    app.add_window(win)

    def redraw():
        print("redraw")
        win.queue_draw()
        reactor.callLater(1, redraw)
    redraw()

    yield Deferred()
react(main)
