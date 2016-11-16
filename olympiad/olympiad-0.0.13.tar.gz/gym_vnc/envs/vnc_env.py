import logging
import os
import six.moves.urllib.parse as urlparse

from gym_vnc import error, remotes as remotes_module, rewarder, spaces, twisty, utils, vectorized, vncdriver
from gym_vnc import pyprofile
from gym_vnc.envs import diagnostics
from gym_vnc.remotes import healthcheck
from gym_vnc.runtimes import registration
from gym_vnc.vncdriver import libvnc_session

logger = logging.getLogger(__name__)

if os.environ.get('GYM_VNCDRIVER', None) == 'go':
    # VNC Driver session setup can happen much later, handle the import now
    import go_vncdriver

def go_vncdriver():
    import go_vncdriver
    go_vncdriver.setup()
    return go_vncdriver.VNCSession

def py_vncdriver():
    return vncdriver.VNCSession

def libvnc_vncdriver():
    return libvnc_session.LibVNCSession

def vnc_session(which=None):
    if which is None:
        which = os.environ.get('GYM_VNCDRIVER')

    if which == 'go':
        logger.info('Using the golang VNC implementation')
        return go_vncdriver()
    elif which == 'py':
        logger.info('Using the Python VNC implementation')
        return py_vncdriver()
    elif which == 'libvnc':
        logger.info('Using the libvnc VNC implementation')
        return libvnc_vncdriver()
    elif which is None:
        try:
            go = go_vncdriver()
            logger.info('Using golang VNC implementation')
            return go
        except ImportError as e:
            logger.info("Go driver failed to import:{}".format(e))
            logger.info("Using pure Python vncdriver implementation. Run 'pip install go-vncdriver' to install the more performant Go implementation. Optionally set the environment variable GYM_VNCDRIVER='go' to force its use.")
            return py_vncdriver()
    else:
        raise error.Error('Invalid VNCSession driver: {}'.format(which))

class VNCMultiplexer(object):
    """VNCMultiplexer is responsible for managing the backend connections
    to the VNC environments. If a particular environment fails, we may
    need to connect to a new one in its place.
    """

    def __init__(self, vnc_session_factory):
        self.vnc_session_factory = vnc_session_factory

def parse_remotes(remotes):
    # Parse a list of remotes of the form:
    #
    # address:vnc_port+rewarder_port (e.g. localhost:5900+15900)
    #
    # either vnc_port or rewarder_port can be omitted, but not both

    all_vnc = None
    all_rewarder = None

    vnc_addresses = []
    rewarder_addresses = []

    for remote in remotes:
        # Parse off +, then :
        if '+' in remote:
            if all_vnc == False:
                raise error.Error('Either all or no remotes must have rewarders: {}'.format(remotes))
            all_vnc = True

            remote, rewarder_port = remote.split('+')
            rewarder_port = int(rewarder_port)
        else:
            if all_vnc == True:
                raise error.Error('Either all or no remotes must have rewarders: {}'.format(remotes))
            all_vnc = False

            rewarder_port = None

        if ':' in remote:
            if all_rewarder == False:
                raise error.Error('Either all or no remotes must have a VNC port: {}'.format(remotes))
            all_rewarder = True

            remote, vnc_port = remote.split(':')
            vnc_port = int(vnc_port)
        else:
            if all_rewarder == True:
                raise error.Error('Either all or no remotes must have a VNC port: {}'.format(remotes))
            all_rewarder = False

            vnc_port = None
            all_rewarder = False

        host = remote

        if rewarder_port is not None:
            rewarder_address = '{}:{}'.format(host, rewarder_port)
            rewarder_addresses.append(rewarder_address)

        if vnc_port is not None:
            vnc_address = '{}:{}'.format(host, vnc_port)
            vnc_addresses.append(vnc_address)

    if not all_vnc and not all_rewarder:
        raise error.Error('You must provide either rewarder or a VNC port: {}'.format(remotes))

    if not vnc_addresses:
        vnc_addresses = None
    if not rewarder_addresses:
        rewarder_addresses = None
    return vnc_addresses, rewarder_addresses

class VNCEnv(vectorized.Env):
    metadata = {
        'render.modes': ['human'], # we wrap with a RenderGuard which can render to rgb_array
        'configure.required': True,
        'semantics.async': True,
        'semantics.autoreset': True,
        'video.frames_per_second' : 60,
        'runtime.vectorized': True,
    }

    def __init__(self):
        self._started = False

        self.observation_space = spaces.VNCObservationSpace()
        self.action_space = spaces.VNCActionSpace()

        self._seed_value = None
        self._remotes_manager = None
        self._use_multiple_senses = True

        self._probe_key = 0xbeef1

        self.vnc_session = None
        self.rewarder_session = None

    def _seed(self, seed):
        self._seed_value = seed
        return [seed]

    def _configure(self, remotes=None, start_timeout=None, reuse=True, docker_image=None,
                   ignore_clock_skew=False, disable_action_probes=False,
                   use_multiple_senses=False, vnc_kwargs={}, vnc_driver=None):
        '''
        remotes - Remotes to connect to, given as a comma-separated list of
                  host:vnc_port[+rewarder_port] e.g.:
                  "vnc://127.0.0.1:5900+15900,127.0.0.1:5901+15901" or "vnc://127.0.0.1:5900"

                  If None, remotes is read from GYM_VNC_REMOTES environment variable.

        ignore_clock_skew - Assume remotes are on the same machine as us,
                            for the purposes of diagnostics measurement.

                            If true, we skip measuring the clock skew over the network,
                            and skip generating diagnostics which rely on it.

                            True when used by the rewarder to measure latency between
                            the VNC frame and its calculation of reward for that frame.
                            In this case we share a common clock with the env generating the
                            VNC frame, so we don't need to send/receive probes.
                            Clock skew is zero in this case.

                            False when remotes are potentially different machines
                            (such as an agent, or a demonstrator),
                            and we will be sending probe keys and measuring network ping
                            rountrip times to calculate clock skew.

        use_multiple_senses - Generates observation in dictionary.
        '''
        self._use_multiple_senses = use_multiple_senses

        if self._started:
            raise error.Error('{} has already been started; cannot change configuration now.'.format(self))

        twisty.start_once()

        if self.spec is not None:
            runtime = registration.runtime_spec(self.spec.tags['runtime'])
            # Let the user manually set the docker_image version
            if docker_image:
                # TODO: don't support this option?
                runtime.image = docker_image

        if isinstance(remotes, int):
            if self.spec is None:
                raise error.Error('Must make() environment to spin up a new Docker image')

            self._remotes_manager = remotes_module.Docker(runtime=runtime, n=remotes, reuse=reuse)
            self._remotes_manager.start()
            remotes = self._remotes_manager.connection_strings()
        elif remotes is None:
            remotes = os.environ.get('GYM_VNC_REMOTES')
            if remotes is None:
                raise error.Error("""No remotes provided.

(HINT: you can also set GYM_VNC_REMOTES to a comma separated list of VNC/rewarder pairs to connect to.

For example, you can run: export GYM_VNC_REMOTES=vnc://127.0.0.1:5900+15900,127.0.0.1:5901+15901.)""")

        if isinstance(remotes, str):
            assert "://" in remotes, ("Remote must start with vnc:// or "
                                      "https://")
            parsed = urlparse.urlparse(remotes)
            if parsed.scheme == 'vnc':
                # User spun up some static envs
                remotes = parsed.netloc.split(',')
            elif parsed.scheme == 'http' or parsed.scheme == 'https':
                # We're going to connect to an allocator

                # TODO: better join method
                base_url = parsed.scheme + '://' + parsed.netloc
                if parsed.path:
                    base_url += '/' + parsed.path
                query = urlparse.parse_qs(parsed.query)
                n = query.get('n', [1])[0]
                n = int(n)

                address = query.get('address', [None])[0]
                self._remotes_manager = remotes_module.Allocator(runtime, n=n, address=address, base_url=base_url)

                start_timeout = query.get('start_timeout', [20 * 60])[0]
                start_timeout = int(start_timeout)
                remotes = self._remotes_manager.start()

        vnc_addresses, rewarder_addresses = parse_remotes(remotes)

        self.n = len(remotes)
        logger.info('Connecting to initial remotes: vnc_addresses=%s rewarder_addresses=%s', vnc_addresses, rewarder_addresses)

        if start_timeout is None:
            # Pick a reasonable timeout for all envs to be connectable
            start_timeout = 2 * self.n + 5

        self.connection_names = [str(i) for i in range(self.n)]
        self.crashed = {}

        if vnc_addresses is not None:
            cls = vnc_session(vnc_driver)
            vnc_kwargs.setdefault('start_timeout', start_timeout)
            logger.info('Running with VNCSession arguments: %s', vnc_kwargs)
            self.vnc_kwargs = vnc_kwargs
            self.vnc_session = cls()
        else:
            self.vnc_session = None

        if rewarder_addresses is not None:
            self.rewarder_session = rewarder.RewarderSession(start_timeout)
        else:
            self.rewarder_session = None

        if ignore_clock_skew:
            logger.info('Printed stats will ignore clock skew. (This usually makes sense only when the environment and agent are on the same machine.)')

        if self.rewarder_session or ignore_clock_skew:
            # Don't need rewarder session if we're ignoring clock skew
            if self.spec is not None:
                metadata_encoding = self.spec.tags.get('metadata_encoding')
            else:
                metadata_encoding = None
            self.diagnostics = diagnostics.Diagnostics(self.n, self._probe_key, ignore_clock_skew, metadata_encoding=metadata_encoding, use_multiple_senses=use_multiple_senses, disable_action_probes=disable_action_probes)
        else:
            self.diagnostics = None

        for i in range(self.n):
            vnc_address = rewarder_address = None
            if vnc_addresses is not None:
                vnc_address = vnc_addresses[i]
            if rewarder_addresses is not None:
                rewarder_address = rewarder_addresses[i]
            self.connect(i, vnc_address, rewarder_address)

        self._reset_mask()

    def connect(self, i, vnc_address, rewarder_address):
        name = self.connection_names[i]
        if self.vnc_session is not None:
            self.vnc_session.connect(name=name, address=vnc_address, **self.vnc_kwargs)

        if self.rewarder_session is not None:
            if self.spec is not None:
                env_id = self.spec.id
            else:
                env_id = None

            if self._seed_value is not None:
                # Once we use a seed, we clear it so we never
                # accidentally reuse the seed. Seeds are an advanced
                # feature and aren't supported by most envs in any
                # case.
                seed = self._seed_value[i]
                self._seed_value[i] = None
            else:
                seed = None

            network = self.rewarder_session.connect(
                name=name, address=rewarder_address,
                seed=seed, env_id=env_id,
                fps=self.metadata['video.frames_per_second'])
        else:
            network = None

        if self.diagnostics is not None:
            self.diagnostics.connect(i, network)
        self.crashed.pop(i, None)

    def _close(self, i=None):
        if i is not None:
            name = self.connection_names[i]
            if self.rewarder_session:
                self.rewarder_session.close(name)
            if self.vnc_session:
                self.vnc_session.close(name)
            if self.diagnostics:
                self.diagnostics.close(i)
            self.mask.close(i)
        else:
            if hasattr(self, 'rewarder_session') and self.rewarder_session:
                self.rewarder_session.close()
            if hasattr(self, 'vnc_session') and self.vnc_session:
                self.vnc_session.close()
            if hasattr(self, 'diagnostics') and self.diagnostics:
                self.diagnostics.close()
            if hasattr(self, 'remotes_manager') and self._remotes_manager:
                self._remotes_manager.close()

    def _reset(self):
        if self.rewarder_session:
            self.rewarder_session.reset()
        self._reset_mask()
        return [None] * self.n

    def _reset_mask(self):
        self.mask = Mask(self.n, initially_masked=bool(self.rewarder_session))

    def _pop_rewarder_session(self):
        with pyprofile.push('vnc_env.VNCEnv.rewarder_session.pop'):
            reward_d, done_d, info_d, err_d = self.rewarder_session.pop()

        reward_n = []
        done_n = []
        info_n = []
        err_n = []
        for name in self.connection_names:
            reward_n.append(reward_d.get(name))
            done_n.append(done_d.get(name))
            info_n.append(info_d.get(name, {}))
            err_n.append(err_d.get(name))
        return reward_n, done_n, info_n, err_n

    def _step_vnc_session(self, compiled_n):
        with pyprofile.push('vnc_env.VNCEnv.vnc_session.step'):
            observation_d, info_d, err_d = self.vnc_session.step(compiled_n)

        observation_n = []
        info_n = []
        err_n = []
        for name in self.connection_names:
            observation_n.append(observation_d.get(name))
            info_n.append(info_d.get(name))
            err_n.append(err_d.get(name))
        return observation_n, info_n, err_n

    def _compile_actions(self, action_n):
        try:
            return [[event.compile() for event in action] for action in action_n]
        except Exception as e:
            raise error.Error('Could not compile actions. Original error: {} ({}). action_n={}', e, type(e), action_n)

    def _action_d(self, action_n):
        action_d = {}
        for i, action in enumerate(action_n):
            action_d[self.connection_names[i]] = action
        return action_d

    def _step(self, action_n):
        # We pop from the rewarder session first since we need to
        # determine if any of the current VNC actions need to be
        # masked. (If the environment is resetting, we should
        # definitely not send it any actions.)
        #
        # It's a bit counterintuitive to check for rewards first,
        # since we haven't submitted the actions yet, but keep in mind
        # that everything here is asynchronous!
        if self.rewarder_session:
            reward_n, done_n, info_n, err_n = self._pop_rewarder_session()
        else:
            reward_n = done_n = [None] * self.n
            info_n = [{} for _ in range(self.n)]
            err_n = [None] * self.n

        observation_mask, action_mask = self.mask.maintain_mask(done_n, info_n)

        # Drop any actions to resetting environments.
        #
        # We pass the mask to add_probe so it doesn't try to schedule
        # probes which will just time out anyway.
        self.mask.apply_to_actions(action_n, info_n, action_mask)
        # Send our actions and return the current framebuffer
        if self.vnc_session:
            # Compile actions to something more palatable by drivers
            # written in other language.
            action_n = self._compile_actions(action_n)
            if self.diagnostics:
                self.diagnostics.clear_probes_when_done(done_n)
                self.diagnostics.add_probe(action_n, action_mask)
            action_d = self._action_d(action_n)

            visual_observation_n, obs_info_n, vnc_err_n = self._step_vnc_session(action_d)
            # Merge in any keys from the observation
            self._propagate_obs_info(info_n, obs_info_n)
        else:
            visual_observation_n = [None] * self.n
            vnc_err_n = [None] * self.n

        self.mask.apply_to_return(visual_observation_n, reward_n, done_n, info_n, observation_mask)

        text_n = [info.pop('env.text', []) for info in info_n]
        if self._use_multiple_senses:
            observation_n = [{
                'vision': obs,
                'text': text,
            } for (obs, text) in zip(visual_observation_n, text_n)]
        else:
            observation_n = visual_observation_n

        self._handle_initial_n(observation_n, reward_n)
        self._handle_err_n(err_n, vnc_err_n, info_n, observation_n, reward_n, done_n)
        self._handle_crashed_n(info_n)
        return observation_n, reward_n, done_n, {'n': info_n}

    def _handle_initial_n(self, observation_n, reward_n):
        if self.rewarder_session is None:
            return

        for i, reward in enumerate(reward_n):
            if reward is None:
                # Index hasn't come up yet, so ensure the observation
                # is blanked out.
                observation_n[i] = None

    def _handle_err_n(self, err_n, vnc_err_n, info_n, observation_n=None, reward_n=None, done_n=None):
        # Propogate any errors upwards.
        for i, (err, vnc_err) in enumerate(zip(err_n, vnc_err_n)):
            if err is None and vnc_err is None:
                # All's well at this index.
                continue

            if observation_n is not None:
                observation_n[i] = None
                done_n[i] = True

            # Propagate the error
            if err is not None and vnc_err is not None:
                # Both the rewarder and vnc failed at the same
                # time. What are the odds?
                info_n[i]['error'] = 'Both VNC and rewarder sessions failed: {}; {}'.format(vnc_err, err)
            elif err is not None:
                info_n[i]['error'] = 'Rewarder session failed: {}'.format(err)
            else:
                info_n[i]['error'] = 'VNC session failed: {}'.format(vnc_err)

            self.crashed[i] = True
            self._close(i)

    def _handle_crashed_n(self, info_n):
        # This is just temporary. In the future, we'll get some new
        # environments and connect to those.
        if len(self.crashed) == self.n:
            errors = [info['error'] for info in info_n if 'error' in info]
            if len(errors) == 0:
                raise error.Error('All {} environments have crashed. No error key in info_n: {}'.format(self.n, info_n))
            else:
                raise error.Error('All {} environments have crashed! Most recent error: {}'.format(self.n, errors))
        for i in self.crashed:
            info_n[i]['remote.crashed'] = True

    def _propagate_obs_info(self, info_n, obs_info_n):
        for obs_info, info in zip(obs_info_n, info_n):
            # obs_info keys take precedence over info keys
            if obs_info is not None:
                info.update(obs_info)

    def _render(self, mode='human', close=False):
        if close:
            # render(close) is not currently supported by the Go VNCSession
            return

        if mode is 'human' and self.vnc_session is not None:
            if 0 not in self.crashed:
                self.vnc_session.render(self.connection_names[0])

    def __str__(self):
        return 'VNCEnv<{}>'.format(self.spec.id)

class Mask(object):
    """Blocks the agent from interacting with the environment while the
    environment is resetting.

    On the boundaries:

    - Mask will *drop* actions to environments which have just started
      resetting (i.e. returning done=True in this iteration and have
      env_state=resetting).

    - Mask will *allow* actions to environments which have just
      finished resetting (i.e. their env_state=running).

    - Mask will *allow* observations from environments which have just
      started resetting (i.e. returning done=True in this iteration
      and have env_state=resetting).

    - Mask will *allow* observations from environments which have just
      finished resetting (i.e. their env_state is running)
    """
    def __init__(self, n, initially_masked=True):
        self.n = n
        if initially_masked:
            self.mask = [None] * n
        else:
            self.mask = [True] * n

    def close(self, i):
        self.mask[i] = None

    def maintain_mask(self, done_n, info_n):
        self._unmask(info_n)
        observation_mask = list(self.mask)
        self._remask(done_n, info_n)
        action_mask = self.mask
        return observation_mask, action_mask

    def _unmask(self, info_n):
        # Unmask any environments which have finished resetting.
        for i, ok in enumerate(self.mask):
            if ok:
                continue

            # Env hasn't started yet
            if ok is None:
                if info_n[i].get('env_status.reset_complete'):
                    logger.info('[%d] Environment completed requested reset', i)
                    # Restore myself as ok
                    self.mask[i] = True
                else:
                    continue

            env_state = info_n[i].get('env_status.env_state')
            if env_state is None:
                # No rewarder message received, so nothing new to say
                continue
            elif env_state == 'running':
                episode_id = info_n[i]['env_status.episode_id']
                logger.info('[%d] Environment finished resetting (now on episode_id=%d)', i, episode_id)
                # Restore myself as ok
                self.mask[i] = True

        ##### pull the observation mask from here

    def _remask(self, done_n, info_n):
        for i, (done, info_i) in enumerate(zip(done_n, info_n)):
            if not done:
                continue

            # Mask any environments which just started resetting
            state_id = info_i['env_status.state_id']
            episode_id = info_i['env_status.episode_id']
            env_state = info_i['env_status.env_state']

            if env_state == 'running':
                logger.info('[%d] Episode ended: done=True state_id=%s episode_id=%s env_state=%s. Not masking since the reset has already completed.', i, state_id, episode_id, env_state)
            else:
                logger.info('[%d] Environment ended: done=True state_id=%s episode_id=%s env_state=%s', i, state_id, episode_id, env_state)
                self.mask[i] = False

    def apply_to_actions(self, action_n, info_n, mask):
        for i, ok in enumerate(mask):
            if ok:
                continue

            action_n[i] = []
            info_n[i]['mask.masked.action'] = True
        return self.mask

    def apply_to_return(self, observation_n, reward_n, done_n, info_n, mask):
        # Next, mask any environments which are resetting. We are
        # guaranteed to get done=True messages prior to getting the
        # env.describe message telling us it's resetting, so the
        # conservative route (block upon done=True, unblock upon
        # env.describe with env_state=running) locks us out of the
        # maximum surface area of environment reset possible.
        for i, ok in enumerate(mask):
            if ok:
                continue

            if reward_n[i] != 0 and ok is not None:
                # We should not be able to lose valid initial rewards
                # for an environment, since the env.describe will
                # always arrive before any rewards.
                #
                # We should not be able to lose valid final rewards
                # for an episode since the done message should arrive
                # after any rewards.
                #
                # A very fast reset (one encompassing an entire
                # episode) could cause us to lose rewards. But let's
                # see if it happens.
                logger.warn('WARNING: Masking non-zero reward for environment %d: %r. Unless you just reset the environment, this is unexpected in practice but not necessarily a bug; please report it. info=%s', i, reward_n[i], info_n)

            observation_n[i] = None
            reward_n[i] = 0
            done_n[i] = False
            info_n[i]['mask.masked.observation'] = True
