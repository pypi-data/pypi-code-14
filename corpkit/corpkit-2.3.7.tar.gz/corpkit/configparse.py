"""
corpkit: save and load config file for project
"""

def conmap(cnfg, section):
    """
    Helper for load settings
    """
    dct = {}
    options = cnfg.options(section)
    # todo: this loops over too many times
    for option in options:
        opt = cnfg.get(section, option)
        if opt == '0':
            opt = False
        elif opt == '1':
            opt = True
        elif opt.isdigit():
            opt = int(opt)
        elif all(i.isdigit() or i == '.' for i in opt):
            opt = float(opt)
        if isinstance(opt, str) and opt.lower() == 'none':
            opt = False
        if not opt:
            opt = False
        dct[option] = opt
    return dct

def load_config(f):
    """
    Parse a config file and return a dict of kwargs
    """
    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser

    Config = configparser.ConfigParser()
    Config.read(f)
    dct = {}
    return dct

def save_config(dct, f):
    """
    Turn dict of options and values into config file at path f
    """

    try:
        import configparser
    except ImportError:
        import ConfigParser as configparser

    Config = configparser.ConfigParser()

    Config.add_section('Build')
    
    Config.set('Interrogate','Multiprocess',\
               dct.get('multiprocess', False))
    Config.add_section('Interrogate')

    Config.set('Interrogate','Multiprocess',\
               dct.get('multiprocess', False))
    
    Config.add_section('Visualise')
    Config.add_section('Concordance')
    Config.add_section('Manage')

    with open(f, 'w') as cfgfile:
        Config.write(cfgfile)

    return