#!/usr/bin/env python
import zmq
import logging

import socket

def get_ip_address():
 return socket.gethostname()


if __name__ == '__main__':
    #                         
    # |  _   _   _  o ._   _  
    # | (_) (_| (_| | | | (_| 
    #        _|  _|        _| 
    #        
    logging.basicConfig(filename='zezfio.log', level=logging.ERROR)

    #  _             
    # |_) _. _|_ |_  
    # |  (_|  |_ | | 
    #
    import sys, os
    address, path_config, db_path_rel = sys.argv[1:]
    db_path = os.path.abspath(db_path_rel)

    #                                     _       
    # |_|  _. ._   _| |  _     _  _  ._ _|_ o  _  
    # | | (_| | | (_| | (/_   (_ (_) | | |  | (_| 
    #                                          _|
    from zezfio import generator
    d_instance = generator.get_dict_module_server(path_config,db_path)

    #  __                 
    # (_   _  ._    _  ._ 
    # __) (/_ | \/ (/_ |  
    #
    context = zmq.Context(io_threads=4)
    sock = context.socket(zmq.REP)

    #IPC Adress
    sock.bind(address)

    #Random tcp
    tcp_port_selected = sock.bind_to_random_port('tcp://*', min_port=6001, max_port=6004, max_tries=100)
    # ~#~#~#~#
    # Little_optimisation
    # ~#~#~#~#
    send = sock.send
    recv = sock.recv

    # ~#~#~#~#
    # Error_code
    # ~#~#~#~#    
    from ctypes import c_int
    errno_fail = c_int(-1)
    errno_success = c_int(0)

    while True:
            #For the sake of performance, inline the main loop
            #Get the info
            try:
                m = recv()
            except zmq.error.ZMQError:
                logging.exception("Error when asking for a message")
                continue

            if m == "get_tcp":
                send("tcp://%s:%s" %(get_ip_address(),tcp_port_selected))
                continue

            try:
                action, str_instance, name = m.split(".")
            except:
                logging.exception("Error when splitting the message %s"%m)
                continue

            try:
                instance = d_instance[str_instance]
            except Exception as e:
                logging.exception("Cannot get the %s category" % str_instance)
                send(errno_fail)
                continue

            #Get the instance
            if action == "has":

                try:
                    getattr(instance,"%s_interface" % name)
                except Exception as e:
                    logging.exception(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success)
                    logging.debug("Is Present")

            elif action == "size":

                try:
                    size = getattr(instance, "%s_len_interface" % name)
                except Exception as e:
                    logging.error(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success,  zmq.SNDMORE)
                    send(size)
                    logging.debug("Size send")

            elif action == "get":
                try:
                    size = getattr(instance, "%s_len_interface" % name)
                    array = getattr(instance, "%s_interface" % name)
                except Exception as e:
                    logging.exception(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success,  zmq.SNDMORE)
                    send(size, zmq.SNDMORE)               
                    send(array)

            elif action == "set":
                try:
                    bytes = recv()
                except zmq.error.ZMQError:
                    logging.exception("Error when reading the number of bytes in set")
                    continue

                try:
                    getattr(instance, "set_%s" % name)(bytes)
                except Exception as e:
                    logging.exception(e)
                    send(errno_fail)
                    continue
                else:
                    errno_success = d_instance["zezfio_id"]
                    send(errno_success)
                    logging.debug("Set Done. Errno is %s" % errno_success.value)

            elif action == "get_ascii":
                try:
                    array = getattr(instance, "%s_ascii" % name)
                except Exception as e:
                    logging.exception(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success,  zmq.SNDMORE)            
                    send(array)

            elif action == "set_ascii":
                try:
                    string = recv()
                except zmq.error.ZMQError:
                    logging.exception("Error when reading the number of string in set")
                    continue

                try:
                    getattr(instance, "set_ascii_%s" % name)(string)
                except Exception as e:
                    logging.exception(e)
                    send(errno_fail)
                    continue
                else:
                    errno_success = d_instance["zezfio_id"]
                    send(errno_success)
                    logging.debug("Set Done. Errno is %s" % errno_success.value)

            else:
                logging.error("Cannot understand the action to do %s"%action)
                continue
