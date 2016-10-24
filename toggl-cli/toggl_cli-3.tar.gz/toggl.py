#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import sys
import yaml
import os


from toggl_api import TogglApi

path = os.path.dirname(os.path.realpath(__file__))

yaml_file = open(path + '/config.yml')
config = yaml.load(yaml_file)

# print(config);

if __name__ == "__main__" :
    print('**** TOGGL CLI CLIENT BY -- GOURAV *****\n')

    API = config['default_api']['key']
    WID = config['default_workspace']['id']


    print('Default Account is '+API+'\n')
    print('Default workspace is : '+str(WID)+'\n\n')

    business = {}

    workspace_code = 0
    for workspace in config["workspaces"]:
        business["w"+str(workspace_code)] = {
            "btype" : "workspace",
            "bid" : workspace["id"],
            "bname" :  workspace["name"]
        }
        workspace_code += 1

    project_code = 0
    for project in config["projects"]:
        business["p"+str(project_code)] = {
            "btype" : "project",
            "bid" : project["id"],
            "bname" :  project["name"]
        }
        project_code += 1

    def display_menu():
        print("\t\tcode\t\ttype\t\tname\n")
        for code, desc in business.items():
            print("\t\t"+code+"\t\t"+desc["btype"]+"\t\t"+desc["bname"]+"\n")
        conf = business.get(input("Enter Code\n>"))
        if(conf != None):
            return TogglApi(api_token=API,btype=conf['btype'],bid=conf['bid'])
        return TogglApi(api_token=API,btype="workspace",bid=WID)

    toggl = display_menu()


    def start():
        toggl.start(input("Enter description\n>"))

    def stop():
        toggl.stop()
        print("stop")

    def current_entry():
        toggl.get_current()

    def menu():
        toggl = display_menu()

    commands = {
        'start' : start,
        'stop' : stop,
        'current' : current_entry,
        'menu' : menu
    }

    flag = True
    while(flag):
        cmd= input("Enter Command or type exit to quit \n>")
        if (cmd == "exit"):
            flag = False
            continue
        command = commands.get(cmd.strip())
        command()
