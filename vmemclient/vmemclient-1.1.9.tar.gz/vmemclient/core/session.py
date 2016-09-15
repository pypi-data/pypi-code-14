#!/usr/bin/env python

"""
Copyright 2012 - 2015 Violin Memory, Inc..

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
import json
import sys
import urllib
import urllib2

from vmemclient.core import request
from vmemclient.core.node import XGNode
from vmemclient.core.error import *
from vmemclient.core.response import XGResponse


class BasicSession(object):
    """A basic REST session object.

    This class will never directly be created, but exists only to
    be inherited from.
    """
    def __init__(self, host, user, password, debug,
                 proto, keepalive, log_fd, port):
        self.host = str(host)
        self.user = str(user)
        self.password = str(password)
        self.debug = bool(debug)
        self.proto = str(proto).lower()
        self.keepalive = bool(keepalive)
        self._closed = True

        # Verify the protocol
        if proto not in ('https', 'http'):
            raise ValueError('Protocol {0} not supported'.format(proto))

        if proto is 'https':
           port = 443

        # Verify the logger
        if log_fd is None:
            self.log_fd = sys.stdout
        elif (hasattr(log_fd, 'write') and callable(log_fd.write) and
              hasattr(log_fd, 'flush') and callable(log_fd.flush)):
            self.log_fd = log_fd
        else:
            raise ValueError('log_fd needs callable "write" ' +
                             'and "flush" methods')

        # Verify the port
        if port is None:
            self.port = None
        else:
            self.port = int(port)

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def __repr__(self):
        values = ['<{0}'.format(self.__class__.__name__),
                  'host:{0}'.format(self.host),
                  'user:{0}'.format(self.user),
                  'password:{0}'.format(self.password),
                  'proto:{0}'.format(self.proto)]
        return ' '.join(values)

    def login(self):
        '''Open the REST connection (invokes open()).'''
        return self.open()

    def open(self):
        raise NotImplementedError

    @property
    def closed(self):
        """If the connection is believed to be open or not."""
        return self._closed

    def close(self):
        raise NotImplementedError

    def log(self, msg):
        self.log_fd.write('{0}\n'.format(msg))
        self.log_fd.flush()


class XGSession(BasicSession):
    """XML Gateway session object

    The XGSession is used to send and receive XML based messages
    to a Violin Memory Gateway or Memory Array. In addition to
    sending requests and receiving responses, it also manages
    authentication by logging in at initialization and retaining
    the authentication cookie returned.
    """

    def __init__(self, host, user='admin', password='',
                 debug=False, proto='https', autologin=True,
                 keepalive=False, log_fd=None, port=None):
        """Create new XGSession instance.

        Arguments:
            host      -- Name or IP address of host to connect to.
            user      -- Username to login with.
            password  -- Password for user
            debug     -- Enable/disable debugging to stdout (bool)
            proto     -- Either 'http' or 'https'
            autologin -- Should auto-login or not (bool)
            keepalive -- Attempt auto-reconnects on autologout
            log_fd    -- Where to send log messages to
        """
        super(XGSession, self).__init__(host, user, password, debug,
                                        proto, keepalive, log_fd, port)
        self.request_url = '{0}://{1}/admin/launch?script=xg'.format(
                           self.proto, self.host)
        self._handle = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        if autologin and not self.open():
            raise AuthenticationError('Incorrect authentication credentials')

    def open(self):
        """Login to the host and save authentication cookie."""
        login_url = ('{0}://{1}/admin/launch'.format(self.proto, self.host) +
                     '?script=rh&template=login&action=login')

        login_data = urllib.urlencode({'d_user_id': 'user_id',
                                       't_user_id': 'string',
                                       'c_user_id': 'string',
                                       'e_user_id': 'true',
                                       'f_user_id': self.user,
                                       'f_password': self.password,
                                       'Login': 'Login',
                                       })

        # Handle various login responses.  A valid login must contain all
        # of the following searched for parameters.
        valid_responses = [['template=dashboard', "HTTP-EQUIV='Refresh'"],
                           ['template=index', 'HTTP-EQUIV="Refresh"']]

        try:
            resp = self._handle.open(login_url, login_data).read()
            for valid_response_list in valid_responses:
                checks = [x in resp for x in valid_response_list]
                if all(checks):
                    self.log('Successfully logged in using {0}'.format(
                             self.proto))
                    self._closed = False
                    return True
            else:
                self.log('Failed to login using {0}'.format(self.proto))
                if self.debug:
                    self.log('Response: {0}'.format(resp))
        except (urllib2.HTTPError, urllib2.URLError) as e:
            self.log('{0} {1}: {2}'.format(e.__class__.__name__, self.host, e))

        return False

    def close(self):
        """Close the connection to the given Violin Memory appliance."""
        if self.closed:
            return

        url = '{0}://{1}/admin/launch?script=rh&template=logout&action=logout'

        try:
            resp = self._handle.open(url.format(self.proto, self.host))
            pg = resp.read()
            if 'You have been successfully logged out.' not in pg:
                self.log('Failed logout, somehow:\n{0}'.format(pg))
            else:
                self._closed = True
        except (urllib2.HTTPError, urllib2.URLError) as e:
            self.log('{0}: {1}'.format(e.__class__.__name__, e))

    def _get_version_info(self):
        """Get a dict of version info."""
        node = '/system/version/release'
        ans = self.get_node_values(node)[node]
        host_type = ans[0]
        return {'type': ans[0],
                'version': ans[1:]}

    def send_request(self, req, strip=None, retry=True):
        """Sends an XGRequest to the host and returns a XGResponse object.

        Arguments:
            req    -- An XGRequest object
            strip  -- Key prefix stripping (deprecated)
            retry  -- Should the request try again on autologout
        """
        data = req.to_xml()

        if self.debug:
            self.log('sending:\n{0}'.format(data))
        try:
            resp = self._handle.open(self.request_url, data)
            resp_str = resp.read()
            if self.debug:
                self.log('received:\n{0}'.format(resp_str))

            return XGResponse.fromstring(req, resp_str, strip)
        except AuthenticationError as e:
            self._closed = True
            if self.keepalive and retry:
                self.log('Attempting keepalive reconnect')
                if self.login():
                    return self.send_request(req, strip, False)
            raise e
        except (urllib2.HTTPError, urllib2.URLError) as e:
            msg = '{0}: {1}'.format(e.__class__.__name__, e)
            self.log(msg)
            raise NetworkError(msg)

    def save_config(self):
        """Save the configuration on the remote system.

        Equivalent to a "conf t" "wr mem".

        Returns:
            Action result as a dict.
        """
        return self.perform_action('/mgmtd/db/save')

    def get_nodes(self, node_names, nostate=False, noconfig=False):
        """Retrieve a "flat" list of XGNode objects based on node_names.

        If you wish to perform some iteration over a representational
        hierarchy, use get_node_tree() instead.

        This takes similar arguments to get_node_values() but returns
        all the node infomation received from the gateway in terms of
        XGNode objects.

        Arguments:
            node_names  -- String or list of node names or patterns (see
                           below) that will be queried.
            nostate     -- Set to True to not return state nodes.
            noconfig    -- Set to True to not return config nodes.

        Returns:
            list()      -- A flat (non-hierarchical) dict-like object with
                           keys as the node name and values of XGNode objects.

        Node name syntax:

        get_nodes() uses the same primitive pattern syntax used
        for TMS XML GET requests, namely:

        If a node name name ends with ..
            /*    perform a shallow iteration (no subtree option).
            /**   perform a subtree iteration.
            /***  perform a subtree iteration and include node itself
        """
        return self._get_nodes(node_names, nostate, noconfig, flat=True)

    def _get_nodes(self, node_names, nostate=False, noconfig=False,
                   flat=False, values_only=False, strip=None):
        """Internal worker function for:

            * get_nodes
            * get_node_values
        """
        query_flags = []
        if nostate:
            query_flags.append("no-state")
        if noconfig:
            query_flags.append("no-config")

        # Convert basestring to list, so we can accept either now
        if isinstance(node_names, basestring):
            node_names = [node_names]

        nodes = []
        for n in node_names:
            nodes.append(XGNode(n, flags=query_flags))

        req = request.XGQuery(nodes, flat, values_only)
        resp = self.send_request(req, strip)

        # TODO(gfreeman): If we have send_request return empty nodes
        #       dict rather than None for error we can eliminate this
        #       conditional.
        return resp.nodes

    def get_node_values(self, node_names, nostate=False, noconfig=False,
                        strip=None):
        """Retrieve values of one or more nodes, returning as a flat dict.

        If you wish to perform some iteration over a representational
        hierarchy, use get_node_tree_values() instead.

        This is a convenience function for users who do not want to
        worry about node binding types or attributes and want to avoid
        the complexity of creating XGNodes and XGRequest objects
        themselves.

        Arguments:
            node_names  -- String or list of node names or patterns (see
                           below) that will be queried.
            nostate     -- Set to True to not return state nodes.
            noconfig    -- Set to True to not return config nodes.
            strip       -- String to remove from the beginning of each key

        Returns:
            dict()      -- A flat (non-hierarchical) dict-like object with
                           keys being the node name and values being the
                           node value.
        """
        return self._get_nodes(node_names, nostate=nostate,
                               noconfig=noconfig, flat=True,
                               values_only=True, strip=strip)

    def perform_action(self, name, nodes=None):
        """Performs the action specified and returns the result.

        Arguments:
            name  -- The node name (string)
            nodes -- The relevant nodes (list)

        Returns:
            A dict of the return code and message.
        """
        # Input validation
        if nodes is None:
            nodes = []
        if not isinstance(name, basestring):
            raise ValueError('Expecting name to be of type string')
        elif not isinstance(nodes, list):
            raise ValueError('Expecting nodes to be of type list')
        else:
            for x in nodes:
                if not isinstance(x, XGNode):
                    raise ValueError('Invalid node: {0}'.format(x.__class__))

        # Perform the action given
        req = request.XGAction(name, nodes)
        resp = self.send_request(req)
        return resp.as_action_result()

    def perform_set(self, nodes=None):
        """Performs a 'set' using the nodes specified and returns the result.

        Arguments:
            nodes -- The relevant nodes (list or XGNodeDict)

        Returns:
            A dict of the return code and message.
        """
        # Input validation
        if nodes is None:
            nodes = []
        try:
            # Works for XGNodeDict input
            set_nodes = nodes.get_updates()
        except (AttributeError, TypeError):
            # Assume list instead
            set_nodes = nodes
        if not isinstance(set_nodes, list):
            raise ValueError('Expecting nodes to be of type list')
        else:
            for x in set_nodes:
                if not isinstance(x, XGNode):
                    raise ValueError('Invalid node: {0}'.format(x.__class__))

        req = request.XGSet(set_nodes)
        resp = self.send_request(req)
        try:
            # Works for XGNodeDict input, clear the tracked modifications
            nodes.clear_updates()
        except (AttributeError, TypeError):
            pass
        return resp.as_action_result()

    def get_node_tree(self, node_names, nostate=False, noconfig=False):
        raise Exception("Not yet implemented.")

    def get_node_tree_values(self, node_names, nostate=False, noconfig=False):
        raise Exception("Not yet implemented.")

    def set_nodes_values(self, node_dict):
        """Sets nodes per dict with node name -> value mappings."""

        # Requires nodes to have type defined in lookup array
        raise Exception("Not yet implemented.")


class JsonSession(BasicSession):
    """JSON REST session object

    The JSession object is used to send and receive JSON REST based messages
    to a Violin Memory JSON host.  In addition to sending and receiving
    responses, it also manages authentication by logging in at initialization
    and retaining the authentication cookie returned.
    """

    _AUTH_ERROR_MESSAGES = ['You are not authenticated',
                            'Your session has expired']

    def __init__(self, host, user='admin', password='',
                 debug=False, proto='http', autologin=True,
                 keepalive=False, log_fd=None, port=None):
        """Create a new JSON session instance.

        Arguments:
            host      -- Hostname or IP address
            user      -- Username
            password  -- Password
            debug     -- Enable/disable debugging (bool)
            proto     -- Either 'http' or 'https'
            autologin -- Should auto-login or not (bool)
            keepalive -- Attempt auto-reconnects on autologout
            log_fd    -- Where to send log messages (default: stdout)
        """
        super(JsonSession, self).__init__(host, user, password, debug,
                                          proto, keepalive, log_fd, port)

        self._auth_error = self._AUTH_ERROR_MESSAGES[0]
        self.login_info = None
        self._url = '{0}://{1}/admin/rest'.format(self.proto, self.host)
        self._reset_handle()

        if autologin and not self.login():
            raise AuthenticationError('Incorrect authentication credentials')

    def _reset_handle(self):
        self._handle = urllib2.build_opener(urllib2.HTTPCookieProcessor())

    def open(self):
        """Login to the host and save the authentication cookie."""
        self._reset_handle()
        login_url = self._create_login_url()
        login_data = self._create_login_data()
        req = request.BasicJsonRequest(login_url, login_data)
        resp = None

        # Attempt the login
        try:
            resp = self._handle.open(req).read()
        except (urllib2.HTTPError, urllib2.URLError) as e:
            self.log('{0}: {1}'.format(e.__class__.__name__, e))
            return False
        self.log('Login response: {0}'.format(resp))

        # Load the JSON response
        try:
            resp = json.loads(resp)
        except ValueError as e:
            val = resp if resp is not None else str(e)
            raise ValueError('Non-JSON response: {0}'.format(val))

        # Check for errors (incorrect n/p, etc)
        try:
            self._check_response_for_errors(resp)
        except Exception as e:
            self.log(str(e))
            return False

        # Successful login, otherwise
        self._closed = False
        self._process_login_response(resp)
        self._auth_error = self._AUTH_ERROR_MESSAGES[1]
        self.login_info = resp
        self.update_properties()
        return True

    def close(self):
        """Close the connection to the given appliance."""
        self._close()
        self._closed = True
        self._auth_error = self._AUTH_ERROR_MESSAGES[0]
        self.login_info = None

    def update_properties(self):
        """Update / set the properties of this connection."""
        self._properties = {}

    def get(self, location, data=None, get_params=None, headers=None):
        """Return the results from performing a HTTP GET."""
        return self._communicate(request.GetRequest,
                                 location, data, get_params, headers)

    def post(self, location, data=None, get_params=None, headers=None):
        """Return the results from performing a HTTP POST."""
        return self._communicate(request.PostRequest,
                                 location, data, get_params, headers)

    def put(self, location, data=None, get_params=None, headers=None):
        """Return the results from performing a HTTP PUT."""
        return self._communicate(request.PutRequest,
                                 location, data, get_params, headers)

    def delete(self, location, data=None, get_params=None, headers=None):
        """Return the results from performing a HTTP DELETE."""
        return self._communicate(request.DeleteRequest,
                                 location, data, get_params, headers)

    def _communicate(self, cls_type, location, raw_data,
                     get_params, headers, retry=True):
        """Retrieve values of a specified JSON location.

        Returns:
            A dict with the answer.
        """
        data = json.dumps(raw_data) if raw_data else None
        if get_params is None:
            url_get_params = ''
        else:
            url_get_params = '?' + urllib.urlencode(get_params)
        req_obj = cls_type(
            self._url + location + url_get_params,
            data=data,
            headers={} if headers is None else headers,
        )
        if self.debug:
            self.log('Sending {0}: {1}'.format(
                     req_obj.get_method(), req_obj.get_full_url()))
            if req_obj.data:
                self.log('Data: {0}'.format(req_obj.data))
        resp = None

        # Attempt communication with the Violin appliance
        try:
            resp = self._handle.open(req_obj)
        except urllib2.HTTPError as e:
            if e.getcode() == 403:
                self._closed = True
                if self.keepalive and retry:
                    self.log('Attempting keepalive reconnect.')
                    if self.login():
                        return self._communicate(cls_type, location, raw_data,
                                                 get_params, headers, False)
                raise AuthenticationError(self._auth_error)
            results = e.read()
        else:
            results = resp.read()

        # Debug output
        if self.debug:
            self.log('Received {0}'.format(results))

        # Perform some translation on the results
        if results:
            # Try and turn results into JSON
            try:
                results = json.loads(results)
            except ValueError:
                pass
            # Look for errors in the results
            try:
                self._check_response_for_errors(results)
            except AuthenticationError:
                self._closed = True
                if self.keepalive and retry:
                    self.log('Attempting keepalive reconnect')
                    if self.login():
                        return self._communicate(cls_type, location,
                                                 raw_data, get_params,
                                                 headers, False)
                raise

        # Return the results
        return results


class ConcertoJsonSession(JsonSession):
    """The "basic" namespace for Concerto Violin devices."""

    _HTML_EXCEPTION_PATTERN = re.compile(
            '<[hH]3>Exception information:?(.+?)</[hH]3>.+?<[bB]>Message:?' +
            '</[bB]>.+?<[fF][oO][nN][tT].+?>(.+?)</[fF][oO][nN][tT]',
            re.DOTALL)

    def _check_response_for_errors(self, results):
        if isinstance(results, basestring):
            # Basestring errors take two forms:
            #   1) HTML page with an embedded error
            #   2) string with newlines, ending with a JSON error
            m = re.search(self._HTML_EXCEPTION_PATTERN, results)
            if m:
                raise UnknownPathError('{0}: {1}'.format(
                                       m.group(1).strip(), m.group(2).strip()))
            try:
                new_results = json.loads(results.split('\n')[-1])
            except ValueError:
                pass
            else:
                if (hasattr(new_results, 'get') and
                        not new_results.get('success', True)):
                    raise MissingParameterError(new_results.get('msg', ''))
        elif results.get('code', 'success') != 'success':
            if results['code'].lower() == 'unauthorized':
                raise AuthenticationError(self._auth_error)
            else:
                raise RestActionFailed('{0}: {1}'.format(
                                       results['code'], results['msg']))

    def _get_version_info(self):
        ans = self.get('/server/properties/version')
        if isinstance(ans, basestring):
            raise Exception('Version query returned string: {0}'.format(
                            ans))
        elif not ans['success']:
            raise Exception(ans['msg'])
        info = ans['data']
        info['version'] = '{0}.{1}'.format(info['concerto_version'],
                                           info['build'])
        info['build'] = int(info['build'])
        return info

    def _create_login_url(self):
        return '{0}://{1}:{2}/concerto/auth/login'.format(
            self.proto, self.host, self.port)

    def _create_login_data(self):
        return json.dumps({'data': {'username': self.user,
                                    'password': self.password,
                                    'server': self.host}})

    def _process_login_response(self, resp):
        self._url = '{0}://{1}:{2}/concerto'.format(
                self.proto, self.host, self.port)
        self.login_info = resp

    def _close(self):
        loc = '/auth/logout'
        retry_setting = self.keepalive
        self.keepalive = False
        try:
            resp = self.post(loc, json.loads(self._create_login_data()))
        except AuthenticationError:
            pass
        except Exception as e:
            self.log(e)
        self.keepalive = retry_setting

    def update_properties(self):
        """Update the properties of this connection object.

        Raises:
            QueryError
        """
        ans = self.get('/server/properties/info')
        if ans['success']:
            self._properties = ans['data']
        else:
            self.log('Properties query failed: {0}'.format(
                     ans.get('msg', str(ans))))
            self._properties = {}
