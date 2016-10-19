import subprocess 
import platform
import os
import shutil
# from window.AlignmentEditorWindow import AlignmentEditorWindow

class Clientold(object):
    def open_txt_file(self,filename):
  #       if platform.system() == 'Windows':
  #           subprocess.Popen(["write.exe", filename])
  #       if platform.system() == 'Linux':
  #           if 'DESKTOP_SESSION' in os.environ:
  #               if os.environ['DESKTOP_SESSION'] == 'gnome':
  #                   subprocess.Popen(["gedit", filename])
		# else:
		#     subprocess.Popen(["gedit", filename])
		template_load_window = AlignmentEditorWindow(self)
		template_load_window.Show()

    def save_result_in(self,pathname, to_pathname):
        shutil.copyfile(pathname,to_pathname)

    def copy_file_in(self,path_of_file,distination):
        shutil.copyfile(path_of_file, distination)

    def open_result(self, pathname):
        if platform.system() == 'Windows':
            subprocess.Popen(os.environ['PROGRAMFILES'] + os.sep + 'University of Illinois\\VMD' + os.sep + 'vmd.exe ' + pathname)
        if platform.system() == 'Linux':
            subprocess.Popen(["vmd", pathname])

    def open_procheck_folder(self, myfolder):
        if platform.system() == 'Windows':
            subprocess.Popen(['explorer.exe', myfolder])
        if platform.system() == 'Linux':
            if 'DESKTOP_SESSION' in os.environ:
		subprocess.Popen(['nemo', myfolder])
                if os.environ['DESKTOP_SESSION'] == 'gnome':
                    subprocess.Popen(['nemo', myfolder])
            else:
                subprocess.Popen(['dolphin', myfolder])
        else:
            subprocess.Popen(['nemo', myfolder])

    def open_plot_profile(self,pathname):
        if platform.system() == 'Windows':
            subprocess.Popen(os.environ['PROGRAMFILES'] + os.sep + 'internet explorer' + os.sep + 'iexplore.exe ' + self.path_of_file("dope_profile"))
        if platform.system() == 'Linux':
            if 'DESKTOP_SESSION' in os.environ:
                if os.environ['DESKTOP_SESSION'] == 'gnome':
                    subprocess.Popen(["eog", pathname])
		else:
		    subprocess.Popen(["eog", pathname])

    # def open_plot_profile_loop(self):
    #     if platform.system() == 'Windows':
    #         subprocess.Popen(os.environ['PROGRAMFILES'] + os.sep + 'internet explorer' + os.sep + 'iexplore.exe ' + self.path_of_file("dope_profile_loop"))
    #     if platform.system() == 'Linux':
    #         if 'DESKTOP_SESSION' in os.environ:
    #             if os.environ['DESKTOP_SESSION'] == 'gnome':
    #                 subprocess.Popen(["eog" , self.path_of_file("dope_profile_loop")])
    #             if os.environ['DESKTOP_SESSION'] == 'default':
    #                 subprocess.Popen(["eog" , self.path_of_file("dope_profile_loop")])
    #     else:
    #         subprocess.Popen(["eog" , self.path_of_file("dope_profile_loop")])

    def open_in_other_editor(self,editor, arquivo):
        subprocess.Popen([editor, arquivo])

    def save_myloop_in(self,pathname):
        shutil.copyfile(self.path_of_file("myloop"),pathname)
