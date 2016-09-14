#!/usr/bin/python

import time,readline,thread
import sys,struct,fcntl,termios

def blank_current_readline():
    # Next line said to be reasonably portable for various Unixes
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    # ANSI escape sequences (All VT100 except ESC[0G)
    sys.stdout.write('\x1b[2K')                         # Clear current line
    sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))  # Move cursor up and clear line
    sys.stdout.write('\x1b[0G')                         # Move to start of line


def noisy_thread():
    while True:
        time.sleep(3)
        blank_current_readline()
        print 'Interrupting text!'
        sys.stdout.write('> ' + readline.get_line_buffer())
        sys.stdout.flush()          # Needed or text doesn't show until a key is pressed


if __name__ == '__main__':
    thread.start_new_thread(noisy_thread, ())
    while True:
        s = raw_input('> ')
