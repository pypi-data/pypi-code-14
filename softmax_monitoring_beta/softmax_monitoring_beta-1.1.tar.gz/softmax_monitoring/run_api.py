import requests
import util
import static as softmax
import constants

class RunAPI(object):
	def __init__(self, token):
		self.name = "RUN_API"
		self.token = token

	# Creates a new run with specified name: 
	def new_run(self, run_name, enable_logging):
		self.enable_logging = enable_logging
		self.run_name = run_name

		self.job_id = softmax.job_api.create_job(run_name, token=self.token)
		self.train_line_id = softmax.job_api.create_line(self.job_id, "Train", token=self.token)
		self.val_line_id = softmax.job_api.create_line(self.job_id, "Val", token=self.token)
		self.test_line_id = softmax.job_api.create_line(self.job_id, "Test", token=self.token)

		return self.job_id

	# Adds a point to either train, val, test index
	def add_point(self, split_index, x, y):
		if split_index == constants.TRAIN_INDEX:
			softmax.job_api.create_point(self.train_line_id, x, y, token=self.token)
		elif split_index == constants.VAL_INDEX:
			softmax.job_api.create_point(self.val_line_id, x, y, token=self.token)
		elif split_index == constants.TEST_INDEX:
			softmax.job_api.create_point(self.test_line_id, x, y, token=self.token)
		else:
			raise Exception("Index of line is not specified %s" % split_index)

	def add_log(self, text):
		if self.job_id is not None and self.enable_logging:
			softmax.job_api.create_log(self.job_id, text, token=self.token)

	def add_trained_model(self, name, epoch, url, type):
		softmax.job_api.create_trained_model(self.job_id, name, epoch, url, type, token=self.token)

	def add_prediction(self, name, epoch, url, type):
		softmax.job_api.create_prediction(self.job_id, name, epoch, url, type, token=self.token)

	def add_error_log(self, text):
		softmax.job_api.create_error_log(self.job_id, text, token=self.token)

	def add_metadata(self, text):
		softmax.job_api.create_metadata(self.job_id, text, token=self.token)