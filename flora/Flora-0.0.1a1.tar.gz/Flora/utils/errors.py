class Error(Exception):
    """Your Basic Error"""
    pass

class SelfBot(Error):
    """Raised When Selfbot is not supported"""
    pass

class NotSelfBot(Error):
    """Raised When NonSelfbot is not supported"""
    pass
