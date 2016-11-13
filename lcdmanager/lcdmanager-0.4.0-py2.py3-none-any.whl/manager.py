#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
LCD Manager

Allows to use widgets on CharLCD

Usage:
    lcd = CharLCD(20, 4, gp.Gpio())
    lcd.init()
    lcd_manager = Manager(lcd)
    label1 = Label(0, 0)
    label1.label = "This"
    lcd_manager.add_widget(label1)

    #merge buffer and prepare content
    lcd_manager.render()
    #display content
    lcd_manager.flush()
"""
from builtins import object  # pylint: disable=I0011,W0622
import charlcd.abstract.lcd as lcd_abstract
import time

TRANSPARENCY = ' '


class Manager(object):
    """Class Manager"""
    def __init__(self, lcd):
        if lcd.display_mode != lcd_abstract.DISPLAY_MODE_BUFFERED:
            raise AttributeError("lcd must be instance of buffered lcd")

        self.lcd = lcd
        self.widgets = []
        self.name_widget = {}
        self.size = {
            'width': self.lcd.get_width(),
            'height': self.lcd.get_height()
        }
        self.options = {
            'refresh_after': 60 * 5,  # 5 minutes
            'last_refresh': time.time()
        }

    def flush(self):
        """display content"""
        self._time_to_refresh()
        try:
            if not self.lcd.initialized:
                self.lcd.init()
            self.lcd.flush()
        except IOError:
            self.lcd.initialized = False

    def render(self):
        """add widget view to lcd buffer"""
        for widget in self.widgets:
            if not widget.visibility:
                continue
            position = widget.position
            y_offset = 0
            for line in widget.render():
                if position['y'] + y_offset >= self.lcd.get_height():
                    break
                self.lcd.write(
                    line,
                    position['x'],
                    position['y'] + y_offset
                )
                y_offset += 1

    def add_widget(self, widget):
        """add widget to manager"""
        self.widgets.append(widget)
        if widget.name is not None:
            self.name_widget[widget.name] = len(self.widgets) - 1

    def get_widget(self, name):
        """get widget from  manager or None"""
        if name in self.name_widget:
            return self.widgets[self.name_widget[name]]

        return None

    @property
    def width(self):
        """manager width"""
        return self.size['width']

    @property
    def height(self):
        """manager height"""
        return self.size['height']

    def _time_to_refresh(self):
        """force lcd reinitializtion after required time"""
        if self.options['last_refresh'] + self.options['refresh_after'] < time.time():
            self.options['last_refresh'] = time.time()
            self.lcd.initialized = False