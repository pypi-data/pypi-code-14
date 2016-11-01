from uamconfig.utils.utils import *

def patch(properties, patch):
    for key in patch.keys():
        properties[key] = patch[key]
    return properties

def run(properties_filename, patch_filename, output):
    properties = get_properties(properties_filename)
    patch = get_properties(patch_filename)
    patched_properties = patch(properties, patch)
    export_differences(patched_properties, output)
    print("{} changes merged into properties.".format(len(patch)))
    print("Written to {}".format(output))
