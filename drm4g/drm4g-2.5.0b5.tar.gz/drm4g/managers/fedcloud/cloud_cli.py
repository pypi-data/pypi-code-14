#!/usr/bin/env python

import os
import pickle
import logging
#import argparse
import threading
from os.path import exists, join
from drm4g          import DRM4G_DIR, REMOTE_VOS_DIR, RESOURCE_MANAGERS
from drm4g.core.configure     import Configuration
from drm4g.utils.importlib    import import_module

logger = logging.getLogger(__name__)

#cluster_cfg = join(DRM4G_DIR, "etc", "cluster.conf")
cloudsetup = join(DRM4G_DIR, "etc", "cloudsetup.json")
pickled_file = join(DRM4G_DIR, "var", "fedcloud_pickled")

lock = threading.RLock()
# if exists( cluster_cfg ) :
#     from fedcloud import ClusterBasicData
#     cluster_ip = os.environ.get( "IP_FILE" )
#     if not cluster_ip :
#         exit( "Please define a file to store the VM's IP directions" )
#     cluster_basic_data = ClusterBasicData( pickled_file, cluster_cfg, cloudsetup )

'''
configure = Configuration()
        
if configure.check_update() or not configure.resources :
    configure.load()
    errors = configure.check()
    if errors :
        logger.error ( ' '.join( errors ) )
        raise Exception ( ' '.join( errors ) )
'''

def start_instance( instance, resource_name ) :
    try:
        #logger.error( "Running cloud_cli's start_instance function" )
        instance.create()
        instance.get_ip()
        '''
        resource_elem = {}
        resource_elem["enable"] = config["enable"]
        resource_elem["communicator"] = config["communicator"]
        resource_elem["username"] = instance.vo_user
        resource_elem["frontend"] = instance.ext_ip
        #resource_elem["lrms"] = config["lrms"] #if its added, the stop won't work well
        resource_elem["vo"] = instance.vo
        resource_elem["myproxy_server"] = config["myproxy_server"]
        resource_elem["endpoint"] = instance.endpoint
        resource_elem["flavour"] = instance.flavour
        resource_elem["virtual_image"] = config['virtual_image'] #or instance.app (instance.app_name = config['virtual_image'] = basic_data['virtual_image'] = 'Ubuntu-14.04')
        #resource_elem["instance"] = "NO IDEA" #instance.app??
        resource_elem["bdii"] = config['bdii']
        resource_elem["volume"] = instance.volume
        ''
        configure.resources[str(instance.int_ip)]=resource_elem
        ''
        #conf.resources[resource_name+'::'+instance.int_ip]=resource_elem #maybe I should use the public ip
        resource_dict[resource_name+'::'+instance.int_ip]=resource_elem #maybe I should use the public ip
        logger.error( "resource_dict:\n"+str(resource_dict) )
        '''
    except Exception as err :
        logger.error( "\nError creating instance: %s" % str( err ) )
        logger.error( "\n"+err )
        #logger.error( "Ending  cloud_cli's start_instance function with an error" )
        try :
            logger.info( "Trying to destroy the instance" )
            instance.delete( )
        except Exception as err :
            logger.error( "Error destroying instance: %s" % str( err ) )  
    else :
        with lock:     
            # with open( cluster_ip, "a") as ipf :
            #     ipf.write( instance.ext_ip )  
            #     ipf.write( "\n" )
            try:
                with open( pickled_file+"_"+resource_name, "a" ) as pf :
                    pickle.dump( instance, pf )
            except Exception:
                try :
                    logger.info( "Trying to destroy the instance" )
                    instance.delete( )
                except Exception as err :
                    logger.error( "Error destroying instance: %s" % str( err ) ) 
        #logger.error( "Ending  cloud_cli's start_instance function" )

def stop_instance( instance ):
    try :
        #logger.error( "Running cloud_cli's stop_instance function" )
        '''private_ip = instance.int_ip #maybe I should use the public ip'''
        instance.delete()
    except Exception as err :
        logger.error( "Error destroying instance: %s" % str( err ) )
        #logger.error( "Ending  cloud_cli's stop_instance function with an error" )
    '''
    else:
        logger.error( "resource_dict:\n"+str(resource_dict) )
        del resource_dict[resource_name+'::'+private_ip]
        #logger.error( "Ending  cloud_cli's stop_instance function" )
    '''

'''
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "--action", choices = [ "start", "stop" ], help = "Action to execute" )
    args = parser.parse_args()
'''
def main(args, resource_name, config):
    #if args.action == "start" :
    #logger.error( "Running cloud_cli's main function" )
    if args == "start" :
        #if exists( cluster_ip ) :
        #    os.remove( cluster_ip )
        if exists( pickled_file+"_"+resource_name ) :
            os.remove( pickled_file+"_"+resource_name )
        try :
            #hdpackage =  __import__( "fedcloud.%s" % cluster_basic_data.cluster_setup.infrastructure )
            #hdpackage =  __import__( "%s" % RESOURCE_MANAGERS[config['lrms']] )
            #hdpackage =  __import__( RESOURCE_MANAGERS[config['lrms']] + ".%s" % config['lrms'] )
            #hdpackage = import_module( "%s" % RESOURCE_MANAGERS[config['lrms']] )
            hdpackage = import_module( RESOURCE_MANAGERS[config['lrms']] + ".%s" % config['lrms'] )
        except Exception as err :
            raise Exception( "The infrastructure selected does not exist. "  + str( err ) )
        #context = eval( "hdpackage.%s.Contextualization( cluster_basic_data )" % cluster_basic_data.cluster_setup.infrastructure )
        #context.create()

        threads = [] 
        handlers = []
        #for number_of_th in range( cluster_basic_data.cluster_setup.nodes )  :
        for number_of_th in range( int(config['nodes']) ):
            #instance = eval( "hdpackage.%s.Instance( cluster_basic_data )" % cluster_basic_data.cluster_setup.infrastructure ) 
            #instance = eval( "hdpackage.%s.Instance( config )" % config['lrms'] )
            instance = eval( "hdpackage.Instance( config )" )
            th = threading.Thread( target = start_instance, args = ( instance, resource_name, ) ) 
            th.start()
            threads.append( th )
        [ th.join() for th in threads ]
    #elif args.action == "stop" :
    elif args == "stop" :
        instances = []
        if not exists( pickled_file+"_"+resource_name ):
            logger.error( "There are no available VM's to be deleted" )
            exit( 1 )
        with open( pickled_file+"_"+resource_name, "r" ) as pf :
            while True :
                try:
                    instances.append( pickle.load( pf ) )
                except EOFError :
                    break
        if not instances :
            logger.error( "For shutdown --init must be absent and pickle file must be present" )
            exit( 1 )
        threads = []
        for instance in instances :
            th = threading.Thread( target = stop_instance, args = ( instance, ) )
            th.start()
            threads.append( th )
        [ th.join() for th in threads ]
        os.remove( pickled_file+"_"+resource_name )
    else : 
        logger.error( "Invalid option" )
        #logger.error( "Ending  cloud_cli's main function" )
        exit( 1 )
    #logger.error( "Ending  cloud_cli's main function" )

if __name__ == "__main__" :
    main()

'''
#copied from cream.py
def _renew_voms_proxy(self):
    ###revisar esto
    if cluster_basic_data.cluster_setup.infrastructure is "fedcloud":
        vo=str(cluster_basic_data.cluster_setup.infrastructure)+".egi.eu"
    else:
        vo=str(cluster_basic_data.cluster_setup.infrastructure)
    #output = "The proxy 'x509up.%s' has probably expired" %  self.resfeatures[ 'vo' ]
    output = "The proxy 'x509up.%s' has probably expired" %  vo
    ##logger.error( output )
    #logger.error( output )
    #if 'myproxy_server' in self.resfeatures :
    if 'myproxy_server' in cluster_basic_data.cluster_setup.credentials:
        #LOCAL_X509_USER_PROXY = "X509_USER_PROXY=%s" % join ( REMOTE_VOS_DIR , self.resfeatures[ 'myproxy_server' ] )
        LOCAL_X509_USER_PROXY = "X509_USER_PROXY=%s" % join ( REMOTE_VOS_DIR , cluster_basic_data.cluster_setup.credentials[ 'myproxy_server' ] )
    else :
        LOCAL_X509_USER_PROXY = "X509_USER_PROXY=%s/${MYPROXY_SERVER}" % ( REMOTE_VOS_DIR )
    cmd = "%s voms-proxy-init -ignorewarn " \
    "-timeout 30 -valid 24:00 -q -voms %s -noregen -out %s --rfc" % (
        LOCAL_X509_USER_PROXY ,
        vo ,
        join( REMOTE_VOS_DIR , 'x509up.%s ' ) % vo )

    #logger.error( "Executing command: %s" % cmd )
    out, err = self.Communicator.execCommand( cmd )
    #logger.error( out + err )
    if err :
        output = "Error renewing the proxy(%s): %s" % ( cmd , err )
        logger.error( output )
'''
