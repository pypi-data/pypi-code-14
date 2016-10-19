import wx
import time

class AutoModelError(object):
	"""docstring for AutoModelError"""
	def __init__(self, error_msg):
		wx.MessageBox(error_msg, 'Oops', wx.OK | wx.ICON_ERROR)

	def log(self, mensage):
		error_log = file("error_log.txt", "a")
		error_log_msg = str(time.localtime().tm_mday)+"/"+str(time.localtime().tm_mon)+"/"+str(time.localtime().tm_year)+" "+str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)+":"+str(time.localtime().tm_sec)+" "+str(mensage)+"\n"
		# error_log.write(mensage)      
		# traceback.print_exception(etype, value, etraceback,limit=2, file=error_log)
		error_log.write("----------\n")
		error_log.close()
