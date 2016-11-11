#!/usr/bin/python
import logging
import logging.handlers
import sys
import os

class Loggers(object):
	'''Provides log functionalities either in stream or file form

		Arguments:
			logName (:obj:`str`): name of the log handler
			logFolderPath (:obj:`str`,optional, *default* =None): folder where the log's files will lie
			logFile (:obj:`str`,optional, *default* =None): path of the debug and error log's files

	'''
	def __init__(self, logName, **kwargs):
		defaultArgs= {'logFolderPath':None,'logFile':None}
		defaultArgs.update(kwargs)
		self.log = logging.getLogger(logName)
		self.default_formatter = logging.Formatter('Log: %(message)s | Log level:%(levelname)s | Date:%(asctime)s',datefmt='%d/%m/%Y %H:%M:%S')
		if not len(self.log.handlers):
			self.default_formatter = logging.Formatter('Log: %(message)s | Log level:%(levelname)s | Date:%(asctime)s',datefmt='%d/%m/%Y %H:%M:%S')
			self.stream_handler = logging.StreamHandler(sys.stdout)
			self.stream_handler.setLevel(logging.DEBUG)
			self.stream_handler.setFormatter(self.default_formatter)
			self.log.addHandler(self.stream_handler)
		if defaultArgs['logFolderPath']:
			logName = defaultArgs['logFile'] if defaultArgs['logFile'] else logName
			self.errorLogfile = defaultArgs['logFolderPath']+"/"+logName+".error.log.bz2"
			self.debugLogfile = defaultArgs['logFolderPath']+"/"+logName+".debug.log.bz2"
			if not os.path.isdir(defaultArgs['logFolderPath']):
				print 'tring to create the path'
				try:
					os.mkdir(defaultArgs['logFolderPath'])
					if not os.path.isdir(defaultArgs['logFolderPath']):
						print 'folder not created accordingly'
					else:
						print 'folder created :'+defaultArgs['logFolderPath']
						print os.system('cd '+defaultArgs['logFolderPath']+';cd ..;ls -lra')
				except:
					print 'It was not possible to write to the log folder '+defaultArgs['logFolderPath']+'. You must create it manually and set the required permissions.'
			else:
				try:
					self.debug_handler = logging.handlers.RotatingFileHandler(self.debugLogfile,maxBytes=600000,encoding='bz2-codec',backupCount=4)
					self.error_handler = logging.handlers.RotatingFileHandler(self.errorLogfile,maxBytes=600000,encoding='bz2-codec',backupCount=4)
					self.debug_handler.setLevel(logging.DEBUG)
					self.debug_handler.setFormatter(self.default_formatter)
					self.error_handler.setLevel(logging.ERROR)
					self.error_handler.setFormatter(self.default_formatter)
				except:
					print 'It was not possible to write to the log folder '+defaultArgs['logFolderPath']+'. You must create it manually and set the required permissions.'

	def setLogRotateHandler(self,setFile):
		'''Enables/disables logs to be written to files

		Arguments:
			setFile (:obj:`bool`): False disables, True enables

		'''
		if hasattr(self, 'debug_handler'):
			if setFile:
				self.log.addHandler(self.debug_handler)
				self.log.addHandler(self.error_handler)
			else:
				try:
					self.log.removeHandler(self.error_handler)
					self.log.removeHandler(self.debug_handler)
				except:
					pass
		else:
			self.log.debug('The file log handlers were not created. It is not possible to write to the log files.')

	def setLogLevel(self,logLevel):
		'''Configures class log level

		Arguments:
			logLevel (:obj:`str`): log level ('NOTSET','DEBUG','INFO' 'WARNING', 'ERROR', 'CRITICAL')

		'''
		exec "self.log.setLevel(logging."+logLevel+")"
		exec "self.log."+logLevel.lower()+"('Changing log level to "+logLevel+"')"

	def setLogFormat(self, logType, logFormat):
		'''Configures log format

		Arguments:
			logType (:obj:`str`): log type (error, debug or stream)
			logFormat (:obj:`str`): log format (ex:"Log: %(message)s | Log level:%(levelname)s |
				Date:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S")

		'''
		if not (logType == 'error' or logType == 'stream' or logType == 'debug'):
			self.log.debug('Log type must be error, stream, or debug')
		else:
			exec "self.default_formatter = logging.Formatter('"+logFormat+"')"
			exec "self."+logType+"_handler.setFormatter(self.default_formatter)"


