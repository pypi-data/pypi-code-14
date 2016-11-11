import unittest
from loggers import Loggers
import bz2file
import shutil
import re
import os

def decompBz2(logFile):
	with bz2file.open(logFile) as mfile:
		datalog=mfile.read()
	return datalog

class LoggersTest(unittest.TestCase):
	@classmethod  
	def setUpClass(cls):
		cls.logpath='/tmp/logTest'
		os.mkdir(cls.logpath)
		cls.logTest = Loggers('logTest', logFolderPath = cls.logpath)
		cls.logTest.setLogRotateHandler(True)

	@classmethod  
	def tearDownClass(cls):
		shutil.rmtree(cls.logpath)

	def performRegexTest(self, logLevel, logFunction, logMessage, logLevelDst):
		self.logTest.setLogLevel(logLevel)
		logFunction(logMessage)
		datalog = decompBz2(self.logpath+'/logTest.'+logLevelDst+'.log.bz2')
		match=re.match('Log: '+logMessage+' | Log level:'+logLevel+' | Date:\d{2}\/\d{2}\/\d{4} d{2}:\d{2}:\d{2}',datalog.splitlines()[-1])
		return match

	def testDebugLog(self):
		self.assertIsNotNone(self.performRegexTest('DEBUG', self.logTest.log.debug, 'Debug Test.', 'debug'))

	def testInfoLog(self):
		self.assertIsNotNone(self.performRegexTest('INFO', self.logTest.log.info, 'Info Test.', 'debug'))

	def testWarningLog(self):
		self.assertIsNotNone(self.performRegexTest('WARNING', self.logTest.log.warning, 'Warning Test.', 'debug'))

	def testErrorLog(self):
		self.assertIsNotNone(self.performRegexTest('ERROR', self.logTest.log.error, 'Error Test.', 'error'))

	def testCriticalLog(self):
		self.assertIsNotNone(self.performRegexTest('CRITICAL', self.logTest.log.critical, 'Critical Test.', 'error'))

	def testLogHierarchy(self):
		logMessage ='Debug log in CRITICAL log level Test.'
		self.assertIsNone(self.performRegexTest('CRITICAL', self.logTest.log.debug,logMessage, 'error'))
		logMessage ='Info log in CRITICAL log level Test.'
		self.assertIsNone(self.performRegexTest('CRITICAL', self.logTest.log.info,logMessage, 'error'))
		logMessage ='Warning log in CRITICAL log level Test.'
		self.assertIsNone(self.performRegexTest('CRITICAL', self.logTest.log.warning,logMessage, 'error'))
		logMessage ='Error log in CRITICAL log level Test.'
		self.assertIsNone(self.performRegexTest('CRITICAL', self.logTest.log.error,logMessage, 'error'))
		logMessage ='Critical log in CRITICAL log level Test.'
		self.assertIsNotNone(self.performRegexTest('CRITICAL', self.logTest.log.critical,logMessage, 'error'))

if __name__ == "__main__": 
	unittest.main()
