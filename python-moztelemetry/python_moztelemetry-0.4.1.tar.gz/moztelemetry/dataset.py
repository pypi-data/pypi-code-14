# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import copy_reg
import json
import random
import types
from copy import copy
from itertools import chain, islice
from multiprocessing import cpu_count
from concurrent import futures

from moztelemetry import heka_message_parser
from .store import S3Store


MAX_CONCURRENCY = int(cpu_count() * 1.5)


def _group_by_size(obj_list):
    """Partitions a list of objects by cumulative size

    :param obj_list: a list of dict-like objects with a 'size' property
    :return: a list of lists, one for each partition.
    """
    threshold = 2 ** 31

    def group_reducer(acc, obj):
        curr_size, output = acc
        if curr_size + obj['size'] < threshold:
            output[-1].append(obj)
            return curr_size + obj['size'], output
        else:
            output.append([obj])
            return obj['size'], output

    return reduce(group_reducer, obj_list, (0, [[]]))[1]



def _pickle_method(m):
    """Make instance methods pickable

    See http://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma/1816969#1816969
    """
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Dataset:
    """Represents a collection of objects on S3.

    A Dataset can have zero, one or many filters, which are refined using the
    `where` method. The result of refining a Dataset is a Dataset itself, so
    it's possible to chain multiple `where` clauses together.

    The actual data retrieval is triggered by the `records` method, which returns
    a Spark RDD containing the list of records retrieved. To call `records`
    a SparkContext object must be provided.

    Usage example::

        bucket = 'test-bucket'
        schema = ['submission_date', 'doc_type', 'platform']

        records = Dataset(bucket, schema) \\
            .where(doc_type='main') \\
            .where(submission_date=lambda x: x.startswith('201607')) \\
            .where(dim1='linux') \\
            .records(sc)

    For convenience Dataset objects can be created using the factory method
    `from_source`, that takes a source name (e.g. 'telemetry') and returns a
    new Dataset instance. The instance created will we aware of the list of
    dimensions, available on its `schema` attribute for inspection.
    """

    def __init__(self, bucket, schema, store=None,
        prefix=None, clauses=None):
        """Initialize a Dataset provided bucket and schema

        :param bucket: bucket name
        :param schema: a list of fields describing the structure of the dataset
        :param store: an instance of S3Store, potentially reused among several
        datasets
        :param prefix: a prefix to the
        :param clauses: mapping of fields -> callables to refine the dataset
        """
        self.bucket = bucket
        self.schema = schema
        self.prefix = prefix or ''
        self.clauses = clauses or {}
        self.store = store or S3Store(self.bucket)

    def __repr__(self):
        return ('Dataset(bucket=%s, schema=%s, store=%s, prefix=%s, clauses=%s)'
                ) % (self.bucket, self.schema, self.store, self.prefix, self.clauses)

    def where(self, **kwargs):
        """Return a new Dataset refined using the given condition

        :param kwargs: a map of `dimension` => `condition` to filter the elements
            of the dataset. `condition` can either be an exact value or a
            callable returning a boolean value.
        """
        clauses = copy(self.clauses)
        for dimension, condition in kwargs.items():
            if dimension in self.clauses:
                raise Exception('There should be only one clause for {}'.format(dimension))
            if dimension not in self.schema:
                raise Exception('The dimension {} doesn\'t exist'.format(dimension))
            if not hasattr(condition, '__call__'):
                clauses[dimension] = lambda x: x == condition
            else:
                clauses[dimension] = condition
            return Dataset(self.bucket, self.schema, store=self.store,
                           prefix=self.prefix, clauses=clauses)

    def _scan(self, dimensions, prefixes, clauses, executor):
        if not dimensions or not clauses:
            return prefixes
        else:
            dimension = dimensions[0]
            clause = clauses.get(dimension)
            matched = executor.map(self.store.list_folders, prefixes)
            # Using chain to flatten the results of map
            matched = chain(*matched)
            if clause:
                matched = [x for x in matched if clause(x.strip('/').split('/')[-1])]
                del clauses[dimension]

            return self._scan(dimensions[1:], matched, clauses, executor)

    def _summaries(self, limit=None):
        clauses = copy(self.clauses)
        schema = self.schema

        if self.prefix:
            schema = ['prefix'] + schema
            clauses['prefix'] = lambda x: x == self.prefix

        with futures.ProcessPoolExecutor(MAX_CONCURRENCY) as executor:
            scanned = self._scan(schema, [self.prefix], clauses, executor)
            keys = executor.map(self.store.list_keys, scanned)
        # Using chain to keep the list of keys as a generator
        keys = chain(*keys)
        return islice(keys, limit) if limit else keys

    def records(self, sc, limit=None, sample=1, decode=None):
        """Retrieve the elements of a Dataset

        :param sc: a SparkContext object
        :param limit: maximum number of objects to retrieve
        :param decode: an optional transformation to apply to the objects retrieved
        :param sample: percentage of results to return. Useful to return a sample
            of the dataset. This parameter is ignored when `limit` is set.
        :return: a Spark rdd containing the elements retrieved

        """
        summaries = self._summaries(limit)

        # Calculate the sample if summaries is not empty and limit is not set
        if summaries and limit is None and sample != 1:
            if sample < 0 or sample > 1:
                raise ValueError('sample must be between 0 and 1')
            summaries = list(summaries)
            summaries = random.sample(summaries,
                                      int(len(summaries) * sample))

        groups = _group_by_size(summaries)

        if decode is None:
            decode = heka_message_parser.parse_heka_message

        return sc.parallelize(groups, len(groups)) \
            .flatMap(lambda x:x) \
            .map(lambda x: self.store.get_key(x['key'])) \
            .flatMap(lambda x: decode(x))

    @staticmethod
    def from_source(source_name):
        """Create a Dataset configured for the given source_name

        This is particularly convenient when the user doesn't know
        the list of dimensions or the bucket name, but only the source name.

        Usage example::

            records = Dataset.from_source('telemetry) \\
                .where(doc_type='main') \\
                .where(submission_date='20160701')
        """
        meta_bucket = 'net-mozaws-prod-us-west-2-pipeline-metadata'
        store = S3Store(meta_bucket)

        try:
            source = json.loads(store.get_key('sources.json').read())[source_name]
        except KeyError:
            raise Exception('Unknown source {}'.format(source_name))

        schema = store.get_key('{}/schema.json'.format(source['prefix'])).read()
        dimensions = [f['field_name'] for f in json.loads(schema)['dimensions']]
        return Dataset(source['bucket'], dimensions, prefix=source['prefix'])
