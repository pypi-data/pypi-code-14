import sys
import traceback

import colorama
from colorama import Fore, Style


# TODO: Allow to enable backtrace by setting an environment variable.


def _flush_message(message):
    """Flush the message to stdout.
    """
    # TODO: Since these are exceptions, it probably makes more sense
    # to print to stderr
    sys.stderr.write(message + '\n')
    sys.stderr.flush()


def _name_module(module):
    """Replace `<module>` at the beginning of the trace with the
    name of the calling file.
    """
    # return module if module != "<module>" else __file__
    return module


def _build_flow(entries):
    flow = []
    for entry in entries:
        flow.append('{0}{1}{2}{3} ({4})\n'.format(
            Fore.GREEN,
            _name_module(entry[2]),
            Fore.WHITE,
            Style.DIM,
            entry[3]))
    directed_flow = ' {0} --> '.format(Fore.YELLOW).join(flow)
    _flush_message(directed_flow)


class Hook(object):
    def __init__(self,
                 entries,
                 align=False,
                 flow_only=False):
        self.entries = entries
        self._align = align

    def reverse(self):
        self.entries = self.entries[::-1]

    def generate_backtrace(self):
        file_formatting = Style.DIM
        line_formatting = Fore.RED + Style.BRIGHT
        context_formatting = Fore.GREEN
        call_formatting = Fore.YELLOW + ' --> '

        self.style_lengths = [
            len(file_formatting),
            len(line_formatting),
            len(context_formatting),
            len(call_formatting)
        ]
        lengths = self._set_alignment() if \
            self._align else [1, 1, 1, 1]

        backtrace_entries = []

        for entry in self.entries:
            file = file_formatting + entry[0]
            line = line_formatting + str(entry[1])
            context = context_formatting + _name_module(entry[2])
            call = call_formatting + entry[3]
            backtrace_entries.append(
                '{0:{1}} {2:{3}} {4:{5}} {6:{7}}'.format(
                    file, lengths[0],
                    line, lengths[1],
                    context, lengths[2],
                    call, lengths[3]))
        return backtrace_entries

    def _set_alignment(self):
        lengths = [0, 0, 0, 0]

        for entry in self.entries:
            for index, field in enumerate(entry):
                lengths[index] = max(
                    lengths[index],
                    len(str(entry[index])) + self.style_lengths[index])
        return lengths


def rehook(reverse=False,
           flow_only=False,
           align=False):

    colorama.init(autoreset=True)

    def new_excepthook(tpe, value, tb):
        traceback_entries = traceback.extract_tb(tb)
        hook = Hook(traceback_entries, align=align)

        main_message = '{0}{1}{2}: {3}'.format(
            Fore.RED,
            Style.BRIGHT,
            tpe.__name__ + ': ',
            str(value))
        if reverse:
            hook.reverse()
        backtrace = hook.generate_backtrace()
        backtrace.insert(0 if reverse else len(backtrace), main_message)
        for entry in backtrace:
            _flush_message(entry)

    sys.excepthook = new_excepthook
