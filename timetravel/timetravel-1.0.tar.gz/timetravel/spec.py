"""Calendar specifications."""

def g(*args):
    """REGEX: build group."""
    txt = ''
    for arg in args:
        if txt == '':
            txt = arg
        else:
            txt += '|' + arg
    return '(' + txt + ')'

def ncg(*args):
    """REGEX: build non-capturing group."""
    return '(?:' + g(*args)[1:]

def rep01(s):
    """REGEX: build repeat 0 or 1."""
    return s + '?'

def rep0(s):
    """REGEX: build repeat 0 or more."""
    return s + '*'

def rep1(s):
    """REGEX: build repeat 1 or more."""
    return s + '+'

def rncg(s, rep=rep01):
    """REGEX: build repeate non-capturing group."""
    return rep(ncg(s))

class icalendar(object):
    """Sub-strings and REGEX patterns for iCalendar spec.

        src: https://www.ietf.org/rfc/rfc2445.txt
    """
    def __init__(self):
        """iCalendar init."""
        tzidparam = 'TZID=\/?.+?'
        xparam = '.+?=.+?[,.+?]*?'
        dtstparamcomp = [rncg(';VALUE=' + ncg('DATE-TIME', 'DATE')),
                         rncg(';' + tzidparam),
                         rncg(';' + xparam, rep0)]
        dtstparam = ''.join(dtstparamcomp)
        date = r'(\d{8})'
        time = r'\d{6}Z?'
        date_time = date + 'T' + time
        dtstval = ncg(date_time, date)
        self.dtstart = 'DTSTART' + dtstparam + ":" + dtstval + r'\r\n'
        self.dtend = 'DTEND' + dtstparam + ":" + dtstval + r'\r\n'

        self.evstart = 'BEGIN:VEVENT\r\n'
        self.evend = 'END:VEVENT\r\n'
        self.form = "%Y%m%d"
