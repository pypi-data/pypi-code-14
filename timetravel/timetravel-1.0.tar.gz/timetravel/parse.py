"""Calendar parsing."""

import os
import datetime
import re
from . import spec

TODAY = datetime.date.today().strftime("%Y%m%d")

def machine(file, shift=TODAY, event='first', report=False):
    """Creates a new calendar file with shifted dates.

    Args:
        file: str. Calendar file. Supported extensions are ['.ics'].
        shift: str or int. A date to shift to or a number of days to shift.
            - Date: The format must be 'YYYYMMDD'. Based on the event arg,
                    either the first or last event will be shifted to this date
                    and all other events will be shifted by the same relative
                    time.
            - Days: All dates will be shifted by this number of days either
                    forward for a positive int or backward for a negative int.
        event: str, default: 'first'. Reference point for shift calculation.
            Possible values are ['first', 'last'].
        report: bool. Print a summary report.
    """
    days = None
    # check args:
    valid_file = ['.ics']
    valid_event = ['first', 'last']
    fbase, fext = os.path.splitext(file)
    if fext not in valid_file:
        raise LookupError('Invalid file arg; bad extension. See docstring.')
    if isinstance(shift, int):
        days = shift
        dtshift = None
    else:
        dtshift = datetime.datetime.strptime(shift, '%Y%m%d')
    if event not in valid_event:
        raise LookupError('Invalid event arg. See docstring.')

    # read source txt
    with open(os.path.abspath(file)) as f:
        txt = f.read()

    # load calendar spec
    if fext == '.ics':
        cal = spec.icalendar()
    dtstart = cal.dtstart
    dtend = cal.dtend
    evstart = cal.evstart
    evend = cal.evend
    form = cal.form

    # calculate shift
    evidx = event_idx(txt, evstart, evend)
    if not days:
        dts = dates(txt, evidx, dtstart, form)
        if event == 'first':
            dtbase = min(dts)
        elif event == 'last':
            dtbase = max(dts)
        dtdelta = dtshift - dtbase
        days = dtdelta.days

    if report:
        results = [('Events Modified', len(evidx)),
                   ('Days Traveled', days)]
        if dtshift:
            results.append(['Origination', dtbase.strftime(form)])
            results.append(['Destination', dtshift.strftime(form)])
        print_report(results)

    # shift dates
    out = travel(txt, evidx, days, dtstart, dtend, form)

    # write new txt
    outfile = os.path.abspath(fbase + '_' + TODAY + fext)
    with open(outfile, 'w') as f:
        f.write(out)

def travel(txt, evidx, days, dtstart, dtend, form):
    """Shift all events in txt by days."""
    repl_ = lambda match: repl(match, days, form)
    out = txt[:evidx[0][0]]
    for start, end in evidx:
        if start != len(out):
            out += txt[len(out): start - 1]
        event = txt[start:end]
        for pat in [dtstart, dtend]:
            event = re.sub(pat, repl_, event)
        out += event
    out += txt[len(out):]
    return out

def event_idx(txt, evstart, evend):
    """Create a list of indexes for event start/end points in txt."""
    pos = []
    start = txt.find(evstart)
    end = txt.find(evend)
    while end != -1:
        pos.append((start, end + len(evend)))
        start = txt.find(evstart, start + 1)
        end = txt.find(evend, end + 1)
    return pos

def dates(txt, evidx, pat, form):
    """Extract dates from txt."""
    dts = []
    for start, end in evidx:
        match = re.search(pat, txt[start:end])
        s = [g for g in match.groups() if g][0]
        dts.append(datetime.datetime.strptime(s, form))
    return dts

def repl(match, days, form):
    """Shift matched date by days."""
    base = match.group(0)
    s = [g for g in match.groups() if g][0]
    start = base.find(s)
    end = start + len(s)
    dt = datetime.datetime.strptime(s, form)
    new_dt = dt + datetime.timedelta(days=days)
    return base[:start] + new_dt.strftime(form) + base[end:]

def print_report(args):
    """Print args."""
    for item, val in args:
        print(item, ':', val)
