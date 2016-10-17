import logging
import threading
from Queue import Queue

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from python_agent.packages.blinker import signal
from python_agent import config
from python_agent.packages import requests, interval
from python_agent.test_listener.code_coverage import CodeCoverageManager
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import create_environment, get_test_name_from_identifier
from python_agent.test_listener.utils import get_execution_id_from_identifier

log = logging.getLogger(__name__)


class FootprintsManager(object):
    def __init__(self, **kwargs):
        self.footprints_service = FootprintsService()
        self.footprints_queue = FootprintsQueue(maxsize=config.MAX_ITEMS_IN_QUEUE)
        self.code_coverage_manager = CodeCoverageManager(**kwargs)
        self.watchdog = BackgroundScheduler(executors={'processpool': ProcessPoolExecutor(2)})
        self.watchdog.add_job(self.send_all, interval.IntervalTrigger(milliseconds=config.INTERVAL_IN_MILLISECONDS))
        self.watchdog.add_job(self.send_current_partial_footprints,
                              interval.IntervalTrigger(milliseconds=config.INTERVAL_IN_MILLISECONDS))
        self._is_sending_lock = threading.Lock()

    def test_identifier_changing(self, sender, **kwargs):
        old_test_identifier = kwargs.get("old_test_identifier")
        new_test_identifier = kwargs.get("new_test_identifier")
        log.info("Test Identifier Changed. Old: %s. New: %s. Reset Coverage Flag: %s"
                 % (old_test_identifier, new_test_identifier, config.app["is_initial_color"]))
        self.enqueue_footprints(old_test_identifier)

    def send_current_partial_footprints(self):
        current_test_identifier = StateTracker().current_test_identifier
        if current_test_identifier:
            log.info("Enqueuing Current Partial Footprints. Test Identifier: %s" % current_test_identifier)
            self.enqueue_footprints(current_test_identifier)

    def enqueue_footprints(self, test_identifier):
        if not test_identifier:
            log.warning("Test Identifier is Null or Empty. Not Enqueuing Footprints")
            return
        try:
            log.info("Getting Footprints From Code Coverage Manager For Test: %s" % test_identifier)
            footprints = self.code_coverage_manager.get_footprints_from_test(
                get_test_name_from_identifier(test_identifier)
            )
            log.info("Footprints Received From Code Coverage Manager For Test: %s. Number Of Items: %s"
                     % (test_identifier, len(footprints)))
            item = {
                "testName": get_test_name_from_identifier(test_identifier),
                "executionId": get_execution_id_from_identifier(test_identifier),
                "apps": [{
                    "appName": config.app["app_name"],
                    "build": config.app["build"],
                    "branch": config.app["branch"],
                    "footprints": footprints
                }]
            }
            if footprints:
                self.footprints_queue.put(item)
                log.info("Enqueued Footprints Item For Test: %s" % test_identifier)
        except Exception as e:
            log.exception("Failed Enqueuing Footprints. Test: %s. Error: %s" % (test_identifier, str(e)))

    def send_all(self, *args, **kwargs):
        self._is_sending_lock.acquire()
        footprint_items = []
        try:
            while not self.footprints_queue.empty():
                footprint_items.append(self.footprints_queue.get())
            if not footprint_items:
                return
            log.info("Dequeued Footprints From Footprints Queue. Number Of Footprint Items: %s" % len(footprint_items))
            self.footprints_service.send_footprints(footprint_items)
        except Exception as e:
            log.exception("Failed Sending All Footprints. Number Of Footprint Items: %s. Error: %s "
                          % (len(footprint_items), str(e)))
        finally:
            self._is_sending_lock.release()

    def start(self):
        log.info("Starting Footprints Manager")
        try:
            self.watchdog.start()
            log.info("Started Footprints Watchdog")
            test_identifier_signal = signal('test_identifier_changing')
            test_identifier_signal.connect(self.test_identifier_changing)
            footprints_queue_full = signal('footprints_queue_full')
            footprints_queue_full.connect(self.send_all)
            log.info("Started Footprints Manager")
        except Exception as e:
            log.exception("Failed Starting Footprints Manager. Error: %s" % str(e))

    def shutdown(self):
        log.info("Shutting Down Footprints Manager")
        try:
            current_test_identifier = StateTracker().current_test_identifier
            if config.app["is_initial_color"]:
                self.enqueue_footprints(current_test_identifier)
            else:
                execution_id = get_execution_id_from_identifier(current_test_identifier)
                test_identifier = execution_id + "/" + config.INIT_TEST_NAME
                self.enqueue_footprints(test_identifier)

            self.watchdog.shutdown()
            self.send_all()
            self.code_coverage_manager.shutdown()
            log.info("Finished Shutting Down Footprints Manager")
        except Exception as e:
            log.exception("Failed Shutting Down Footprints Manager. Error: %s" % str(e))


class FootprintsService(object):

    def send_footprints(self, footprint_items):
        try:
            log.info("Sending Footprints. Number Of Footprint Items: %s" % len(footprint_items))
            message = {}
            message["customerId"] = config.app["customer_id"]
            message["environment"] = create_environment()
            self.populate_footprints(message, footprint_items)

            url = config.app["server"] + config.FOOTPRINTS_ROUTE

            response = requests.post(url, json=message, timeout=3)
            response.raise_for_status()
            log.info("Sent Footprints to Server. number of footprint items: %s" % len(footprint_items))
        except Exception as e:
            log.exception("Failed Sending Footprints. Number Of Footprint Items: %s. error:%s"
                          % (len(footprint_items), str(e)))

    def populate_footprints(self, message, footprint_items):
        if config.FOOTPRINTS_ROUTE_VERSION == "v2":
            message["items"] = []
            message["methods"] = []
            message["apps"] = [{
                "appName": config.app["app_name"],
                "branchName": None,
                "buildName": None,
                "moduleName": None
            }]
            message["configurationData"] = config.app
            for footprint_item in footprint_items:
                item = {
                    "testName": footprint_item["testName"],
                    "executionId": footprint_item["executionId"],
                    "localTime": None,
                    "apps": []
                }
                for app_idx, footprint_item_app in enumerate(footprint_item["apps"]):
                    app = {
                        "appIdx": app_idx,
                        "footprints": []
                    }
                    for method_idx, method in enumerate(footprint_item_app["footprints"]):
                        message["methods"].append({"name": method["name"], "hash": method["hash"], "appIdx": app_idx})
                        app["footprints"].append([method_idx, method["hits"]])
                    item["apps"].append(app)
                message["items"].append(item)
        else:  # config.FOOTPRINTS_ROUTE_VERSION == "v1"
            message["items"] = footprint_items


class FootprintsQueue(Queue, object):
    def put(self, item, block=True, timeout=None):
        super(FootprintsQueue, self).put(item, block=block, timeout=timeout)
        if self.full():
            footprints_queue_full = signal('footprints_queue_full')
            log.info("Footprints Queue is Full. Signaling...")
            footprints_queue_full.send()
