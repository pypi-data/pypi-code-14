from enum import Enum
import socket
import time

class Status(Enum):
	'''
	Operational status codes for the application
	'''

	RUNNING = 0
	WORKING = 1

__all__ = ['Status']
__host__ = 'localhost'
__port__ = 80
__start_time__ = int(time.time())
__status__ = Status.RUNNING
__version__ = '0.2.0'
