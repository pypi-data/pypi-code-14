class ParseError (ValueError):
    def __init__(self, tmpl, *args, **kw):
        ValueError.__init__(self, tmpl.format(*args, **kw))
