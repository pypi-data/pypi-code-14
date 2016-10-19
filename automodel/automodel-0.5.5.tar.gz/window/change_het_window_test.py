from change_het_window import ChangeHetWindow
import wx

if __name__ == '__main__':
	app = wx.PySimpleApp()
	# my_window = ChangeHetWindow(None, 1,"tests/change_het_tests/1bdm.pdb")
	my_window = ChangeHetWindow(None, 1,"/tmp/tmprYCqYC/5mdh.pdb")
	my_window.Show()
	app.MainLoop()