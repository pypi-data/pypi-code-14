# -*- coding: utf-8 -*-
"""
Validate.py
^^^^^^^^^^

API for wwPDB Validation Web Service

:copyright: @wwPDB
:license: Apache 2.0, see LICENSE file for more details.


Updates:

     3-Aug-2016 jdw  add Authorization header
    20-Sep-2016 jdw  refactor for standard packaging
"""
# from __future__ import print_function
from __future__ import unicode_literals
# from __future__ import division
#
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import sys

# import six

from onedep import __version__
from onedep import __apiUrl__

#
from onedep.utils.ApiBase import ApiBase
log = logging.getLogger(__name__)


class Validate(ApiBase):

    def __init__(self, apiKey=None, apiUrl=None, errorFlagKey='onedep_error_flag', statusTextKey='onedep_status_text'):
        """
        OneDep validation webservice client API

        :param string apiKey: (Optional) security token.
        :param string apiUrl: (Optional) alternative API server URL.
        :param string errorFlagKey: (Optional) key for error flag in service return dictionary
        :param string statusTextKey: (Optional) key for status text in service return dictionary

        """
        apiUrl = apiUrl if apiUrl else __apiUrl__
        apiKey = apiKey if apiKey else "this_is_an_unassigned_api_key"
        userAgent = 'OneDepClient/%s Python/%s ' % (__version__, sys.version.split()[0])
        apiName = "valws"
        #
        super(Validate, self).__init__(apiKey=apiKey, userAgent=userAgent, apiName=apiName, apiUrl=apiUrl, verify=False)
        #
        #
        valContentTypes = {'model': ['pdbx'],
                           'structure-factors': ['pdbx'],
                           'nmr-chemical-shifts': ['pdbx'],
                           'nmr-restraints': ['any'],
                           'em-volume': ['map'],
                           'validation-report-full': ['pdf'],
                           'validation-data': ['xml'],
                           'validation-report-log': ['txt'],
                           'validation-report-slider': ['svg'],
                           }

        #
        self.setContentTypes(valContentTypes)
        #
        self.setApiReturnStatusKeys(errorFlagKey=errorFlagKey, statusTextKey=statusTextKey)

    def newSession(self):
        """  Create a new OneDep service session.

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text, and session_id)

        """
        return self.createSession()

    def inputModelXyzFile(self, pdbxFilePath):
        """  Input file containing model coordinates in PDBx/mmCIF format.

        :param string pdbxFilePath: full path to the input data file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)

        """
        return self.inputFile(filePath=pdbxFilePath, contentType='model', fileFormat='pdbx')

    def inputStructureFactorFile(self, pdbxFilePath):
        """  Input file containing structure factor amplitudes in PDBx/mmCIF format.

        :param string pdbxFilePath: full path to the input data file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.upload(filePath=pdbxFilePath, contentType='structure-factors', fileFormat='pdbx')

    def inputNmrChemicalShiftsFile(self, pdbxFilePath):
        """  Input file containing NMR chemical shift data in PDBx/mmCIF format.

        :param string pdbxFilePath: full path to the input data file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.upload(filePath=pdbxFilePath, contentType='nmr-chemical-shifts', fileFormat='pdbx')

    def inputNmrRestraints(self, nefFilePath):
        """  Input file containing NMR restraints data in NEF/STAR format.

        :param string nefFilePath: full path to the input data file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.upload(filePath=nefFilePath, contentType='nmr-restraints', fileFormat='nef')

    def inputEmVolume(self, ccp4MapFilePath):
        """  Input file containing EM volume data in CCP4 map format.

         :param string ccp4MapFilePath: full path to the input data file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.upload(filePath=ccp4MapFilePath, contentType='em-volume', fileFormat='map')

    def inputFile(self, filePath, contentType, fileFormat):
        """ Add the input data file to the current session context.

        :param string filePath: full path to the input data file
        :param string contentType: a supported content type (e.g. model, structure factors, ...)
        :param string fileFormat: a supported format type (e.g. pdbx, map, ...)

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.upload(filePath, contentType, fileFormat)

    def getStatus(self):
        """  Return the service status for the current session.

         :rtype: json service response converted to dictionary (with mininal keys: status, api_error_flag, api_status_text)
        """
        return self.post(endPoint="session_status")

    def getReport(self, filePath):
        """  Store the output validation report from the current session context in the specified output file path.

        :param string filePath: full path to the output file

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.downloadByType(dstPath=filePath, contentType="validation-report-full")

    def getReportData(self, filePath):
        """  Store the output validation data file from the current session context in the specified output file path.

        :param string filePath: full path to the output file

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.downloadByType(dstPath=filePath, contentType="validation-data")

    def getReportLog(self, filePath):
        """  Store the output session log file from the current session context in the specified output file path.

        :param string filePath: full path to the output file

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.downloadByType(dstPath=filePath, contentType="validation-report-log")

    def getOutputByType(self, filePath, contentType):
        """  Store the output file containing 'contentType' from the current session context in the specified output file path.

        :param string filePath: full path to the output file
        :param string contentType: target contentType

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.downloadByType(dstPath=filePath, contentType=contentType)

    def getIndex(self):
        """  Return a catalog of the data content of the current session.

         :rtype: json service response converted to dictionary (catalog plus keys - api_error_flag, api_status_text, index)
        """
        return self.post(endPoint="session_index")

    def getActivity(self):
        """  Return a summary service activity for the current service user.

         :rtype: json service response converted to dictionary (catalog plus keys - api_error_flag, api_status_text, activity_summary)
        """
        return self.post(endPoint="activity")

    def run(self, **params):
        """  Submit request to run the validation suite using the current session
             data file content.

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.post(endPoint="validate_request", **params)
