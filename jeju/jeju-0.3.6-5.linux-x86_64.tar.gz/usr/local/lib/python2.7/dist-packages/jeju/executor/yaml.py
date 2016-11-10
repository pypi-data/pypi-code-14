###########################################
# This is very naive replacement algorithm
# TODO
############################################
import string
import uuid
import logging

import jeju.do

exist_ruamel = True

try:
    import ruamel.yaml
    from ruamel.yaml.util import load_yaml_guess_indent
except ImportError:
    err_msg = """
    ##################################################################
    # ! Warning                                                      #
    # rumal.yaml library does not exist                              #
    # jeju *can not* execute yaml plugin!                            #
    #                                                                #
    # To install ruamel.yaml                                         #
    # (RedHat, CentOS)                                               #
    # yum install python-devel gcc                                   #
    # pip install ruamel.yaml                                        #
    #                                                                #
    # (Debian, Ubuntu)                                               #
    # apt-get install python-dev gcc                                 #
    # pip install ruamel.yaml                                        #
    ##################################################################
    """
    print err_msg
    import time
    time.sleep(5)
    exist_ruamel = False

def replaceable(code, kv):
    # change keyword to value
    keys = kv.keys()
    # find keyword which is ${keyword}
    # replace value ${keyword} <- kv[keyword]
    for key in keys:
        nkey = "${%s}" % key
        code = string.replace(code, nkey, kv[key])
    logging.debug("#" * 20 + "\n%s" % code)
    logging.debug("#" * 20)
 
    return code

def find_file_path(lookahead):
    print lookahead
    if lookahead == None:
        return None
    ctx = lookahead['text']
    items = ctx.split()
    if items[0] == 'edit':
        return items[1]

def execute_yaml(**kwargs):
    code = kwargs['code']
    kv = kwargs['kv']

    import os
    # call replaceable
    rcode = replaceable(code, kv)

    file_path = find_file_path(kwargs['lookahead'])
    if file_path == None:
        msg = "[DEBUG] I don't know how to edit!"
        print msg
        return msg

    ####################################
    # Warning: We install ruamel.yaml
    ####################################
    if exist_ruamel == False:
        logging.error(err_msg)
        distro = jeju.do.detect_dist()
        os_ = distro['distname'].split(' ')[0].lower()
        if os_ == "ubuntu" or os_ == "debian":
            cmd = "apt-get update;apt-get install -y gcc python-dev;pip install ruamel.yaml"
        elif os_ == "centos" or os_ == "redhat":
            cmd = "yum install -y python-devel gcc;pip install ruamel.yaml"
        else:
            return {'input':rcode, 'output':'[ERROR] Install ruamel.yaml'}

        import os
        os.system(cmd)

    # redundant
    import ruamel.yaml
    from ruamel.yaml.util import load_yaml_guess_indent

    config, ind, bsi = load_yaml_guess_indent(open(file_path))
    config2, ind2, bsi2 = load_yaml_guess_indent(rcode)

    # Overwrite config2 to config
    config.update(config2)

    ruamel.yaml.round_trip_dump(config, open(file_path, 'w'), indent=ind, block_seq_indent=bsi)
    return {'input': rcode, 'output':open(file_path,'r').read()}

