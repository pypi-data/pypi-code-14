import logging
import threading
from Queue import Queue

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from python_agent.packages.blinker import signal
from python_agent import config
from python_agent.packages import requests, interval
from python_agent.test_listener.utils import create_environment

log = logging.getLogger(__name__)


class EventsManager(object):
    def __init__(self):
        self.events_service = EventsService()
        self.events_queue = EventsQueue(maxsize=config.MAX_ITEMS_IN_QUEUE)
        self.watchdog = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(1)})
        self.watchdog.add_job(self.send_all, interval.IntervalTrigger(milliseconds=config.INTERVAL_IN_MILLISECONDS))
        self._is_sending_lock = threading.Lock()

    def push_event(self, event):
        try:
            if not event:
                return
            self.events_queue.put(event)
            log.info("Pushed Event. Event: %s" % event)
        except Exception as e:
            log.exception("Failed Pushing Event: %s. Error: %s" % (event, str(e)))

    def send_all(self, *args, **kwargs):
        self._is_sending_lock.acquire()
        events = []
        try:
            while not self.events_queue.empty():
                events.append(self.events_queue.get())
            if not events:
                return
            log.info("Dequeued Events From Events Queue. Number Of Events: %s" % len(events))
            self.events_service.send_events(events)
        except Exception as e:
            log.exception("Failed Sending All Events. Number Of Events: %s. Error: %s " % (len(events), str(e)))
        finally:
            self._is_sending_lock.release()

    def start(self):
        log.info("Starting Events Manager")
        try:
            self.watchdog.start()
            log.info("Started Events Watchdog")
            events_queue_full = signal('events_queue_full')
            events_queue_full.connect(self.send_all)
            log.info("Started Events Manager")
        except Exception as e:
            log.exception("Failed Starting Events Manager. error: %s" % str(e))

    def shutdown(self):
        log.info("Shutting Down Events Manager")
        try:
            self.watchdog.shutdown()
            self.send_all()
            log.info("Finished Shutting Down Events Manager")
        except Exception as e:
            log.exception("Failed Shutting Down Events Manager. Error: %s" % str(e))


class EventsService(object):

    def send_events(self, events):
        try:
            log.info("Sending Events. Number Of Events: %s" % len(events))
            message = {}
            message["appName"] = config.app["app_name"]
            message["customerId"] = config.app["customer_id"]
            message["environment"] = create_environment()
            message["events"] = events
            if config.app["branch"]:
                message["branch"] = config.app["branch"]
            if config.app["build"]:
                message["build"] = config.app["build"]

            url = config.app["server"] + config.TEST_EVENTS_ROUTE

            response = requests.post(url, json=message, timeout=3)
            response.raise_for_status()
            log.info("Sent Events to Server. Number Of Events: %s" % len(events))
        except Exception as e:
            log.exception("Failed Sending Events. Number Of Events: %s. error: %s"
                          % (len(events), str(e)))


class EventsQueue(Queue, object):
    def put(self, item, block=True, timeout=None):
        super(EventsQueue, self).put(item, block=block, timeout=timeout)
        if self.full():
            events_queue_full = signal('events_queue_full')
            log.info("Events Queue is Full. Signaling...")
            events_queue_full.send()

