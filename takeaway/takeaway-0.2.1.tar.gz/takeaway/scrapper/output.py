from .error import ScrapperError

from queue import Empty

import logging
import threading


class OutputThread(threading.Thread):
    """
    Thread to output statements from scrapper thread (Start only one !)
    """

    def __init__(self, queue, output, interface, length):
        super(OutputThread, self).__init__()
        logging.info("Init of Output thread")
        self.queue = queue
        self.output = output
        self.interface = interface
        self.length = length

    def run(self):
        bar = self.interface.progress_bar(length=self.length)
        current = 0
        while True:
            try:
                download_completed, name = self.queue.get(timeout=20)
                # If nothing to print after 10 seconds exit the thread
                current += 1
            except Empty:
                break
            if type(download_completed) is ScrapperError:  # Print custom_error if output is custom_error
                self.interface.print("\nError while downloading {}.".format(name))
                self.interface.update_progress_bar(bar, current)
                pass
            elif download_completed is True:  # Print successful
                self.interface.update_progress_bar(bar, current)
            self.queue.task_done()
            if current == self.length:
                self.interface.end_progress_bar(bar)

        logging.debug("Enf of Output thread")
