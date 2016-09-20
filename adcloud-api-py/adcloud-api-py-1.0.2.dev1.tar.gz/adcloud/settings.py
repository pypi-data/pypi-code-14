#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import logging
import logging.config
from builder import SQLSessionBuilder

from errors import (ADCFileUnFoundError,
                    ADCMissingRequiredOptionError,
                    ADCTypeError,
                    ADCInvalidSettingError,
                    ADCSettingValueTypeError,)

from handler import FunctionHandler
from entities import (ADCEngine,
                           ADCUserLogs,
                           ADCDataset,
                           ADCDatasetField,
                           ADCDatasetRelationship,)


_logger = logging.getLogger(__name__)

class APISettings(object):
    valid_settings = {
        "dataset": {"type": int, 'required': True},
        "fields": {"type": list, 'required': True},
        "filter": {"type": str, 'required': True},
        "aggregate": {"type": list, 'required': False},
        "groups": {"type": list, 'required': False},
        "sort": {"type": list, 'required': False, "value": {"type": tuple, "words": ["desc", "asc"]}},
        "limits": {"type": int, 'required': False},
    }

    def __init__(self, session_builder, api_config):
        self.api_config = api_config
        self._session = session_builder.getSession()

        self._init_attributes()

    def _init_attributes(self):
        # validate required setting option.
        for key, value in self.valid_settings.items():
            if value['required']:
                if not self.api_config.has_key(key):
                    raise ADCInvalidSettingError(
                        "The setting of %s is required." % (key))

        # validate the setting type
        for key, value in self.api_config.items():
            setattr(self, key, value)
            if self.valid_settings.has_key(key):
                if not isinstance(value, self.valid_settings[key]['type']):
                    raise ADCInvalidSettingError("The type of '%s' is incorrect,it should be a %s." % (
                        key, self.valid_settings[key]['type']))

                if self.valid_settings[key].has_key('value'):
                    for element in self.api_config[key]:
                        if not isinstance(element, self.valid_settings[key]['value']['type']):
                            raise ADCInvalidSettingError(
                                "The type of '%s' is incorrect,it should be a list of tuples." % (key))

                        if element[1] not in self.valid_settings[key]['value']['words']:
                            raise ADCInvalidSettingError("The key word %s is invalid,you can choose one in %s." % (
                                element[1], self.valid_settings[key]['value']['words']))
            else:
                raise ADCInvalidSettingError(
                    "The setting of '%s' is invalid." % (key))

        # validate dependency setting options
        if self.api_config.has_key('aggregate') != self.api_config.has_key('groups'):
            raise ADCInvalidSettingError(
                "The both options of 'aggregate' and 'groups' should be required or missed at the same time.")

        if self.api_config.has_key('groups') and self.api_config.has_key('fields'):
            for field in self.api_config['fields']:
                if field not in self.api_config['groups']:
                    raise ADCInvalidSettingError("The field %s not exists in groups list %s." % (
                        field, self.api_config['groups']))

        if self.api_config.has_key('sort') and self.api_config.has_key('fields'):
            for field, _ in self.api_config['sort']:
                if field not in self.api_config['fields']:
                    raise ADCInvalidSettingError("The field %s not exists in fields list %s." % (
                        field, self.api_config['fields']))

        # compare settings with meta data in database

        adc_dataset = self._session.query(ADCDataset).filter(
            ADCDataset.id == self.api_config['dataset']).one()
        if adc_dataset is None:
            raise ADCInvalidSettingError(
                "The dataset '%s' is invalid." % (self.api_config['dataset']))

        adc_engine = self._session.query(ADCEngine).filter(
            ADCEngine.id == adc_dataset.table.datasource.adc_engine.id).one()

        dataset_relations = self._session.query(ADCDatasetRelationship).filter(
            ADCDatasetRelationship.foreign_dataset == adc_dataset)


        valid_fields = []
        
        for relation in dataset_relations:
            valid_fields = valid_fields + relation.primary_dataset.fields

        valid_fields = valid_fields + adc_dataset.fields

        valid_field_dict = {}
        for field in valid_fields:
            valid_field_dict[field.field_name] = field

        self.fields=[]
        # validate fields
        for field_name in self.api_config['fields']:
            if not valid_field_dict.has_key(field_name):
                raise ADCInvalidSettingError("The value of '%s' is invalid in fields %s,and may be one in %s." % (
                    field_name, self.api_config['fields'],valid_field_dict.keys()))
            else:
                self.fields.append(valid_field_dict[field_name])
                #if valid_field_dict[field_name].dataset!=adc_dataset:


        self.aggregates=[]
        # validate aggregate
        if self.api_config.has_key('aggregate'):
            for field_name,agg_func in self.api_config['aggregate']:
                if not valid_field_dict.has_key(field_name):
                    raise ADCInvalidSettingError("The value of '%s' is invalid in aggregate %s." % (
                        field_name, self.api_config['aggregate']))
                else:
                    self.aggregates.append((valid_field_dict[field_name],agg_func))

        self.groups=[]
        # validate groups
        if self.api_config.has_key('groups'):
            for field_name in self.api_config['groups']:
                if not valid_field_dict.has_key(field_name):
                    raise ADCInvalidSettingError("The value of '%s' is invalid in groups %s." % (
                        field_name, self.api_config['groups']))
                else:
                    self.groups.append(valid_field_dict[field_name])

        self.sorts=[]
        # validate sort
        if self.api_config.has_key('sort'):
            for field_name,sort_type in self.api_config['sort']:
                if not valid_field_dict.has_key(field_name):
                    raise ADCInvalidSettingError("The value of '%s' is invalid in sort %s." % (
                        field_name, self.api_config['sort']))
                else:
                    self.sorts.append((valid_field_dict[field_name],sort_type))

        self.adc_dataset = adc_dataset
        self.dataset_relations = dataset_relations
        self.adc_engine = adc_engine
        self.adc_datasource=self.adc_dataset.table.datasource
        self.datasource_settings=None
        if self.adc_datasource.settings:
            self.datasource_settings=eval(self.adc_datasource.settings)
        self.limits=None
        if self.api_config.has_key('limits'):
            self.limits=self.api_config['limits']



