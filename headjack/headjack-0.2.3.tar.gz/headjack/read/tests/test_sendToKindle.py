import os
import nose
import shutil
import yaml
from headjack.utKit import utKit

from fundamentals import tools


# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()


# load settings
settingsFile = pathToInputDir + "/example_settings.yaml"
# settingsFile = "/Users/Dave/.config/headjack/headjack.yaml"


stream = file(settingsFile, 'r')
settings = yaml.load(stream)
stream.close()


su = tools(
    arguments={"settingsFile": settingsFile},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="headjack"
)
arguments, settings, log, dbConn = su.setup()


import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

# xt-setup-unit-testing-files-and-folders


class test_sendToKindle():

    def test_sendToKindle_function(self):

        from headjack.read import sendToKindle
        sender = sendToKindle(
            log=log,
            settings=settings,
            dbConn=dbConn
        )
        sender.send()

    def test_sendToKindle_function_exception(self):

        from headjack.read import sendToKindle
        try:
            this = sendToKindle(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function
