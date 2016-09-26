from subprocess import Popen, PIPE, STDOUT

class PBS():
    def __init__(self, object):
        self.object = object
        self.pbs_commands = []
        self.commands = []

        if 'pbs_commands' in self.object:
            for command in self.object['pbs_commands']:
                self.add_pbs_command(command)

        self.prepare()

    def add_pbs_command(self, command):
        """
        Adds a PBS command
        :param command: The command without "#PBS "
        """
        self.pbs_commands.append('#PBS ' + command)

    def prepare_shell(self):
        """
        Prepares the shell part
        """
        if 'shell' in self.object:
            self.add_pbs_command('-S %s' % self.object['shell'])

    def prepare_nodes_processes(self):
        """
        Prepares the nodes and number of processes part of PBS commands
        """
        if 'processes' in self.object and 'nodes' not in self.object:
            self.add_pbs_command('-l procs=%d' % self.object['processes'])
        elif 'nodes' in self.object:
            if 'processes' in self.object and 'process_per_node' not in self.object:
                ppn = self.object['processes'] / self.object['nodes']
            elif 'process_per_node' in self.object:
                ppn = self.object['process_per_node']

            if 'ppn' in locals():
                self.add_pbs_command(
                    '-l nodes=%d:ppn=%d' %
                    (self.object['nodes'], ppn)
                )

    def prepare_memory(self):
        """
        Prepares memory limits
        """
        if 'memory' in self.object:
            self.add_pbs_command('-l mem=%s' % self.object['memory'])

        if 'memory_per_process' in self.object:
            self.add_pbs_command('-l pmem=%s' % self.object['memory_per_process'])

    def prepare_modules(self):
        if 'modules' in self.object:
            if '-' in self.object['modules']:
                self.commands.append('module purge')

            for module in self.object['modules']:
                if module != '-':
                    self.commands.append('module load %s' % module)

    def prepare_commands(self):
        if 'commands' in self.object:
            for command in self.object['commands']:
                self.commands.append(command)

    def prepare(self):
        """
        Prepares the script
        """
        self.prepare_shell()
        self.prepare_nodes_processes()
        self.prepare_memory()
        self.prepare_modules()
        self.commands.append('')
        self.commands.append('# Commands')
        self.prepare_commands()
        self.commands.append('')

    def get_string(self):
        # Make the PBS commands part
        """
        Makes the PBS script and returns it
        :return: The PBS script
        """
        string = '\n'.join(self.pbs_commands)

        if string != '':
            string += '\n\n'

        string += '\n'.join(self.commands)

        print string

        return string

    def submit(self):
        p = Popen(['qsub'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        grep_stdout = p.communicate(input=self.get_string())[0]
        p.stdin.close()

        return grep_stdout

    def __str__(self):
        return self.get_string()
