import xml.etree.cElementTree as ET
import xml
from os import walk
import os
import shutil

def get_files(directory):
    """
    Walks the directory and takes the souce and header file paths to be returned.
    :param directory: The directory to search
    :return: A tuple of (sources, headers) where sources and headers are a list of strings representing file paths.
    """
    sources = []
    headers = []
    for (dirname, _, filenames) in walk(directory):
        if "nbproject" not in dirname:
            new_dir = dirname.replace(directory, "")
            if len(new_dir) > 0:
                new_dir += "/"
            for f in filenames:
                if f.endswith(".c") or f.endswith(".cpp"):
                    sources.append(new_dir + f)
                elif f.endswith(".h"):
                    headers.append(new_dir + f)
    return (sources, headers)


def modify_project(directory):
    proj_path = directory + "nbproject/project.xml"
    proj_name = os.path.basename(os.path.normpath(directory))
    project = ET.parse(proj_path)
    # TODO: Fix this messy hack to get name element.
    # TODO: Also potentially fix inserting namespaces as ns0 ns1 etc.
    project.getroot()[1][0][0].text = proj_name
    project.write(proj_path)


def modify_config(config_path, src, headers):
    config = ET.parse(config_path)
    root = config.getroot()
    logical_root = root[0]
    print("Adding files to \"logical folders\"")
    ## add the files to logical folders
    for elem in logical_root.getchildren():
        if elem.attrib['name'] == "HeaderFiles":
            for header in headers:
                newelem = ET.SubElement(elem, "itemPath")
                newelem.text = header
        if elem.attrib['name'] == "SourceFiles":
            for source in src:
                newelem = ET.SubElement(elem, "itemPath")
                newelem.text = source
    print("Configuring build configs")
    ## add conf data stuff
    conf_root = root.find("./confs")
    # copy the files
    allfiles = src.copy()
    allfiles.extend(headers)
    for conf in conf_root.findall("./conf"):
        for item in allfiles:
            newElem = ET.SubElement(conf, "item")
            newElem.attrib = {"path": item,
                              "ex": "false",
                              "flavor2": "0"
                              }
            if item in headers:
                newElem.attrib["tool"] = "3"
            else:
                newElem.attrib["tool"] = "0"
    config.write(config_path)


def create_nbproject(directory):
    nbdir = directory + "nbproject/"
    if os.path.exists(nbdir):
        shutil.rmtree(nbdir)
    os.mkdir(nbdir)
    new_config_path = nbdir + "configurations.xml"
    if not os.path.exists(xml_files_path + "/Makefile"): # only copy makefile if project doesn't already have one.
        # TODO: possibly support getting Makefile from within subdirectories when getting source/header files.
        shutil.copyfile(xml_files_path + "/Makefile", directory + "Makefile")
    shutil.copyfile(xml_files_path + "/project.xml", nbdir + "project.xml")
    shutil.copyfile(xml_files_path + "/configurations.xml", new_config_path)
    return new_config_path


def main():
    # TODO: add args check for custom dir
    directory = os.getcwd()
    if not directory.endswith("/"):
        directory += "/"
    print(directory)
    sources, headers = get_files(directory)
    print("Found %d sources and %d headers" % (len(sources), len(headers)))
    print(sources)
    print(headers)
    # If netbeans project exists here already, remove it. Else, create the empty folder.
    new_config_path = create_nbproject(directory)
    print("Creating the new config at %s" % new_config_path)
    modify_config(new_config_path, sources, headers)
    print("Modifying project")
    modify_project(directory)
    print("Process complete!")


if __name__ == '__main__':
    xml_files_path = "/usr/etc/"
    main()