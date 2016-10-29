# coding=utf-8
import contextlib
import importlib
import json
import logging
import os
import shelve
import sys
import traceback

import form
import netop
import rpc


class NetMagusSession(object):
    """
    This class is a wrapper to handle an interactive session between the
    NetMagus backend and a user script.  It serves as a unifed API for user
    script operations to send/receive data with the NetMagus backend.  It
    also serves as a unified API for the NetMagus backend to call and execute
    user scripts.

    The NetMagus backend will call the module as (ex.):
        "python -m netmagus --script user.py --token aBcDeF --input-file
        /some/path/to/aBcDeF.json --loglevel 10

    The "token" is used by NM to desginate all file and RPC interactions tied
    to a given execution.

    This class will be called by the module's __main__.py file to:
     - read JSON from the NetMagus backend via the input-file if it exists
     - read in any previous state tied to the token/session
     - import the user's script/module and execute it's run() method
        - run() method must receive a NetMagusSession object as only arg
        - run() method may return NetOpStep or (NetOpStep, anyobject)
     - receive a NetOpStep (and a state object) as a return from the user's
       run() method
     - store any state object and send JSON response back to NetMagus backend

     The following attributes exist within each object:
    """

    _log_level_index = {
        0: 0,
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARN,
        4: logging.ERROR,
        5: logging.CRITICAL
    }



    def __init__(self, token, input_file, loglevel, script):
        """
        the launcher will simply parse CLI args and instantiate a new
        NetMagusSession. This will need to receive those CLI args and store
        to internal object state
        """
        self.token = token
        self.input_file = input_file
        self.loglevel = self._log_level_index[int(loglevel)]
        self.script = script
        self.logger = None
        self.nm_input = None
        self.user_state = None

        # Convenience methods for user script writers
        self.rpc_connect = rpc.rpc_connect
        self.rpc_disconnect = rpc.rpc_disconnect
        self.rpc_form = rpc.Form
        self.rpc_html = rpc.Html
        self.netopstep = netop.NetOpStep
        self.textarea = form.TextArea
        self.textinput = form.TextInput
        self.radiobutton = form.RadioButton
        self.passwordinput = form.PasswordInput
        self.dropdownmenu = form.DropDownMenu
        self.checkbox = form.CheckBox

    def rpc_send(self, message):
        rpc.rpc_send(self.token, message)

    def rpc_receive(self):
        return rpc.rpc_receive(self.token)

    def rpc_form_query(self, message, **kwargs):
        return rpc.rpc_form_query(self.token, message, **kwargs)

    def start(self):
        # if no logging was requested, disabled all output in the logging module
        if not self.loglevel:
            logging.disable(logging.CRITICAL)
        else:
            # Set the logging level here for all steps
            logging.basicConfig(level=self.loglevel)
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(self.loglevel)

        self.__read_response_file()
        self.__read_state_file()
        recipe_return = self.__run_user_script()
        self.__write_response_file(recipe_return)
        self.__write_state_file(self.user_state)

    def __run_user_script(self):
        try:
            if not os.path.isfile(self.script):
                raise IOError('Path to user script must be a full absolute '
                              'path, not just a file name.')
            sys.path.append(os.path.dirname(self.script))
            module_name = os.path.basename(self.script).split('.')[0]
            self.logger.debug('Importing user module {}'.format(module_name))
            user_module = importlib.import_module(module_name)
            self.logger.debug(
                    '{} imported user module named: {}'.format(
                            type(user_module),
                            user_module))
            recipe_return = user_module.run(self)
            if isinstance(recipe_return, netop.NetOpStep):
                next_step = recipe_return
                self.__fix_formcomponent_indexes(next_step)
                # user must pass full file path back to us for the next
                # script he  wants executed, we add the rest
                next_step.commandPath = ' '.join(
                        [sys.executable, '-m netmagus --script',
                         next_step.commandPath])
            elif isinstance(recipe_return, tuple):
                next_step, recipe_state = recipe_return
                self.__fix_formcomponent_indexes(next_step)
                next_step.commandPath = ''.join(
                        [self.script, next_step.commandPath])
            else:
                raise TypeError(
                        'Recipe files should return either NetOpStep or tuple('
                        'NetOpStep, stateobject)')
            return recipe_return
        except ImportError:
            self.logger.critical(
                    'Unable to load the specified python module: {}'.format(
                            self.script))
            raise
        except (Exception, NameError, IOError) as ex:
            self.logger.critical(
                    'Error calling run() method defined in the target file: '
                    '{}'.format(self.script))
            tb = traceback.format_exc()
            logging.exception(ex)
            htmlextrainfo = {
                'html': {
                    'printToUser': True,
                    'outputType': 'html',
                    'title': 'ERROR IN RECIPE',
                    'data': '<h3>This recipe has encountered a critical error '
                            'and can not continue.  Please review the '
                            'traceback info and/or contact support for '
                            'assistance.</h3><br><br>Traceback info was: '
                            '<pre>{}</pre>'.format(tb)
                }
            }
            next_step = netop.NetOpStep(currentStep=1, dataValid=False,
                                        extraInfo=htmlextrainfo)

        return next_step

    def __read_response_file(self):
        self.logger.debug('Reading JSON data from NetMagus request')
        try:
            with open(self.input_file) as data_file:
                self.nm_input = json.load(data_file)
            os.remove(self.input_file)  # remove file after reading it
        except IOError:
            self.logger.warn('Unable to access input JSON file {}'.format(
                    self.input_file))
        except TypeError:
            self.logger.error('Unable to decode JSON data in {}'.format(
                    self.input_file))

    def __read_state_file(self):
        state_file = self.input_file + '_State'
        with contextlib.closing(
                shelve.open(state_file, protocol=2, writeback=True)) \
                as state_shelve:
            try:
                self.user_state = state_shelve['recipe_state']
            except KeyError:
                self.logger.info(
                        'The file {} exists but does not contain previous '
                        'state from a recipe execution.  '
                        'Setting state to NONE'.format(state_file))
                self.user_state = None
            except IOError:
                self.logger.info(
                        'No _State file found from previous recipe execution '
                        'steps. Setting state to NONE.')
                self.user_state = None

    def __write_response_file(self, response):
        # store the returned data into a Response file for NetMagus to
        # continue the op if using file-based exchange
        response_file = self.input_file + 'Response'
        self.logger.debug(
                'Target output JSON file will be: {}'.format(response_file))
        try:
            with open(response_file, 'w') as outfile:
                outfile.write(str(response))
        except IOError:
            self.logger.error(
                    'Unable to open target JSON Response file: {}'.format(
                            response_file))
            raise

    def __write_state_file(self, stateobject):
        # store the returned state object into a file for future operation
        # steps to retrieve
        state_file = self.input_file + '_State'
        self.logger.debug(
                'Target output shelve file will be: {}'.format(state_file))
        try:
            with contextlib.closing(shelve.open(state_file, protocol=2,
                                                writeback=True)) as \
                    state_shelve:
                state_shelve['recipe_state'] = stateobject
        except IOError:
            self.logger.error(
                    'Unable to open target shelve state file: {}'.format(
                            state_file))
            raise

    def __fix_formcomponent_indexes(self, netop_obj):
        """
        This method is a temporary fix to append an index attribute to each
        form component to be sent to NetMagus as JSON.  Eventually this will
        be done in the NetMagus back-end upon receipt according to the order
        of the list of form controls.  For now these are being added here in
        the same fashion before being sent to the NetMagus back-end.
        :param netop_obj: a netmagus.NetOpStep object to be serialized and
        sent to NetMagus
        """
        # TODO: REMOVE INDEX INCREMENTING ONCE PROBERT100 FIXES NM
        index_counter = 0
        for item in netop_obj.form:
            setattr(item, 'index', index_counter)
            index_counter += 1
