import importlib
import os


def scan(root='.', exclusions=None):
    ''' root = directory tree root '''
    exclusions = exclusions or []
    exclusions = ['/'.join((root, val)) for val in exclusions]
    print exclusions
    for dir_name, subdir_list, file_list in os.walk(root):
        print 'dir=', dir_name
        # if dir_name in exclusions:
        #     continue
        for exc in exclusions:
            if 'scripts' in dir_name:
                print 'FIZZ: ', dir_name.startswith(exc)
            if dir_name.startswith(exc):
                continue
        check = (
            dir_name.startswith('./env') or
            dir_name.startswith('./.git') or
            '__init__.py' not in file_list
        )
        if check:
            continue
        for file_name in file_list:
            if not file_name.endswith('.py'):
                continue
            print 'in', dir_name, file_name
            if '__init__' in file_name:
                path = dir_name
                path = path[2:]
            else:
                path = '/'.join([dir_name, file_name])
                path = path[2:-3]  # trim ./ off front and .py off end
            path = path.replace('/', '.')
            importlib.import_module(path)

scan(exclusions=['scripts'])
