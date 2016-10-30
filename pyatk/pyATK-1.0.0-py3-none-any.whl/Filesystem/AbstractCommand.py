# -*- coding: utf-8 -*-
from abc import abstractmethod


class AbstractCommand:
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass
