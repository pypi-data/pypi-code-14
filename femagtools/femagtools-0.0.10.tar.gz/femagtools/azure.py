"""
Author: Nicolas Mauchle <mauchle@semafor.ch>
To use this class you have to install:

 - --pre azure
 - msrest
 - msrestazure

Also you have to set up an application account

"""
import logging
import os
import threading      # Not supported from httplib
import time
import femagtools
import random         # later used in create project
import pdb
from .config import Config

logger = logging.getLogger(__name__)

AZURE_MODULE_FOUND = True
try:
    from azure.storage.blob import BlockBlobService
except:
    AZURE_MODULE_FOUND = False

block_blob_service = BlockBlobService(account_name='myaccount', account_key='mykey')
