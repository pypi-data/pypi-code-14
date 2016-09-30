#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Marco'


class DbSignal(object):
    """
    Einer Klasse die einen generischen Signal/Slot Mechanismus implementiert.
    Angelehnt an PyQt Signale und dazu weitgehenst kompatibel.
    """
    def __init__(self):
        self.__slots = []

    def connect(self, slot):
        """
        Verbindet eine Python Funktion als Slot mit dem Signal

        :param slot: Python Funktion
        """
        if not slot in self.__slots:
            self.__slots.append(slot)

    def disconnectAll(self):
        """
        Löst alle vorhanden Verbindungen zu registrierten Slots.
        """
        self.__slots = []

    def emit(self, *args):
        """
        Feuert das Signal ab und benachrichtigt alle verbundenen Slots.
        Es wird im Moment noch kein separater Thread generiert, dadurch
        ist dies eine blockierende Operation.
        Es können auch Parameter mit durchgereicht werden.

        :param args:
        """
        for slot in self.__slots:
            slot(*args)

    def slots(self):
        return self.__slots