import logging
import numpy as np
from gym_vnc import pyprofile
import threading
import time

from gym_vnc import error
from gym_vnc.twisty import reactor
from gym_vnc.vncdriver import server_messages

logger = logging.getLogger(__name__)

class NumpyScreen(object):
    def __init__(self, width, height):
        self.lock = threading.Lock()

        shape = (height, width, 3)
        self._screens = (np.zeros(shape, dtype=np.uint8), np.zeros(shape, dtype=np.uint8))

        self.color_cycle = [0, 1, 2]
        self._width = None
        self._height = None

        self._defer = []
        self._back_updated = True

    def peek(self):
        front_screen, _ = self._screens
        return front_screen

    def flip(self):
        pyprofile.push('vncdriver.numpy_screen.flip_bitmap')
        with self.lock:
            if self._back_updated:
                updates = self._defer

                # Flip screens
                front_screen, back_screen = self._screens
                self._screens = back_screen, front_screen

                # Apply any pending updates
                self._back_updated = False
                reactor.callFromThread(self.update_back)
            else:
                updates = []
            result = self.peek(), {'vnc_session.framebuffer_updates': updates}
        pyprofile.pop()
        return result

    def apply(self, framebuffer_update):
        with self.lock:
            # Pop any pending updates
            self._update_back()
            self._apply(framebuffer_update)
            self._defer.append(framebuffer_update)

    def _apply(self, framebuffer_update):
        for rect in framebuffer_update.rectangles:
            if isinstance(rect.encoding,
                          (server_messages.RAWEncoding, server_messages.ZRLEEncoding, server_messages.ZlibEncoding)):
                self._update_rectangle(rect.x, rect.y, rect.width, rect.height, rect.encoding.data)
            else:
                raise error.Error('Unrecognized encoding: {}'.format(rect.encoding))

    def update_back(self):
        with self.lock:
            self._update_back()

    def _update_back(self):
        if self._back_updated:
            return
        self._back_updated = True

        for framebuffer_update in self._defer:
            self._apply(framebuffer_update)
        self._defer = []

    def _update_rectangle(self, x, y, width, height, data):
        _, back_screen = self._screens
        back_screen[y:y+height, x:x+width, self.color_cycle] = data





    # def _copy_rectangle(self, screen, src_x, src_y, x, y, width, height):
    #     update = np.frombuffer(data, dtype=np.uint8)
    #     update = update.reshape([height, width, 4])
    #     update = update[:, :, self._color_cycle]  # Ignore X channel


    #     screen[y:y+height, x:x+width] = screen[src_y:src_y+height, src_x:src_x+width]

    # def _fill_rectangle(self, screen, x, y, width, height, color):
    #     update = np.frombuffer(color, dtype=np.uint8)
    #     update = update[self._color_cycle]
    #     screen[y:y+height, x:x+width] = update

    # def begin(self, number_of_rectangles):
    #     self.lock.acquire()
    #     # This may already have been called via
    #     # reactor.callFromThread. It's safe to be called multiple times.
    #     self._update_back()

    # def commit(self):
    #     self.lock.release()

    # def back_bitmap(self):
    #     _, back_screen = self._screens
    #     return back_screen

    # def screen_synced(self):
    #     # TODO: lock?
    #     return self._screens is not None
