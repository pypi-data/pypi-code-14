from __future__ import print_function
from __future__ import print_function
#!/usr/bin/env python

import sys, os
import time, threading
import glib, gobject
import gst
#pygst.require("0.10")

MAX_BUFFERS = 10

class CLI_Main:
	
    def __init__(self):
        self.player = gst.element_factory_make("playbin2", "player")
                
        audiosink = gst.element_factory_make("autoaudiosink", "audio-output")
        self.decsink = gst.element_factory_make("appsink", "decoded-output")

        self.decsink.set_property("caps", gst.Caps("audio/x-raw-int, width=16, depth=16, signed=true"))
        self.decsink.set_property("drop", False)
        self.decsink.set_property("max-buffers", MAX_BUFFERS)
        self.decsink.set_property("sync", True)
        self.decsink.set_property("emit-signals", True)
        self.decsink.connect("new-buffer", self.add_buffer)
        
        # teebin = gst.Bin("tee-bin")
        # tee = gst.element_factory_make('tee', "tee")
        
        # decsnkq = gst.element_factory_make("queue", "queue-decsnk")
        # audsnkq = gst.element_factory_make("queue", "queue-audsnk")
		
        # mixer = gst.element_factory_make("adder", "mainmixer")
        # teebin.add(mixer)
        # pad = mixer.get_pad("sink0")
        # ghostpad = gst.GhostPad("sink", pad)
        # teebin.add_pad(ghostpad)
		
        # teebin.add(tee, audsnkq, decsnkq, audiosink, self.decsink)
        # mixer.link(tee)
        # tee.link(decsnkq)
        # tee.link(audsnkq)
        # decsnkq.link(self.decsink)
        # audsnkq.link(audiosink)
        
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        self.player.set_property("audio-sink", self.decsink)
        
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.playmode = False
            
    def start(self):
        for filepath in sys.argv[1:]:
            if os.path.isfile(filepath):
                self.playmode = True
                self.player.set_property("uri", "file://" + filepath)
                self.player.set_state(gst.STATE_PLAYING)
                while self.playmode:
                    time.sleep(1)
                    
        time.sleep(1)
        loop.quit()

    def add_buffer(self, sink):
        buf = sink.emit('pull-buffer')
        print("audio buf %d bytes" % len(str(buf)))

mainclass = CLI_Main()
## thread.start_new_thread(mainclass.start, ())
## gobject.threads_init()
## loop = glib.MainLoop()
## loop.run()
mainclass.start()

