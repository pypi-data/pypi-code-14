from client.protocols.common import models
from client.utils import auth
import client
import datetime
import json
import logging
import os
import pickle
import socket
import ssl
import urllib.error
import urllib.request

log = logging.getLogger(__name__)

class BackupProtocol(models.Protocol):

    # Timeouts are specified in seconds.
    SHORT_TIMEOUT = 2

    RETRY_LIMIT = 5
    BACKUP_FILE = ".ok_messages"
    BACKUP_ENDPOINT = '{prefix}://{server}/api/v3/backups/'
    REVISION_ENDPOINT = '{prefix}://{server}/api/v3/revision/'

    def run(self, messages):
        if self.args.local or self.args.restore:
            return

        if self.args.revise:
            action = 'Revise'
        elif self.args.submit:
            action = 'Submission'
        else:
            action = 'Backup'

        message_list = self.load_unsent_messages()

        access_token = auth.authenticate(False)
        log.info('Authenticated with access token %s', access_token)
        log.info('Sending unsent messages %s', access_token)

        if not access_token:
            print("Not authenticated. Cannot send {} to server".format(action))
            self.dump_unsent_messages(message_list)
            return

        # Messages from the current backup to send first
        is_send_first = self.args.submit or self.args.revise
        subm_messages = [messages] if is_send_first else []

        if is_send_first:
            response = self.send_all_messages(access_token, subm_messages,
                                              current=True)
            if message_list:
                self.send_all_messages(access_token, message_list,
                                       current=False)
        else:
            message_list.append(messages)
            response = self.send_all_messages(access_token, message_list,
                                              current=False)

        prefix = 'http' if self.args.insecure else 'https'
        base_url = '{0}://{1}'.format(prefix, self.args.server) + '/{}/{}/{}'

        if isinstance(response, dict):
            print('{action} successful for user: {email}'.format(action=action,
                        email=response['data']['email']))

            submission_type = 'submissions' if self.args.submit else 'backups'
            url = base_url.format(response['data']['assignment'],
                                  submission_type,
                                  response['data']['key'])

            if self.args.submit or self.args.backup:
                print('URL: {0}'.format(url))

            if self.args.backup:
                print('NOTE: this is only a backup. '
                      'To submit your assignment, use:\n'
                      '\tpython3 ok --submit')

        self.dump_unsent_messages(message_list + subm_messages)
        print()


    @classmethod
    def load_unsent_messages(cls):
        message_list = []
        try:
            with open(cls.BACKUP_FILE, 'rb') as fp:
                message_list = pickle.load(fp)
            log.info('Loaded %d backed up messages from %s',
                     len(message_list), cls.BACKUP_FILE)
        except (IOError, EOFError) as e:
            log.info('Error reading from ' + cls.BACKUP_FILE + \
                     ', assume nothing backed up')
        return message_list


    @classmethod
    def dump_unsent_messages(cls, message_list):
        with open(cls.BACKUP_FILE, 'wb') as f:
            log.info('Save %d unsent messages to %s', len(message_list),
                     cls.BACKUP_FILE)

            pickle.dump(message_list, f)
            os.fsync(f)


    def send_all_messages(self, access_token, message_list, current=False):
        if current and self.args.revise:
            action = "Revise"
        elif current and self.args.submit:
            action = "Submit"
        else:
            action = "Backup"

        num_messages = len(message_list)
        send_all = self.args.submit or self.args.backup
        retries = self.RETRY_LIMIT

        if send_all:
            timeout = None
            stop_time = datetime.datetime.max
            retries = self.RETRY_LIMIT * 2
        else:
            timeout = self.SHORT_TIMEOUT
            stop_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
            log.info('Setting timeout to %d seconds', timeout)

        first_response = None
        error_msg = ''
        log.info("Sending {0} messages".format(num_messages))

        while retries > 0 and message_list and datetime.datetime.now() < stop_time:
            log.info('Sending messages...%d left', len(message_list))

            print('{action}... {percent}% complete'.format(action=action,
                percent=100 - round(len(message_list) * 100 / num_messages, 2)),
                end='\r')

            # message_list is assumed to be ordered in chronological order.
            # We want to send the most recent message first, and send older
            # messages after.
            message = message_list[-1]

            try:
                response = self.send_messages(access_token, message, timeout, current)
            except socket.timeout as ex:
                log.warning("socket.timeout: %s", str(ex))
                retries -= 1
                error_msg = 'Connection timed out after {} seconds. '.format(timeout) + \
                            'Please check your network connection.'
            except ssl.CertificateError as ex:
                log.warning("SSL Error: %s", str(ex))
                retries -= 1
                error_msg = 'SSL Verification Error: {}\n'.format(ex) + \
                            'Please check your network connection and SSL configuration.'
            except (urllib.error.URLError, urllib.error.HTTPError) as ex:
                log.warning('%s: %s', ex.__class__.__name__, str(ex))
                retries -= 1
                if not hasattr(ex, 'read'):
                    error_msg = 'Please check your network connection:\n{}'.format(ex)
                    continue

                try:
                    response_json = json.loads(ex.read().decode('utf-8'))
                except json.decoder.JSONDecodeError as ex:
                    log.warning("Invalid JSON Response", exc_info=True)
                    retries -= 1
                    error_msg = 'Invalid Server Error Response: {} \n'.format(ex) + \
                                'The server did not provide a valid response. Try again soon.'
                    continue

                log.warning('%s: %s', ex.__class__.__name__, str(ex))
                log.warning('%s error message: %s', ex.__class__.__name__,
                            response_json['message'])

                if ex.code == 403 and 'download_link' in response_json['data']:
                    retries = 0
                    error_msg = 'Aborting because OK may need to be updated.'
                else:
                    retries -= 1
                    error_msg = response_json['message']
            else:
                if not first_response:
                    first_response = response
                message_list.pop()

        if current and error_msg:
            print()     # Preserve progress bar.
            print('Could not', action.lower() + ':', error_msg)
        elif not message_list:
            print('{action}... 100% complete'.format(action=action))
            return first_response
        elif not send_all:
            # Do not display any error messages if --backup or --submit are not
            # used.
            print()
        elif not error_msg:
            # No errors occurred, but could not complete request within TIMEOUT.
            print()     # Preserve progress bar.
            print('Could not {} within {} seconds.'.format(action.lower(), timeout))
        else:
            # If not all messages could be backed up successfully.
            print()     # Preserve progress bar.
            print('Could not', action.lower() + ':', error_msg)

    def send_messages(self, access_token, messages, timeout, current):
        """Send messages to server, along with user authentication."""
        is_submit = current and self.args.submit and not self.args.revise
        is_revision = current and self.args.revise

        data = {
            'assignment': self.assignment.endpoint,
            'messages': messages,
            'submit': is_submit
        }
        serialized_data = json.dumps(data).encode(encoding='utf-8')

        if is_revision:
            address = self.REVISION_ENDPOINT.format(server=self.args.server,
                        prefix='http' if self.args.insecure else 'https')
        else:
            address = self.BACKUP_ENDPOINT.format(server=self.args.server,
                        prefix='http' if self.args.insecure else 'https')
        address_params = {
            'access_token': access_token,
            'client_name': 'ok-client',
            'client_version': client.__version__,
        }
        address += '?'
        address += '&'.join('{}={}'.format(param, value)
                            for param, value in address_params.items())

        redacted_address = address.replace(access_token, '*******')
        log.info('Sending messages to %s', redacted_address)

        request = urllib.request.Request(address)
        request.add_header("Content-Type", "application/json")

        response = urllib.request.urlopen(request, serialized_data, timeout)

        return json.loads(response.read().decode('utf-8'))

protocol = BackupProtocol
