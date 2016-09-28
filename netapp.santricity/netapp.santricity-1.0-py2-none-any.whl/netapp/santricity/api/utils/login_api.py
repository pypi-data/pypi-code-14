#!/usr/bin/env python
# coding: utf-8

"""
LoginApi.py

  The Clear BSD License

  Copyright (c) – 2016, NetApp, Inc. All rights reserved.

  Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the limitations in the disclaimer below) provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

  * Neither the name of NetApp, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

  NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import absolute_import

import sys
import os

# python 2 and python 3 compatibility library
from six import iteritems

from ....santricity.configuration import Configuration
from ....santricity.api_client import ApiClient


class LoginApi(object):

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient(context_path='/devmgr/utils')
            self.api_client = config.api_client
    
    
    def logout(self, **kwargs):
            """
            
            

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.logout(callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :return: None
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = []
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method logout" % key
                    )
                params[key] = val
            del params['kwargs']

    

            resource_path = '/login'.replace('{format}', 'json')
            path_params = {}
    

            query_params = {}
    

            header_params = {}
    

            form_params = []
            local_var_files = {}
    

            body_params = None
    

            # HTTP header `Accept`
            header_params['Accept'] = self.api_client.\
                select_header_accept(['application/json'])
            if not header_params['Accept']:
                del header_params['Accept']

            # HTTP header `Content-Type`
            header_params['Content-Type'] = self.api_client.\
                select_header_content_type(['application/json'])

            # Authentication setting
            auth_settings = ['basicAuth']

            response = self.api_client.call_api(resource_path, 'DELETE',
                                                path_params,
                                                query_params,
                                                header_params,
                                                body=body_params,
                                                post_params=form_params,
                                                files=local_var_files,
                                                response_type=None,
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def perform_manual_login(self, login_request, **kwargs):
            """
            Perform a manual login
            

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.perform_manual_login(login_request, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param LoginRequest login_request:  (required)
    
            :return: LoginResponse
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['login_request']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method perform_manual_login" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'login_request' is set
            if ('login_request' not in params) or (params['login_request'] is None):
                raise ValueError("Missing the required parameter `login_request` when calling `perform_manual_login`")
    
    

            resource_path = '/login'.replace('{format}', 'json')
            path_params = {}
    

            query_params = {}
    

            header_params = {}
    

            form_params = []
            local_var_files = {}
    

            body_params = None
    
            if 'login_request' in params:
                body_params = params['login_request']
    

            # HTTP header `Accept`
            header_params['Accept'] = self.api_client.\
                select_header_accept(['application/json'])
            if not header_params['Accept']:
                del header_params['Accept']

            # HTTP header `Content-Type`
            header_params['Content-Type'] = self.api_client.\
                select_header_content_type(['application/json'])

            # Authentication setting
            auth_settings = ['basicAuth']

            response = self.api_client.call_api(resource_path, 'POST',
                                                path_params,
                                                query_params,
                                                header_params,
                                                body=body_params,
                                                post_params=form_params,
                                                files=local_var_files,
                                                response_type='LoginResponse',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def perform_manual_login_state_check(self, **kwargs):
            """
            Perform a manual login or check login state
            

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.perform_manual_login_state_check(callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str uid: userId
    
            :param str pwd: password
    
            :param str xsrf: XSRF protected
    
            :param bool onlycheck: Only check login status
    
            :return: LoginResponse
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['uid', 'pwd', 'xsrf', 'onlycheck']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method perform_manual_login_state_check" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
    
    
    
    
    
    
    

            resource_path = '/login'.replace('{format}', 'json')
            path_params = {}
    

            query_params = {}
    
            if 'uid' in params:
                query_params['uid'] = params['uid']
    
            if 'pwd' in params:
                query_params['pwd'] = params['pwd']
    
            if 'xsrf' in params:
                query_params['xsrf'] = params['xsrf']
    
            if 'onlycheck' in params:
                query_params['onlycheck'] = params['onlycheck']
    

            header_params = {}
    

            form_params = []
            local_var_files = {}
    

            body_params = None
    

            # HTTP header `Accept`
            header_params['Accept'] = self.api_client.\
                select_header_accept(['application/json'])
            if not header_params['Accept']:
                del header_params['Accept']

            # HTTP header `Content-Type`
            header_params['Content-Type'] = self.api_client.\
                select_header_content_type(['application/json'])

            # Authentication setting
            auth_settings = ['basicAuth']

            response = self.api_client.call_api(resource_path, 'GET',
                                                path_params,
                                                query_params,
                                                header_params,
                                                body=body_params,
                                                post_params=form_params,
                                                files=local_var_files,
                                                response_type='LoginResponse',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    









