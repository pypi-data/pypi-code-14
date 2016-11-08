#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.core import Extension


module = Extension('confluent_kafka_smyte.cimpl',
                    libraries= ['rdkafka'],
                    sources=['confluent_kafka_smyte/src/confluent_kafka_smyte.c',
                             'confluent_kafka_smyte/src/Producer.c',
                             'confluent_kafka_smyte/src/Consumer.c'])

setup(name='confluent-kafka-smyte',
      version='0.9.3',
      description='Smyte fork of Confluent\'s Apache Kafka client for Python',
      author='Confluent Inc',
      author_email='support@confluent.io',
      url='https://github.com/smyte-forks/confluent-kafka-python',
      ext_modules=[module],
      packages=find_packages(),
      data_files = [('', ['LICENSE'])])
