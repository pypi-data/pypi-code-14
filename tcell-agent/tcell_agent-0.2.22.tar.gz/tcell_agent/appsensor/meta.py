# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

from tcell_agent.appsensor import params

class AppSensorMeta(object):
    def __init__(
            self,
            remote_address,
            method,
            location,
            route_id,
            session_id=None,
            user_id=None,
            transaction_id=None):
        self.remote_address = remote_address
        self.method = method
        self.location = location
        self.route_id = route_id
        self.session_id = session_id
        self.user_id = user_id
        self.transaction_id = transaction_id

        self.get_dict = None
        self.post_dict = None
        self.cookie_dict = None
        self.files_dict = None
        self.json_body_str = None
        self.request_content_len = None
        self.response_code = None
        self.do_request = False
        self.do_response = False
        self.user_agent_str = False

        self.do_path_parameters = False
        self.path_dict = None

    def request_data(
            self,
            request_content_len,
            get_dict,
            post_dict,
            cookie_dict,
            json_body_str,
            user_agent_str,
            files_dict):
        self.do_request = True
        self.get_dict = get_dict
        self.cookie_dict = cookie_dict
        self.json_body_str = json_body_str
        self.request_content_len = request_content_len
        self.user_agent_str = user_agent_str

        filenames_dict = {}
        for param_name in (files_dict or {}).keys():
            filenames_dict[param_name] = []
            for file_obj in files_dict.getlist(param_name):
                filenames_dict[param_name].append(file_obj.name)

        self.files_dict = params.flatten_clean(filenames_dict)
        self.post_dict = params.flatten_clean(post_dict)

    def response_data(self, response_content_len=None, response_code=None):
        self.do_response = True
        self.response_content_len = response_content_len
        self.response_code = response_code

    def path_parameters_data(self, path_dict):
        self.do_path_parameters = True
        self.path_dict = path_dict

