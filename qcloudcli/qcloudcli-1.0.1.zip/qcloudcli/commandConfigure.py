import showHelp
import handleData

class commandConfigure:
    def __init__(self):
        self.ecs = ecs()
        self.rds = rds()
        self.main_options = ['output', 'SecretId', 'SecretKey', 'Endpoint']
        self.helper = showHelp.qcloudCliHelper()
        self.open_api_headler = handleData.qcloudOpenApiDataHandler()

    def getExtensionOptions(self, cmd, operation):
        if cmd is None or operation is None:
            return None
        if operation in handleData.version_cmds:
            return None
        if cmd.lower() == 'rds':
            _rds = rds()
            return _rds.extensionOptions[operation]
        if cmd.lower() == 'ecs':
            _ecs = ecs()
            return _ecs.extensionOptions[operation]
        return None

    def getExtensionOperations(self, cmd):
        return self.open_api_headler.getExtensionOperationsFromCmd(cmd)
    #
    # this api will return the options for each extension operations, such as "ecs importInstance" "rds ExportDBInstance"
    #
    def showExtensionOperationHelp(self, cmd, operation):
        parameterList = list()
        self.helper.showParameterError(cmd, operation, parameterList)

    def appendList(self, parameterList, optionList):
        for item in optionList:
            parameterList.append(item)

class rds:
    cmdName = 'Rds'
    exportDBInstance = 'ExportDBInstance'
    importDBInstance = 'ImportDBInstance'
    extensionOperations = [exportDBInstance, importDBInstance]
    extensionOptions = {exportDBInstance:['DBInstanceId','OwnerAccount','OwnerId','ResourceOwnerAccount','filename'],
                        importDBInstance:['count','filename']}

class ecs:
    cmdName = 'Ecs'
    exportInstance = 'ExportInstance'
    importInstance = 'ImportInstance'
    extensionOperations = [exportInstance, importInstance]
    extensionOptions = {exportInstance:['InstanceId','OwnerAccount','OwnerId','ResourceOwnerAccount','filename'],
                        importInstance:['count','filename']}

if __name__ == '__main__':
    # print type(rds.extensionOperations)
    # print type(rds.extensionOptions)
    # print rds.extensionOptions['ll']
    configure = commandConfigure()
    print configure.showExtensionOperationHelp("ecs", "ExportInstance")
