#!/usr/bin/env python
import os
import sys
import jinja2
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from tempfile import NamedTemporaryFile
from optparse import OptionParser
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.playbook.play import Play
import nmap
import configobj
import re 


class Boot(object):

    options = namedtuple('Options', ['listtags', 
        'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 
        'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 
        'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 
        'become_user', 'verbosity', 'check'])

    def __init__(self,working_dir):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.nm = nmap.PortScanner()
        self.hosts = []
        self.temp_hosts_file = ""
        self.inventory = """
                    [DYNAMIC]
                    {{ host_list }}
                    """
    
        os.chdir(working_dir)
        self.con = configobj.ConfigObj('ansible.cfg')

    def scan(self,range):
        self.nm.scan(range,arguments=self.con['defaults']['scan_args'])
        self.hosts = self.nm.all_hosts()
        if not self.hosts:
            print("No hosts found")
            sys.exit(1)

        inventory_template = jinja2.Template(self.inventory)
        rendered_inventory = inventory_template.render({
            'host_list': "\n".join(self.hosts),
            })

        hosts = NamedTemporaryFile(delete=False)
        self.temp_hosts_file = hosts
        hosts.write(rendered_inventory)
        hosts.close()
        self.inventory = Inventory(loader=self.loader, 
                variable_manager=self.variable_manager,  
                host_list=hosts.name)

        print(self.con['defaults']['syntax'])
        #There are many more options that could be added here
        self.options = Boot.options(listtags=False, listtasks=False, listhosts=False, 
                syntax=self.con.get('defaults').as_bool('syntax'), 
                connection='ssh', module_path=None, forks=100, 
                remote_user=self.con['defaults']['remote_user'],
                private_key_file=self.con['defaults']['private_key_file'],
                ssh_common_args=None, 
                ssh_extra_args=None, sftp_extra_args=None, 
                scp_extra_args=None, 
                become=True, become_method=None, 
                become_user=self.con['defaults']
                ['become_user'], 
                verbosity=3, 
                check=False)

        self.passwords = {}

    def execute_module(self,module_name, module_args):
        play_source = dict(
                name = "Ansible play",
                hosts = "DYNAMIC",
                gather_facts = "no",
                tasks = [
                    dict(action=dict(module=module_name, args=module_args),
                        register="shell_out")
                        ]
                )
        play = Play().load(play_source, variable_manager=self.variable_manager,
                loader=self.loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                    inventory = self.inventory,
                    variable_manager = self.variable_manager,
                    loader = self.loader,
                    options = self.options,
                    passwords = self.passwords)
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def execute_boot(self,playbook_path,args):        
        playbook_path = playbook_path
        if not os.path.exists(playbook_path):
            print('The playbook does not exist')
            sys.exit(1)
        
        default_vars = {'hosts': 'DYNAMIC'} 
        
        if args:
            regex = re.compile(r"\b(\w+)\s*=\s*([^=]*)(?=\s+\w+\s*:|$)")
            d = dict(regex.findall(args))
            print("Passing through extra vars: " + str(d))
            default_vars.update(d)
            
        self.variable_manager.extra_vars = default_vars 

        pbex = PlaybookExecutor(playbooks=[playbook_path], 
                inventory=self.inventory, 
                variable_manager=self.variable_manager, 
                loader=self.loader, options=self.options, passwords=self.passwords)

        results = pbex.run()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-m","--module",
            help="Name of ansible module to run")
    parser.add_option("-a","--args",
            help ="Argument of module running")
    parser.add_option("-r","--range",
            help ="an nmap friendly host range to scan e.g. 127.0.0.1-100")
    parser.add_option("-n","--name",
            help="name of the playbook to run e.g. boot.yml")
    parser.add_option("-o","--output",
            help="Output the range of discovered hosts to a file")
    parser.add_option("-w","--workingdir",
            help="working dir with ansible.cfg in the root")
    (options,args) = parser.parse_args()

    if not options.workingdir:
        print("Requires working directory set")
        sys.exit(1)

    b = Boot(options.workingdir)

    if options.range:
        b.scan(options.range)
    else:
        print("Requires --range of hosts in nmap format e.g. 10.0.0.1-100")
        sys.exit(1)
    
    if options.output:
        f = b.temp_hosts_file
        print(f)
        sys.exit(0)
    
    if options.module:
        b.execute_module(options.module, options.args)
    else:
        if options.name: 
            b.execute_boot(options.name,options.args)
        else:
            print("Cannot run without a playbook")
            sys.exit(1)
