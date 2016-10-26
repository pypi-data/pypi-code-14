import logging
import uuid
import atexit

from python_agent import config
from python_agent.test_listener.events import EventsManager
from python_agent.test_listener.footprints import FootprintsManager
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import Singleton


log = logging.getLogger(__name__)


class AgentManager(object):
    __metaclass__ = Singleton

    def __init__(self, **kwargs):
        log.info("Initializing...")
        self.state_tracker = StateTracker()
        self.footprints_manager = FootprintsManager(**kwargs)
        self.events_manager = EventsManager()
        if not config.app["test_phase"]:
            self.footprints_manager.start()
            self.events_manager.start()
        atexit.register(self.shutdown)

    def create_execution_id(self):
        return str(uuid.uuid4())

    def push_event(self, event):
        self.events_manager.push_event(event)

    def send_all(self):
        self.events_manager.send_all()
        self.footprints_manager.send_all()

    def shutdown(self):
        if not config.app["test_phase"]:
            self.events_manager.shutdown()
            self.footprints_manager.shutdown()

