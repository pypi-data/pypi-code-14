import voltron
from voltron.plugin import CommandPlugin, VoltronCommand

var_storage = {}


class VarCommand(VoltronCommand):
    def invoke(self, *args):
        global var_storage
        if len(args) == 0:
            print(var_storage)
        elif len(args) == 1:
            print(var_storage[args[0]])
        elif len(args) == 2 or len(args) == 3 and args[1] == '=':
            var_storage[args[0]] = args[-1]


class VarCommandPlugin(CommandPlugin):
    name = 'var'
    command_class = VarCommand
