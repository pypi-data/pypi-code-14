import sys

dependencies = ["openpyxl", "pandas"]

for dependency in dependencies:
    try:
        __import__(dependency)
    except ImportError:
        sys.stderr.write("Pyspark DF Report Builder requires: {}".format(dependency))