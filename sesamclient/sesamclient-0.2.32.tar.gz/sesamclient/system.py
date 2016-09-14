# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import json
import logging
import copy


from .entitybase import EntityBase
from . import utils


logger = logging.getLogger(__name__)


class System(EntityBase):
    """
    This class represents a system.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete(self):
        """Deletes this system from the sesam-node.
        """
        url = self._connection.get_system_url(self.id)
        response = self._connection.do_delete_request(url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        self.update_raw_jsondata(response.text)

    def modify(self, system_config):
        """Modifies the system with the specified configuration."""
        system_config = copy.deepcopy(system_config)
        system_config["_id"] = self.id
        response = self._connection.do_put_request(self._connection.get_system_config_url(self.id), json=system_config)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        self.update_raw_jsondata(response.text)

    @property
    def runtime(self):
        return copy.deepcopy(self._raw_jsondata["runtime"])

    def get_sourceconfigs(self):
        url = self._connection.get_system_sourceconfigs_url(self.id)
        response = self._connection.do_get_request(url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        return response.json()

    def get_sinkconfigs(self):
        url = self._connection.get_system_sinkconfigs_url(self.id)
        response = self._connection.do_get_request(url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        return response.json()

    def get_metadata(self):
        """Gets the current metadata for this system"""
        url = self._connection.get_system_metadata_url(self.id)
        response = self._connection.do_get_request(url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        metadata = response.json()
        return metadata

    def set_metadata(self, metadata):
        """Replaces the metadata for this system with the specified dictionary"""
        url = self._connection.get_system_metadata_url(self.id)
        response = self._connection.do_put_request(url, json=metadata)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])

    def delete_metadata(self):
        """Deleted all metadata for this system"""
        url = self._connection.get_system_metadata_url(self.id)
        response = self._connection.do_delete_request(url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
