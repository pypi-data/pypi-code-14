#! /usr/bin/env python
# -*- coding:utf-8 -*-

import logging


class FunctionHandler(logging.Handler):
    
    def __init__(self,level=logging.NOTSET,handle_func=None,fail_silently=False):
        logging.Handler.__init__(self,level)
        self.handle_func=handle_func
        self.fail_silently=fail_silently

    def emit(self, record):
        """Inserting new logging record to mongo database."""
        if self.handle_func is not None:
            try:
                self.handle_func(record)
            except Exception:
                if not self.fail_silently:
                    self.handleError(record)