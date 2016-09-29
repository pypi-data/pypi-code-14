__author__ = 'xxxx'
import os,sys
import linecache

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import handleCmd
class ProfileCmd:
    useProfile = 'useProfile'
    addProfile = 'addProfile'
    name = '--name'
class ProfileHandler:
    def __init__(self):
        self.handleCmd = handleCmd.handleCmd()

    def getProfileHandlerCmd(self):
        return [ProfileCmd.useProfile, ProfileCmd.addProfile]

    def getProfileHandlerOptions(self):
        return ['--name']

    def useProfileCmd(self, cmd, keyValues):
        if cmd.lower() == ProfileCmd.useProfile.lower():
            if keyValues.has_key(ProfileCmd.name) and len(keyValues[ProfileCmd.name]) > 0:
                _value = keyValues[ProfileCmd.name][0] # use the first value
                if (self.setUserProfile(_value) == True):
                    print "Set user "+_value +" as the default user!"
            else:
                print "Your input is error! Please use cmd \'qcloudcli useprofile --name XX\' to set the default user."
        else:
            print "[", cmd, "] is not right, do you mean "+ProfileCmd.useProfile+" ?"

    def addProfileCmd(self, keyValues):
            userKey = ''
            userSecret = ''
            newProfileName = ''
            #check --name is valid
            if keyValues.has_key(ProfileCmd.name) and len(keyValues[ProfileCmd.name]) > 0:
                _value = keyValues[ProfileCmd.name][0] # check the first value
                # only input key and secret
                newProfileName = _value
            else:
                # need input profilename key and value
                newProfileName = raw_input("New profile name: ")
            userKey = raw_input("Qcloud API SecretID: ")
            userSecret = raw_input("Qcloud API SecretKey: ")
            userRegion = raw_input("Region Id: ")
            userOutput = raw_input("Output format: ")
            _credentialsPath = os.path.join(self.handleCmd.showQcloudConfigurePath(),self.handleCmd.credentials)
            if os.path.exists(_credentialsPath):
                f = open(_credentialsPath, 'a')
                try:
                    content = "[profile "+newProfileName+"]\nqcloud_secretkey = "+userSecret+"\nqcloud_secretid = " +userKey+ "\n"
                    f.write(content)
                finally:
                    f.close()
            else:
                print "your input is not right, do you want "+ProfileCmd.addProfile+" ?"

            _configurePath =os.path.join(self.handleCmd.showQcloudConfigurePath(),self.handleCmd.configure)
            if os.path.exists(_configurePath):
                f = open(_configurePath, 'a')
                try:
                    content = "[profile " + newProfileName + "]\noutput = " + userOutput + "\nregion = " + userRegion + "\n"
                    f.write(content)
                finally:
                    f.close()
            else:
                print "your input is not right, do you mean "+ProfileCmd.addProfile+" ?"


    def setUserProfile(self,value):
        _configurePath = os.path.join(self.handleCmd.showQcloudConfigurePath(), self.handleCmd.configure)
        _credentialsPath = os.path.join(self.handleCmd.showQcloudConfigurePath(),self.handleCmd.credentials)
        useoutput = ''
        useregion = ''
        usekey = ''
        useid = ''
        if os.path.exists(_configurePath):
            va_flag = 0
            de_flag = 0

            f = open(_configurePath, 'r+')
            flist = f.readlines()
            for i in range(len(flist)-2):
                if flist[i].find(value) > 0:
                    va_flag = 1
                    useoutput = flist[i+1]
                    useregion = flist[i+2]
            if va_flag == 0:
                print "Cannot find user name "+ value +"!"
                return False

            for j in range(len(flist)-2):
                if flist[j].find("default") > 0:
                    de_flag = 1
                    flist[j + 1] = useoutput
                    flist[j + 2] = useregion

            if de_flag == 0:
                print "You have not set default user!"
                return False
            f = open(_configurePath, 'w+')
            f.writelines(flist)

        if os.path.exists(_credentialsPath):
            key_flag = 0
            id_flag = 0

            f = open(_credentialsPath, 'r+')
            flist = f.readlines()
            for i in range(len(flist)-2):
                if flist[i].find(value) > 0:
                    key_flag = 1
                    usekey = flist[i + 1]
                    useid = flist[i + 2]
            if key_flag == 0:
                print "Cannot find user name " + value + "!"
                return False

            for j in range(len(flist)-2):
                if flist[j].find("default") > 0:
                    id_flag = 1
                    flist[j + 1] = usekey
                    flist[j + 2] = useid
            if id_flag == 0:
                print "You have not set default user!"
                return False
            f = open(_credentialsPath, 'w+')
            f.writelines(flist)\

        return True

if __name__ == "__main__":
    pass