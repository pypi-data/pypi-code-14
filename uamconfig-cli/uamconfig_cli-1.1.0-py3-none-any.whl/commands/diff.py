from uamconfig.utils.utils import *

def find_differences(old_properties, new_properties):
    """ Returns a dictionary of all the keys and values that are different in
        data2 to data1
        @param  old_properties - A dictionary of the current properties files
        @param  new_properties - A dictionary of the new properties file
        @return A dictionary containing all the entries in the old config file where the
                values do not match the values in data1 for the respective key.
    """
    differences = dict()
    for key in old_properties.keys():
        if key not in new_properties.keys() or new_properties[key] != old_properties[key]:
            differences[key] = old_properties[key]
    return differences

def run(old_properties_filename, new_properties_filename, output):
    old_properties = get_properties(old_properties_filename)
    new_properties = get_properties(new_properties_filename)
    differences = find_differences(old_properties, new_properties)
    if len(differences) > 0:
        print("{} differences written to {}".format(len(differences), output))
    else:
        print("Configuration files are identical")
    export_differences(differences, output)
