from grammaticomastix.globalvars import CFGFILEPARSER
import os.path

#///////////////////////////////////////////////////////////////////////////////
def possible_paths_to_cfg():
    """
        possible_paths_to_cfg()
        ________________________________________________________________________

        return a list of the (str)paths to the config file, without the name
        of the file.

          The first element of the list is the local directory + ".katal",
        the last element of the list is ~ + .katal .
        ________________________________________________________________________

        NO PARAMETER.

        RETURNED VALUE : the expected list of strings.
    """
    res = []

    res.append(os.path.os.path.join(normpath("."),
                                    normpath(ARGS.targetpath),
                                    CST__KATALSYS_SUBDIR))

    if CST__PLATFORM == 'Windows':
        res.append(os.path.join(os.path.expanduser("~"),
                                "Local Settings",
                                "Application Data",
                                "katal"))

    res.append(os.path.join(os.path.expanduser("~"),
                            ".katal"))

    return res

#///////////////////////////////////////////////////////////////////////////////
def read():
    configfile_name = "grammaticomastix.inia"

    if not os.path.exists(configfile_name):
        return False
    
    CFGFILEPARSER = configparser.ConfigParser()
    CFGFILEPARSER.read(configfile_name)
    
    return true
