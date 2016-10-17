import sys
import logging
import time
import traceback

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from python_agent import config
from python_agent.packages import interval, requests
from python_agent.test_listener.utils import create_environment


class SealightsHTTPHandler(logging.Handler):
    def __init__(self, capacity):
        logging.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = []
        self.environment = create_environment()
        self.watchdog = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(1)})
        self.watchdog.add_job(self.flush, interval.IntervalTrigger(milliseconds=config.INTERVAL_IN_MILLISECONDS))
        self.watchdog.start()

    def build_request(self, records):
        return {
            "customerId": config.app["customer_id"],
            "appName": config.app["app_name"],
            "branch": config.app["branch"],
            "build": config.app["build"],
            "creationTime": int(round(time.time() * 1000)),
            "environment": self.environment,
            "log": "\n".join(map(lambda record: self.format(record), records))
        }

    def should_flush(self, record):
        """
        Should the handler flush its buffer?

        Returns true if the buffer is up to capacity. This method can be
        overridden to implement custom flushing strategies.
        """
        return len(self.buffer) >= self.capacity

    def flush(self):
        """
        Override to implement custom flushing behaviour.

        This version just zaps the buffer to empty.
        """
        self.acquire()
        try:
            data = self.build_request(self.buffer)
            response = requests.post(
                "%s%s" % (config.app["server"], config.LOG_SUBMISSION_ROUTE),
                json=data,
                headers={'content-type': 'application/json'},
                timeout=3
            )
            response.raise_for_status()
        except:
            self.handle_exception()
        finally:
            self.buffer = []
            self.release()

    def emit(self, record):
        try:
            self.buffer.append(record)
        except:
            self.handleError(record)

    def close(self):
        try:
            self.flush()
            self.watchdog.shutdown()
        except:
            self.handle_exception()
        finally:
            logging.Handler.close(self)

    def handle_exception(self):
        if logging.raiseExceptions and sys.stderr:  # see issue 13807
            ei = sys.exc_info()
            try:
                traceback.print_exception(ei[0], ei[1], ei[2], None, sys.stderr)
                sys.stderr.write('Failed Sending Logs to Server')
            except IOError:
                pass
            finally:
                del ei