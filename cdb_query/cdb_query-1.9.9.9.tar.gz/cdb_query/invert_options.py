#Internal:
from . import parsers
from . import commands_parser

def invert_options(prog, options):
    commands_list = commands_parser._get_command_names(options)
    args_list = [prog, options.project] + commands_list

    for name in dir(options):
        if isinstance(getattr(options,name),bool):
            options_new, project_drs = parsers.full_parser(args_list + ['-'+name], raise_error=False)
        else:
            if isinstance(getattr(options,name),list):
                opt_list = ','.join(getattr(options,name))
            else:
                opt_list = getattr(options,name)
            options_new, project_drs = parsers.full_parser(args_list + ['--'+name+'='+opt_list], raise_error=False)
        print(name)
    return
    
