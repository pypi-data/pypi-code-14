#!/usr/bin/env python
# coding: utf-8

"""
MonitoringApi.py

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


class MonitoringApi(object):

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient(context_path='/devmgr/v2')
            self.api_client = config.api_client
    
    
    def clear_mel_events(self, system_id, **kwargs):
            """
            Clear MelEvents
            Mode: Both Embedded and Proxy. Gives the user the ability to clear the event cache and the EventLog directly on the StorageDevice.

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.clear_mel_events(system_id, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str system_id: The id of the storage-system (required)
    
            :param bool clear_cache: 
    
            :param bool reset_mel: Reset the EventLog on the StorageDevice
    
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

            all_params = ['system_id', 'clear_cache', 'reset_mel']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method clear_mel_events" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'system_id' is set
            if ('system_id' not in params) or (params['system_id'] is None):
                raise ValueError("Missing the required parameter `system_id` when calling `clear_mel_events`")
    
    
    
    
    
    

            resource_path = '/storage-systems/{system-id}/mel-events'.replace('{format}', 'json')
            path_params = {}
    
            if 'system_id' in params:
                path_params['system-id'] = params['system_id']
    

            query_params = {}
    
            if 'clear_cache' in params:
                query_params['clearCache'] = params['clear_cache']
    
            if 'reset_mel' in params:
                query_params['resetMel'] = params['reset_mel']
    

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
    
    def get_all_global_status_events(self, **kwargs):
            """
            Get all global status events
            Mode: Both Embedded and Proxy. 

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.get_all_global_status_events(callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param int last_known: The sequence number of the last event you have received
    
            :param int wait: seconds to wait for a new event
    
            :return: list[Event]
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['last_known', 'wait']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method get_all_global_status_events" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
    
    
    

            resource_path = '/events'.replace('{format}', 'json')
            path_params = {}
    

            query_params = {}
    
            if 'last_known' in params:
                query_params['lastKnown'] = params['last_known']
    
            if 'wait' in params:
                query_params['wait'] = params['wait']
    

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
                                                response_type='list[Event]',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def get_all_storage_device_status_events(self, system_id, **kwargs):
            """
            Get the list of status Events for the StorageDevice
            Mode: Both Embedded and Proxy. 

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.get_all_storage_device_status_events(system_id, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str system_id: The id of the storage-system (required)
    
            :param int last_known: 
    
            :param int wait: Amount of time to wait for a new event
    
            :return: list[Event]
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['system_id', 'last_known', 'wait']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method get_all_storage_device_status_events" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'system_id' is set
            if ('system_id' not in params) or (params['system_id'] is None):
                raise ValueError("Missing the required parameter `system_id` when calling `get_all_storage_device_status_events`")
    
    
    
    
    
    

            resource_path = '/storage-systems/{system-id}/events'.replace('{format}', 'json')
            path_params = {}
    
            if 'system_id' in params:
                path_params['system-id'] = params['system_id']
    

            query_params = {}
    
            if 'last_known' in params:
                query_params['lastKnown'] = params['last_known']
    
            if 'wait' in params:
                query_params['wait'] = params['wait']
    

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
                                                response_type='list[Event]',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def get_event_availability(self, system_id, **kwargs):
            """
            Check the oldest and newest available events
            Mode: Both Embedded and Proxy. 

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.get_event_availability(system_id, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str system_id: The id of the storage-system (required)
    
            :param bool cache_only: Only retrieve events currently in the cache
    
            :return: MelExtent
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['system_id', 'cache_only']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method get_event_availability" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'system_id' is set
            if ('system_id' not in params) or (params['system_id'] is None):
                raise ValueError("Missing the required parameter `system_id` when calling `get_event_availability`")
    
    
    
    

            resource_path = '/storage-systems/{system-id}/mel-events/available'.replace('{format}', 'json')
            path_params = {}
    
            if 'system_id' in params:
                path_params['system-id'] = params['system_id']
    

            query_params = {}
    
            if 'cache_only' in params:
                query_params['cacheOnly'] = params['cache_only']
    

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
                                                response_type='MelExtent',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def get_log_messages(self, system_id, **kwargs):
            """
            Get a list of log messages for based on input values.
            Mode: Embedded only. 

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.get_log_messages(system_id, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str system_id: The id of the storage-system (required)
    
            :param str logger_type: LoggerType to retrieve records for
    
            :param int start_record: Starting record number
    
            :param int ending_record: Ending record number
    
            :return: LoggerRecordResponse
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['system_id', 'logger_type', 'start_record', 'ending_record']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method get_log_messages" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'system_id' is set
            if ('system_id' not in params) or (params['system_id'] is None):
                raise ValueError("Missing the required parameter `system_id` when calling `get_log_messages`")
    
    
    
    
    
    
    
    

            resource_path = '/storage-systems/{system-id}/service-logs'.replace('{format}', 'json')
            path_params = {}
    
            if 'system_id' in params:
                path_params['system-id'] = params['system_id']
    

            query_params = {}
    
            if 'logger_type' in params:
                query_params['LoggerType'] = params['logger_type']
    
            if 'start_record' in params:
                query_params['startRecord'] = params['start_record']
    
            if 'ending_record' in params:
                query_params['endingRecord'] = params['ending_record']
    

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
                                                response_type='LoggerRecordResponse',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    
    def get_mel_events(self, system_id, **kwargs):
            """
            Retrieve MelEvents
            Mode: Both Embedded and Proxy. 

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please define a `callback` function
            to be invoked when receiving the response.
            >>> def callback_function(response):
            >>>     pprint(response)
            >>>
    
            >>> thread = api.get_mel_events(system_id, callback=callback_function)
    
    

            :param callback function: The callback function
                for asynchronous request. (optional)
    
            :param str system_id: The id of the storage-system (required)
    
            :param int start_sequence_number: 
    
            :param int count: Maximum number to retrieve
    
            :param bool critical: Only retrieve events classified as critical
    
            :param bool include_debug: Whether or not to retrieve debug entries
    
            :return: list[MelEntryEx]
                     If the method is called asynchronously,
                     returns the request thread.
            :raises: ValueError
                       If the required params are not provided or if the response data format is unknown.
                     TypeError:
                        When the data type of response data is different from what we are expecting
                     ApiException:
                        Occurs when we get a HTTP error code (422 and above).

            """

            all_params = ['system_id', 'start_sequence_number', 'count', 'critical', 'include_debug']
            all_params.append('callback')

            params = locals()
            for key, val in iteritems(params['kwargs']):
                if key not in all_params:
                    raise TypeError(
                        "Got an unexpected keyword argument '%s'"
                        " to method get_mel_events" % key
                    )
                params[key] = val
            del params['kwargs']

    
    
            # verify the required parameter 'system_id' is set
            if ('system_id' not in params) or (params['system_id'] is None):
                raise ValueError("Missing the required parameter `system_id` when calling `get_mel_events`")
    
    
    
    
    
    
    
    
    
    

            resource_path = '/storage-systems/{system-id}/mel-events'.replace('{format}', 'json')
            path_params = {}
    
            if 'system_id' in params:
                path_params['system-id'] = params['system_id']
    

            query_params = {}
    
            if 'start_sequence_number' in params:
                query_params['startSequenceNumber'] = params['start_sequence_number']
    
            if 'count' in params:
                query_params['count'] = params['count']
    
            if 'critical' in params:
                query_params['critical'] = params['critical']
    
            if 'include_debug' in params:
                query_params['includeDebug'] = params['include_debug']
    

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
                                                response_type='list[MelEntryEx]',
                                                auth_settings=auth_settings,
                                                callback=params.get('callback'))
            return response
    









