#!/usr/bin/env python
# test_vncsession.py - tests for VNCSesssion class

#import cv2
import time
import unittest
from libvncdriver import VNCSession

class TestVNCSession(unittest.TestCase):
    ''' Test the VNCSession class '''

    def test_requires_remotes(self):
        with self.assertRaises(TypeError):
            VNCSession()  # Requires remotes parameter

    def test_members(self):
        remotes = 'localhost:5900'
        error_buffer = object()  # Placeholder
        vncsession = VNCSession(remotes=[remotes], error_buffer=error_buffer)
        self.assertEqual(remotes, vncsession.remotes)
        self.assertIs(error_buffer, vncsession.error_buffer)

    def test_flip(self):
        vncsession = VNCSession(remotes=['localhost:5900'])
        time.sleep(0.2)
        for i in range(10):
            n, updates = vncsession.flip()
            self.assertEqual(n[0].shape[2], 3)  # Color depth should only be 3
            self.assertIn('vnc.updates.n', updates[0])
            time.sleep(0.01)

    def test_event(self):
        vncsession = VNCSession(remotes=['localhost:5900'])
        for i in range(100):
            vncsession.event(('PointerEvent', i, 100-i, 0))
            time.sleep(.01)

    def test_step(self):
        vncsession = VNCSession(remotes=['localhost:5900'], encoding="trle")
        for k in range(13):
            vncsession.step([[('KeyEvent', ord('A')+k, 1), ('KeyEvent', ord('a')+k, 1)]])
            time.sleep(.01)

if __name__ == '__main__':
    unittest.main()
