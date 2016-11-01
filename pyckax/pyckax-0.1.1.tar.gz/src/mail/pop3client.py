'''
'''
import poplib

class POP3Client:
    # +-------------------------------------------------------------------------
    def __init__(self, **setting):
        self.server = setting['server']
        self.username = setting['username']
        self.password = setting['password']
