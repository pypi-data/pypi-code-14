#import rpyc
import tempfile
import os
import time
import modelagem
from file import *
import zipfile
from options.Prefs import Prefs

option = Prefs()
# PDBFolder = "/home/jorgehf/PDB/"
PDBFolder = option.get_setting("PDBFolder")


class ServerService(object):
	"""docstring for ServerService"""
	def __init__(self, arg):
		# super(ServerService, self).__init__()
		self.arg = arg
		self.workdir = tempfile.mkdtemp() + "/"
		print self.workdir

	def exposed_receive_file(self, filename):
		time.sleep(2)
		return open(self.workdir + os.path.basename(filename), "r")

	def exposed_check_serial(self, password):
		if password == "MODELIRANJE":
			return True
		else:
			return False

	def exposed_receive_file(self, filename, buffer_file):
		received_file = file(self.workdir + os.path.basename(filename), "w")
		received_file.write(buffer_file)
		received_file.close()

	def exposed_find_templates(self,serial):
		# self.callback = rpyc.async(callback)
		teste = modelagem.mold(self.workdir + "seq.ali")
		teste.make_build_profilepy()
		teste.find_templates()
		# self.callback("find_templates")

	def exposed_send_file(self, name_of_file):
		sending_file = file(self.workdir + os.path.basename(name_of_file), "r")
		buffer_file = sending_file.load_in_memory()
		sending_file.close()
		return buffer_file

	def exposed_send_template(self, pdb_name):
		pdb_path = PDBFolder + pdb_name + ".pdb"
		pdb_path_CAPS = PDBFolder + pdb_name.upper() + ".pdb"
		# print pdb_path_CAPS
		if os.path.exists(pdb_path):
			sending_file = file(pdb_path, "r")
			buffer_file = sending_file.load_in_memory()
			sending_file.close()
			return buffer_file

		elif os.path.exists(pdb_path_CAPS):
			sending_file = file(pdb_path_CAPS, "r")
			buffer_file = sending_file.load_in_memory()
			sending_file.close()
			return buffer_file
		else:
			raise IOError

	def exposed_align(self,pir_sequence_file,template):
		teste = modelagem.Align(self.workdir, self.workdir, os.path.basename(template),os.path.basename(pir_sequence_file))
		teste.make_readseq_py()
		teste.read_sequence()
		teste.make_align2d_py()
		teste.align_sequence()

	def exposed_model(self, ali_ali, template):
		teste = modelagem.Modeler(self.workdir, self.workdir, os.path.basename(template), os.path.basename(ali_ali))
		teste.make_get_model_py()
		teste.model_sequence()
		best_result = teste.get_results()
		# print 
		return os.path.basename(best_result)

	def exposed_evaluate(self,template,model_file,ali_ali_file):
		# teste = modelagem.Evaluate(template,model_file,ali_ali_file,self.workdir)
		# teste.make_evaluate_model(model_file)
		# teste.get_evaluate()
		# teste.make_evaluate_model(template)
		# teste.get_evaluate()
		# teste.plot_profiles()
		# return  'dope_profile.png'

		# loop_refinament_folder = self.workdir 
		evaluate_folder = self.workdir
		if not os.path.exists(evaluate_folder):
			os.mkdir(evaluate_folder)
		best_model = self.workdir + model_file
		# loop_model = self.workdir + loopmodel
		my_template = self.workdir + template
		# os.popen("cp "+ best_model + " " + loop_val)
		# os.popen("cp "+ loop_model + " " + loop_val)
		# os.popen("cp "+ my_template + " " + loop_val)
		multiple_align = modelagem.Malign2(evaluate_folder)
		multiple_align.create_script_in_folder(os.path.basename(my_template)[0:-4],os.path.basename(best_model)[0:-4])
		multiple_align.get_model()
		profile_best_model = modelagem.MakeProfile()
		profile_best_model.create_script_in_folder(evaluate_folder + os.path.basename(model_file))
		profile_best_model.get_model()
		profile_my_template = modelagem.MakeProfile()
		profile_my_template.create_script_in_folder(evaluate_folder + os.path.basename(template))
		profile_my_template.get_model()
		# profile_loop_model = modelagem.MakeProfile()
		# profile_loop_model.create_script_in_folder(evaluate_folder + os.path.basename(loopmodel))
		# profile_loop_model.get_model()

		plot_profiles = modelagem.GetProt2(evaluate_folder)
		plot_profiles.create_script_in_folder(my_template,best_model)
		plot_profiles.get_model()
		return "dope_profile_loop.png"

	def exposed_evaluatePROCHECK(self, model_file):
		teste = modelagem.Procheck_Evaluate(self.workdir, model_file)
		teste.copy_templates_for_procheck_evaluate()
		procheck_folder = teste.run_prochek()
		zipped_procheck_folder_name = procheck_folder + ".zip"
		zipped_procheck_folder = self.__zipper__(procheck_folder,zipped_procheck_folder_name)
		return os.path.basename(zipped_procheck_folder)

	def __recursive_zip__(self,zipf, directory, folder = ""):
		for item in os.listdir(directory):
			if os.path.isfile(os.path.join(directory, item)):
				zipf.write(os.path.join(directory, item), folder + os.sep + item)
			elif os.path.isdir(os.path.join(directory, item)):
				self.__recursive_zip__(zipf, os.path.join(directory, item), folder + os.sep + item)

	def __zipper__(self,folder,nome_destino):
		zipz = nome_destino
		zipf = zipfile.ZipFile(zipz, "w", compression=zipfile.ZIP_DEFLATED )
		path = folder
		self.__recursive_zip__(zipf, path)
		zipf.close()
		return nome_destino

	def exposed_loopmodel(self,model, start_residue, end_residue):
		teste = modelagem.Loop_Refinement(self.workdir + os.path.basename(model), start_residue, end_residue)
		teste.create_script_in_folder(self.workdir)
		teste.get_model()
		best_result = teste.get_results()
		# print 
		return os.path.basename(best_result)

	def exposed_evaluatelooprefinament(self,template,model_file,loopmodel, ali_ali_file):
   # def __loop_refinament_validation__(self,thread, callback):
		# self.callback = rpyc.async(callback)
		loop_refinament_folder = self.workdir 
		loop_val = loop_refinament_folder # + "loop_val" +loop +  os.sep
		if not os.path.exists(loop_val):
			os.mkdir(loop_val)
		best_model = self.workdir + model_file
		loop_model = self.workdir + loopmodel
		my_template = self.workdir + template
		# os.popen("cp "+ best_model + " " + loop_val)
		# os.popen("cp "+ loop_model + " " + loop_val)
		# os.popen("cp "+ my_template + " " + loop_val)
		multiple_align = modelagem.Malign(loop_val)
		multiple_align.create_script_in_folder(os.path.basename(my_template)[0:-4],os.path.basename(best_model)[0:-4],os.path.basename(loop_model)[0:-4])
		multiple_align.get_model()
		profile_best_model = modelagem.MakeProfile()
		profile_best_model.create_script_in_folder(loop_val + os.path.basename(model_file))
		profile_best_model.get_model()
		profile_my_template = modelagem.MakeProfile()
		profile_my_template.create_script_in_folder(loop_val + os.path.basename(template))
		profile_my_template.get_model()
		profile_loop_model = modelagem.MakeProfile()
		profile_loop_model.create_script_in_folder(loop_val + os.path.basename(loopmodel))
		profile_loop_model.get_model()

		plot_profiles = modelagem.GetProt(loop_val)
		plot_profiles.create_script_in_folder(my_template,best_model,loop_model)
		plot_profiles.get_model()
		return "dope_profile_loop.png"

		# self.dope_profile_loop = "loop/dope_profile.png"
		# self.callback("dope_profile_loop")



#if __name__ == "__main__":
#    from rpyc.utils.server import ThreadedServer
#    t = ThreadedServer(ServerService, port = 18861)
#    t.start()
