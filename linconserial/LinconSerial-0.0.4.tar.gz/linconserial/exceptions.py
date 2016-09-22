class LinConError(Exception):
    dflt_msg = "LinCon Error"
    def __init__(self, msg = None):
        new_msg = self.dflt_msg
        if msg:
            new_msg = "%s: %s" %(new_msg, msg)
        Exception.__init__(self, new_msg)
