import time
import chalk

class Debug:
    def __init__(self) -> None:
        self._ltag = 7  # Used for cosmetic padding

    def emit(self, message: str, tag: str='\\\\\\/'):
        '''
        Main debugging output function. Colorizes output based on
        a set of predefined tags, and formats the messages appropriately.
        '''
        if tag == 'INFO':
            disp = chalk.blue
        elif tag == 'WARN':
            disp = chalk.yellow
        elif tag == 'ERROR':
            disp = chalk.red
        elif tag == 'BANNER':
            disp = chalk.cyan
            tag = '\\\\\\/'
        else:
            disp = chalk.green

        if len(tag) > self._ltag:
            self._ltag = len(tag) + 2

        tag = '[{}]'.format(tag).rjust(self._ltag)
        msg = '[{}] {} :: {}'.format(time.asctime(), tag, message)
        disp(msg)

    def info(self, message):
        self.emit(message, tag='INFO')

    def warn(self, message):
        self.emit(message, tag='WARN')

    def error(self, message):
        self.emit(message, tag='ERROR')

    def banner(self, message):
        self.emit(message, tag='BANNER')

    def missing_functions(self, sensor, funcs):
        '''
        Convenience function for displaying a list of missing
        functions in a loaded sensor module.
        '''
        mlist = ', '.join(funcs)
        msg = ' * {} missing functions: {}'.format(sensor, mlist)
        self.emit(msg, tag='ERROR')