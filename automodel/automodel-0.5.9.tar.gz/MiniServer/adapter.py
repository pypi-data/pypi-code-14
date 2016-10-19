from server import ServerService
class ServerAdapter(ServerService):
	"""docstring for adapter"""
	def __init__(self):
		super(ServerAdapter, self).__init__(None)
		# self.arg = arg

	def receive_file(self, filename):
		return super(ServerAdapter, self).exposed_receive_file(filename)

	def check_serial(self, password):
		return super(ServerAdapter, self).exposed_check_serial(password)

	def receive_file(self, filename, buffer_file):
		return super(ServerAdapter, self).exposed_receive_file(filename, buffer_file)

	def find_templates(self,serial):
		return super(ServerAdapter, self).exposed_find_templates(serial)

	def send_file(self, name_of_file):
		return super(ServerAdapter, self).exposed_send_file(name_of_file)

	def send_template(self, pdb_name):
		return super(ServerAdapter, self).exposed_send_template(pdb_name)

	def align(self,pir_sequence_file,template):
		return super(ServerAdapter, self).exposed_align(pir_sequence_file,template)

	def model(self, ali_ali, template):
		return super(ServerAdapter, self).exposed_model(ali_ali, template)

	def evaluate(self,template,model_file,ali_ali_file):
		return super(ServerAdapter, self).exposed_evaluate(template,model_file,ali_ali_file)

	def evaluatePROCHECK(self, model_file):
		return super(ServerAdapter, self).exposed_evaluatePROCHECK(model_file)

	def loopmodel(self,model, start_residue, end_residue):
		return super(ServerAdapter, self).exposed_loopmodel(model, start_residue, end_residue)

	def evaluatelooprefinament(self,template,model_file,loopmodel, ali_ali_file):
		return super(ServerAdapter, self).exposed_evaluatelooprefinament(template,model_file,loopmodel, ali_ali_file)

		