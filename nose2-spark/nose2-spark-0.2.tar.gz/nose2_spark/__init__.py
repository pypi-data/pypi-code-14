import os
import sys

import findspark

from nose2.events import Plugin


class Nose2Spark(Plugin):
    configSection = 'nose2-spark'
    commandLineSwitch = (None, 'pyspark', 'Add PySpark to PYTHONPATH')

    def __init__(self):
        self.spark_home = self.config.as_str('spark_home', None)
        self.pyfiles = self.config.as_list('pyfiles', [])

    @staticmethod
    def update_pythonpath(search_path):
        search_path = os.path.abspath(search_path)

        # updating for nose2
        sys.path.insert(0, search_path)

        # updating for imports inside Spark
        pypath = os.environ.get('PYTHONPATH')
        pypath = '%s:%s' % (search_path, pypath) if pypath else search_path
        os.environ['PYTHONPATH'] = pypath

    def createTests(self, event):
        findspark.init(spark_home=os.path.abspath(self.spark_home))

        for pyf in self.pyfiles:
            self.update_pythonpath(pyf)
