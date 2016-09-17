"""
yaml_testbed is a module to set up (initiate) a test bed described in a yaml file.

There are two level of yaml files for a test bed definition: Index file and Object file
    The Index file is to describe an existing test bed, in which there are different components,
    while the object file is to define the objects to be used in a test suite

    e.g. :
    The index file: feature_test_bed_Steven.yaml
        gateway17:  # a gateway machine in the test environment
            mgmtip: 10.74.124.17
            user: root
            password: rootpw

        client18:   # a Linux client in a test environment
            mgmtip: 10.74.124.18
            user: root
            password: rootpw

        cluster-a:  # a storage cluster to be access (using predefined user/account)
            auth_fqdn: auth06.cluster.com
            storage_fqdn: auth06.cluster.com

        cluster-b:  # a storage cluster to be access (using predefined user/account)
            auth_fqdn: auth08.cluster.com
            storage_fqdn: auth08.cluster.com

    The Object file:   basic_write_read_test.yaml
        testbed_conf: feature_test_bed_Steven.yaml    # the index file of the test bed to be used.
        fsg_node:   # the object name
            class: lib.fsgwserver.FsgwServer    # the class name to initiate the object
            name: [gateway17]                   # map to the name in the index file
        nfs_client:
            class: lib.nfsclient.NfsClient
            name: [client18]
        smb_client:
            class: lib.smbclient.SmbClient
            name: [client18]
        cos_cluster:
            class: lib.coscluster.CosCluster
            name: [cluster-a]

In this module, a method is provided to initiate the test bed based on the object yaml file.
    All objects (components under test) are in this module's name space.
"""

import yaml
import os

class FileTypeError(TypeError):
    """TestBed file type error exception."""

def init_yaml_testbed(filename):
    with open(filename, encoding='utf-8') as f:
        object_dict = yaml.load(f)

    index_dict = {}
    ### See if the testbed_conf is defined in this object file
    if 'testbed_conf' in object_dict:
        index_files = object_dict['testbed_conf']
        del object_dict['testbed_conf']
        # The index_file could be a list of a file name.
        ## If it is not a list, change it to a list.
        if isinstance(index_files, str):
            index_files = [index_files]

        # load index dictionary
        for index_file in index_files:
            with open(index_file, encoding='utf-8') as f:
                index_dict.update(yaml.load(f))

    for tb_object in object_dict.keys():
        attr_dict = object_dict[tb_object]
        class_name = attr_dict['class']
        original_name = attr_dict['name']

    ### Todo: Not completed.


def init_testbed(filename, namespace=None):
    basename, ext = os.path.splitext(filename)
    if ext == '' or ext == '.py':
        import importlib
        return importlib.import_module(basename)
    elif ext == 'yaml':
        return init_yaml_testbed(filename)
    else:
        raise FileTypeError("{1} is not a valid test bed file type, only .py and .yaml supported".format(filename))





