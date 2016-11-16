import logging
import threading

logger = logging.getLogger()

class EnvStatus(object):
    def __init__(self, label=None):
        self.cv = threading.Condition()
        self._env_id = None
        self._env_state = None
        self._metadata = {}
        self._state_id = 0
        self._episode_id = 0
        self.label = label or 'EnvStatus'

    def env_info(self):
        with self.cv:
            return {
                'env_state': self._env_state,
                'metadata': self._metadata,
                'env_id': self._env_id,
                'state_id': self._state_id,
                'episode_id': self._episode_id,
            }

    def set_env_info(self, env_state, metadata={}, env_id=None):
        with self.cv:
            if env_id is None:
                env_id = self.env_id
            if env_state is None:
                env_state = self.env_state
            self.cv.notifyAll()

            # Bump when changing from resetting -> running
            #
            # TODO: this *may* not be robust enough, and may make more
            # sense to be received from the remote in the env describe
            # message.
            if self.env_state == 'resetting' and env_state == 'running':
                self._episode_id += 1

            logger.info('[%s] Setting env_state: %s (env_id=%s) -> %s (env_id=%s) (episode_id=%s)', self.label, self._env_state, self._env_id, env_state, env_id, self._episode_id)
            self._env_state = env_state
            self._metadata = metadata
            self._state_id += 1
            if env_id is not None:
                self._env_id = env_id

    @property
    def state_id(self):
        with self.cv:
            return self._state_id

    @property
    def episode_id(self):
        with self.cv:
            return self._episode_id

    @property
    def env_state(self):
        with self.cv:
            return self._env_state

    @env_state.setter
    def env_state(self, value):
        # TODO: Validate env_state
        self.set_env_info(value)

    @property
    def env_id(self):
        with self.cv:
            return self._env_id

    @env_id.setter
    def env_id(self, value):
        self.set_env_info(None, env_id=value)

    def wait_for_env_state_change(self, start_state):
        with self.cv:
            while True:
                if self._env_state != start_state:
                    return self.env_info()
                self.cv.wait(timeout=10)
