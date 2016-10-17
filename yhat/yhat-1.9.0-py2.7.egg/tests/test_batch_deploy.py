from __future__ import absolute_import
import unittest
import tarfile
import os
import json

from yhat.deployment.save_session import save_function
from yhat import batch

# Function test whether the bundling code will
def external_func():
    print("Hello from outside the class!")

class BatchTestDeploy(unittest.TestCase):

    test_archive = ".tmp_yhat_job_test.tar.gz"

    def setUp(self):
        # Stand up the mock server
        pass

    # Remove test files that were created locally
    def tearDown(self):
        # Bring down the mock server
        pass

    # Create a new batch job class with an execute method
    class TestBatchJob(batch.BatchJob):
        def execute():
            print("Hello")
            external_func()

    # Test for creation of the bundle tar
    def testBatchDeploy(self):
        pass

if __name__ == '__main__':
    unittest.main()
