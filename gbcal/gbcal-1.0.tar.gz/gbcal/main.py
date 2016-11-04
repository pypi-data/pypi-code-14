#!/usr/bin/env python2

from __future__ import print_function
import sys
import os

from gbcal import GBCal

def usage():
    usage="""{app} - google bithday calendar

Usage:

- list birthday:
  {app} name_regex

- add birthday:
  {app} -a name date(DD.MM.YYYY)
""".format(app=os.path.basename(sys.argv[0]))

    print(usage)
    sys.exit(1)

def main():
    find_regex = None
    
    if len(sys.argv) == 1:
        # print all events (without find_regex)
        pass

    elif len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            usage()
        else:
            find_regex = sys.argv[1]

    elif len(sys.argv) == 4 and sys.argv[1] == '-a':
        name=sys.argv[2]
        date=sys.argv[3]

        cal = GBCal(create_if_not_exist=False)
        cal.add_event(name=name, date=date)

        return
    
    else:
        print("Invalid usage. Use -h")
    
    cal = GBCal(create_if_not_exist=False)
    events = cal.get_events(regex=find_regex)

    if not events:
        print('No bithday events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == '__main__':
    main()