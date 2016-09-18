import sys
import itertools
import pkgutil


__version__ = '1.0.0'


class DoError(Exception):
    pass


def do_main(package=None):
    if package is None:
        package = sys.modules[__package__]

    args = sys.argv[1:]
    try:
        _do(package, args)
    except DoError as e:
        print(
            'Sorry! Unknonwn command "%s" in "%s"' %
            (str(e), ' '.join(args)),
            file=sys.stderr  # noqa
        )


def _do(package, args):
    modules = _modules(package)

    command_path = list(itertools.takewhile(lambda name: name.isalnum(), args))
    params = list(itertools.takewhile(lambda name: name.startswith('-'), args[1:]))

    if not command_path:
        command = '?'
        module = package
    else:
        command = command_path[0]
        module = modules.get(command)

    if not module:
        raise DoError(command)
    elif hasattr(module, 'do'):
        try:
            if params:
                module.do(params)
            else:
                module.do()
        except TypeError as e:
            if 'positional' in str(e):
                raise DoError(params)
    elif args:
        _do(module, args[1 + len(params):])
    else:
        _usage(package, module, modules, args)


def _modules(module):
    try:
        path = module.__path__
    except AttributeError:
        # not a package, no subcommands
        return {}

    package = sys.modules[module.__package__]
    prefix = module.__name__ + '.'
    moduleinfo = list(
        pkgutil.walk_packages(
            path=path,
            prefix='',
            onerror=lambda x: None
        )
    )

    modules = {}
    for importer, name, ispkg in moduleinfo:
        # no special modules
        if not name:
            continue
        if '._' in name:
            continue
        if name.startswith('_') or name.endswith('_'):
            continue

        subname = name.replace(prefix, '')
        if not subname or len(subname.split('.')) > 1:
            continue
        subname = subname.lstrip('.')
        if name in sys.modules:
            modules[subname] = sys.modules[name]
        else:
            import_name = prefix + name
            modules[subname] = __import__(import_name, fromlist=[package.__name__])

    return modules


def _usage(package, module, modules, args):
    version = ''
    if hasattr(package, '__version__'):
        version = 'v' + package.__version__

    doc = package.__doc__.strip() if package.__doc__ else ''
    print(package.__name__, version, doc, file=sys.stderr)  # noqa
    print()

    prefix = module.__name__.replace('.', ' ') + ' '
    for subcommand, m in sorted(modules.items()):
        if '.' in subcommand:
            continue

        doc = m.__doc__.strip() if m.__doc__ else ''
        more = ' ...' if hasattr(m, '__path__') else ''
        print('    %-20s\t%s' % (prefix + subcommand + more, doc), file=sys.stderr)
