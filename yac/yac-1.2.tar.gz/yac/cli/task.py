#!/usr/bin/env python

import argparse, os, inspect, jmespath, json
from colorama import Fore, Style
from yac.lib.service import get_service, get_service_parmeters, get_service_alias
from yac.lib.stack import get_stack_templates, get_stack_name, get_ec2_ips, deploy_stack_files
from yac.lib.naming import set_namer
from yac.lib.task import get_task, get_task_names, run_task
from yac.lib.params import get_service_params, NULL_PARAMS, INVALID_PARAMS
from yac.lib.vpc import get_vpc_prefs 
from yac.lib.variables import get_variable,set_variable

def main():

    parser = argparse.ArgumentParser(description='Run a task per the task defintions in the provided Servicefile')

    # required args                                         
    parser.add_argument('servicefile', help='location of the Servicefile (registry key or abspath)')
    parser.add_argument('-n','--name', help='name of task to run') 

    parser.add_argument('-p',
                        '--params',  help='path to a file containing additional, static, service parameters (e.g. vpc params, of service constants)') 
    parser.add_argument('-a',
                        '--alias',  help='service alias for the stack currently supporting this service (deault alias is per Servicefile)')
    parser.add_argument('-s',
                        '--show',  help='show all tasks associated with this a service',
                                   action='store_true')      
    parser.add_argument('--public',     help='connect using public IP address', 
                                        action='store_true')     

    args = parser.parse_args()

     # determine service defintion, complete service name, and service alias based on the args
    service_descriptor, service_name, servicefile_path = get_service(args.servicefile) 

    # abort if service_descriptor was not loaded successfully
    if not service_descriptor:
        print("The Servicefile input does not exist locally or in registry. Please try again.")
        exit()

    # get vpc preferences in place
    vpc_prefs = get_vpc_prefs()

    # set the resource namer to use with this service
    set_namer(service_descriptor, servicefile_path, vpc_prefs)

    # get the alias to use with this service
    service_alias = get_service_alias(service_descriptor,args.alias)

    # determine service params based on the params arg
    service_params_input, service_params_name = get_service_params(args.params)

    # abort if service params were not loaded successfully
    if args.params and service_params_name == NULL_PARAMS:
        print("The service params specified do not exist locally or in registry. Please try again.")
        exit()
    elif service_params_name == INVALID_PARAMS:
        print("The service params file specified failed validation checks. Please try again.")
        exit()
        
    # get the service parameters for use with yac-ref's in service templates
    service_parmeters = get_service_parmeters(service_alias, service_params_input, 
                                              service_name, service_descriptor,
                                              servicefile_path, vpc_prefs)

    # get cloud formation template for the service requested and apply yac intrinsic 
    # functions (yac-ref, etc.) using  the service_parmeters
    stack_template = get_stack_templates(service_descriptor,  
                                         service_parmeters)

    if args.show:

        print(Fore.GREEN)

        tasks = get_variable(service_parmeters,"tasks",{})

        if tasks:
            print "Available Tasks:"
            
            for task_name in tasks.keys():
                print "%s: %s"%(task_name,tasks[task_name]['comment'])
        else:
            print "There are no tasks associated with this service"

        print(Style.RESET_ALL)                

    elif args.name:

        # get the task params
        task_def = get_task(args.name, service_descriptor)

        if not task_def:

            task_names = get_task_names(service_parmeters)

            print("The task requested doesn't exist in the Servicefile. " +
                  "Available tasks include:\n%s."%pp_list(task_names))
            exit()

        print(Fore.GREEN)

        # run the requested task
        run_task(args.name,service_parmeters,stack_template)

        print(Style.RESET_ALL)

    else:

        print(Fore.RED)

        print("Nothing to do. Show available tasks using the --show argument or specify a task to run using the --name argument.")

        print(Style.RESET_ALL)        



def pp_list(list):
    str = ""
    for item in list:
        str = str + '* %s\n'%item

    return str