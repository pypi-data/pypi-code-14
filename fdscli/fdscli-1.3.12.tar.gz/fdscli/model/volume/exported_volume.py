#
# Copyright 2016 Formation Data Systems, Inc. All Rights Reserved.
#
class ExportedVolume(object):
    '''Metadata for a volume exported to a bucket.

    Since the exported volume is serialized, a bucket read is required to get metadata.

    Attributes
    ----------
    __obj_prefix_key (str) : Uniquely identifies the exported volume in the bucket.
    __source_volume_name (str)
    __source_volume_type (str)
    __creation_time (long) : Creation time for the original, source volume
    __blob_count (int) : Blob count for the original, source volume
    '''

    def __init__(self, obj_prefix_key=None, source_volume_name=None,
        source_volume_type="OBJECT", creation_time=0, blob_count=0):

        self.__obj_prefix_key = obj_prefix_key
        self.__source_volume_name = source_volume_name
        self.__source_volume_type = source_volume_type
        self.__creation_time = creation_time
        self.__blob_count = blob_count

    @property
    def obj_prefix_key(self):
        return self.__obj_prefix_key

    @obj_prefix_key.setter
    def obj_prefix_key(self, obj_prefix_key):
        self.__obj_prefix_key = obj_prefix_key

    @property
    def source_volume_name(self):
        return self.__source_volume_name

    @source_volume_name.setter
    def source_volume_name(self, source_volume_name):
        self.__source_volume_name = source_volume_name

    @property
    def source_volume_type(self):
        return self.__source_volume_type

    @source_volume_type.setter
    def source_volume_type(self, source_volume_type):
        self.__source_volume_type = source_volume_type

    @property
    def creation_time(self):
        return self.__creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        self.__creation_time = creation_time

    @property
    def blob_count(self):
        return self.__blob_count

    @blob_count.setter
    def blob_count(self, blob_count):
        self.__blob_count = blob_count

