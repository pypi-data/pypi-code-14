import ctypes
import hashlib
import json
import os
import pager
import platform
import sys
import time
import traceback

from kubos import sdk_config, utils, options
from kubos.utils import target, project, sdk

this_dir = os.path.dirname(os.path.abspath(__file__))

DISABLE = 0
INSTALL_UPDATE = 1
EVENTS = 2

EULA_ACCEPTED = 'eula-accepted'
TRACK_EVENTS = 'track-events'

class SDKConfigExt(sdk_config.KubosSDKConfig):
    def load_config(self):
        super(SDKConfigExt, self).load_config()
        self.tracker = Tracker(self.sdk_version, self.container_id,
                               self.sdk_edition)

        eula_path = os.path.join(this_dir, 'eula.txt')
        with open(eula_path, 'r') as f:
            eula_txt = f.read()

        eula_hash = hashlib.sha512(eula_txt).hexdigest()

        if not self.eula_accepted(eula_hash):
            self.prompt_eula(eula_txt, eula_hash)

        if self.eula_accepted(eula_hash):
            # EULA Accepted, setup tracking
            track_events = self.config.get(TRACK_EVENTS, False)
            self.tracker.set_level(EVENTS if track_events else INSTALL_UPDATE)

    def eula_accepted(self, eula_hash):
        eula_accepted = self.config.get(EULA_ACCEPTED, {})
        return eula_accepted.get('hash', None) == eula_hash

    def prompt_eula(self, eula_txt, eula_hash):
        self.accepted = False

        def prompt(pagenum):
            prompt = "Page -%s-. [A=I Accept] [Q=Cancel] [more..] " % pagenum
            pager.echo(prompt)
            ch = pager.getch()
            if ch in [pager.ESC_, pager.CTRL_C_, 'q', 'Q']:
                return False
            elif ch in ['a', 'A']:
                self.accepted = True
                return False
                pager.echo('\r' + ' '*(len(prompt)-1) + '\r')

        eula_path = os.path.join(this_dir, 'eula.txt')
        pager.page(open(eula_path, 'r'), pagecallback=prompt)

        if not self.accepted:
            print >>sys.stderr, 'Error: EULA not accepted, aborting'
            sys.exit(1)

        self.config[EULA_ACCEPTED] = {'hash': eula_hash, 'time': int(time.time())}
        self.config[TRACK_EVENTS] = self.prompt_track_events()
        self.save_config()

    def prompt_track_events(self):
        response = raw_input('''Kubos also tracks additional information about the usage of\
features to further improve the KubOS SDK. All collected information is \
anonymous, and will never be shared with a third party.

Share additional info with Kubos? [Y/n] ''')

        return response not in ['n', 'N']

sdk_config._config_class = SDKConfigExt

class SDKCommandExt(options.command.SDKCommand):
    def execCommand(self, args, following_args):
        self.config.tracker.trackCommand(self.name, args, following_args)
        start = time.time()
        try:
            super(SDKCommandExt, self).execCommand(args, following_args)
        finally:
            self.config.tracker.track('exec-time', {
                'name': self.name,
                'elapsed': time.time() - start
            })

options.command._command_class = SDKCommandExt

class Tracker(object):
    def __init__(self, version, build_number, edition, lang="en", level=DISABLE):
        self.level = DISABLE
        self.running = False

        if platform.system() == 'Darwin':
            dev_lib = os.path.join(this_dir, 'lib', 'osx', 'libanalytics.dylib')
            sdk_lib = os.path.join(sdk.KUBOS_RESOURCE_DIR, 'lib', 'osx', 'libanalytics.dylib')
        else:
            #This block is currently dead
            dev_lib = os.path.join(this_dir, 'lib', 'linux', 'libtrack.so')
            sdk_lib = os.path.join(sdk.KUBOS_RESOURCE_DIR, 'lib', 'linux', 'libanalytics.so')
            project.add_ld_library_path(os.path.join(sdk.KUBOS_RESOURCE_DIR, 'lib', 'linux'))

        lib = dev_lib if os.path.isfile(dev_lib) else sdk_lib
        self.libtrack = libtrack = ctypes.cdll.LoadLibrary(lib)

        libtrack.config.restype = None
        libtrack.config.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                                    ctypes.c_char_p, ctypes.c_char_p]

        libtrack.start.restype = None
        libtrack.stop.restype = None

        libtrack.track.restype = None
        libtrack.track.argtypes = [ctypes.c_char_p]

        libtrack.trackDouble.restype = None
        libtrack.trackDouble.argtypes = [ctypes.c_char_p, ctypes.c_double]

        libtrack.trackStr.restype = None
        libtrack.trackStr.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

        libtrack.trackException.restype = None
        libtrack.trackException.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                                            ctypes.c_char_p, ctypes.c_char_p]

        self.config(version, build_number, edition, lang)
        self.set_level(level)

    def set_level(self, level):
        self.level = level
        if level > DISABLE and not self.running:
            self.start(level=level)
        elif level == DISABLE and self.running:
            self.stop()

    def config(self, version, build_number, edition, lang):
        self.libtrack.config(version, build_number, edition, lang)

    def start(self, level=INSTALL_UPDATE):
        self.level = level
        self.running = True
        self.libtrack.start()

    def track(self, name, val=None):
        if self.level < EVENTS:
            return

        if type(val) in (float, int):
            self.libtrack.trackDouble(name, ctypes.c_double(val))
        elif type(val) is str:
            self.libtrack.trackStr(name, val)
        elif type(val) is dict:
            self.libtrack.trackStr(name, json.dumps(val))
        else:
            self.libtrack.track(name)

    def trackCommand(self, name, args, following_args):
        commandEnv = { 'target': utils.target.get_current_target() }
        #args is a namespace object. vars() returns args's dict() equivalent so we can use it
        arg_dict = vars(args)
        if name == 'target':
            commandEnv['newTarget'] = arg_dict['target']
        self.track(name, commandEnv)
        self.stop()

    def trackException(self, class_name, fn_name, msg, stack_trace):
        self.libtrack.trackException(class_name, fn_name, msg, stack_trace)

    def trackPyException(self):
        exc_info = sys.exc_info()
        class_name = exc_info[0].__name__
        stack = traceback.extract_stack(exc_info[2])
        fn_name = stack[0][2]
        msg = traceback.format_exception_only(exc_info[0], exc_info[1])
        stack_trace = ''.join(traceback.format_list(stack))
        exc_info = None
        self.trackException(class_name, fn_name, msg, stack_trace)

    def stop(self):
        self.level = DISABLE
        self.running = False
        self.libtrack.stop()

