# -*- coding: utf-8 -*-


class DQError(ValueError):

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
