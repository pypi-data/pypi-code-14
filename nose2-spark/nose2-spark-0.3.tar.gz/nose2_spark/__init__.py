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

    def update_spark_home(self):
        spark_home = self.spark_home
        if spark_home is not None:
            spark_home = os.path.abspath(spark_home)
            if not os.path.exists(spark_home):
                raise OSError(
                    "SPARK_HOME path specified in config does not exist: %s"
                    % self.spark_home)

        findspark.init(spark_home)

    @staticmethod
    def update_pythonpath(search_path):
        original_path = search_path

        search_path = os.path.abspath(search_path)
        if not os.path.exists(search_path):
            raise OSError(
                "PYFILES path specified in config does not exist: %s"
                % original_path)

        # updating for nose2
        sys.path.insert(0, search_path)

        # updating for imports inside Spark
        pypath = os.environ.get('PYTHONPATH')
        pypath = '%s:%s' % (search_path, pypath) if pypath else search_path
        os.environ['PYTHONPATH'] = pypath

    def createTests(self, event):
        self.update_spark_home()

        for pyf in self.pyfiles:
            self.update_pythonpath(pyf)
