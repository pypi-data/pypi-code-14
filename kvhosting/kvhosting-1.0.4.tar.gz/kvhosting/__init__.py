"""
The Riak API for Python allows you to connect to a Riak instance,
create, modify, and delete Riak objects, add and remove links from
Riak objects, run Javascript (and Erlang) based Map/Reduce
operations, and run Linkwalking operations.
"""

from kvhosting.riak_error import RiakError, ConflictError
from kvhosting.client import RiakClient
from kvhosting.bucket import RiakBucket, BucketType
from kvhosting.table import Table
from kvhosting.node import RiakNode
from kvhosting.riak_object import RiakObject
from kvhosting.mapreduce import RiakKeyFilter, RiakMapReduce, RiakLink


__all__ = ['RiakBucket', 'Table', 'BucketType', 'RiakNode',
           'RiakObject', 'RiakClient', 'RiakMapReduce', 'RiakKeyFilter',
           'RiakLink', 'RiakError', 'ConflictError',
           'ONE', 'ALL', 'QUORUM', 'key_filter']

ONE = "one"
ALL = "all"
QUORUM = "quorum"

key_filter = RiakKeyFilter()
