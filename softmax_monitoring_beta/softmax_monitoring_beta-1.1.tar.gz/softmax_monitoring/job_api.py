#Simple visualization API-- to log items
import requests
import util

class JobAPI(object):
	def __init__(self, request_endpoint):
		self.request_endpoint = request_endpoint
		
		# Job endpoint
		self.job_endpoint = self.request_endpoint + "/job/"
		self.line_endpoint = self.request_endpoint + "/line/"
		self.point_endpoint = self.request_endpoint + "/point/"

		# Model and Metadata Endpoints
		self.metadata_endpoint = self.request_endpoint + "/metadata/"
		self.error_log_endpoint = self.request_endpoint + "/error_log/"
		self.trained_model_endpoint = self.request_endpoint + "/trained_model/"
		self.prediction_endpoint = self.request_endpoint + "/prediction/"

		# Cassandra Logging endpoint
		self.log_endpoint = self.request_endpoint + "/log/"
		self.print_config()

	def print_config(self):
		print("Request endpoint %s" % self.request_endpoint)
		print("Job endpoint %s" % self.job_endpoint)
		print("Line endpoint %s" % self.line_endpoint)
		print("Point endpoint %s" % self.point_endpoint)
		print("Metadata endpoint %s" % self.metadata_endpoint)
		print("Error log endpoint %s" % self.error_log_endpoint)
		print("Trained model endpoint %s" % self.trained_model_endpoint)

	# Creates a new job with specified name, returns the job id
	def create_job(self, job_name, token):
		raw_body = {'name' : job_name}
		content, status_code = util.post(self.job_endpoint, raw_body, token=token)
		id = content['id']
		print("Created new job with id %s" % id)
		return id

	# Creates a new line with specified name, and job id
	# Returns the id
	def create_line(self, job_id, line_name, token):
		body = {'job' : job_id, 'name' : line_name}
		content, status_code = util.post(self.line_endpoint, body, token=token)
		id = content['id']
		return id

	# Creates a model with specified name, epoch and url
	# Returns the id
	def create_trained_model(self, job_id, name, epoch, url, model_type, token):
		raw_body = {'job' : job_id, 'name' : name, \
		'epoch' : epoch, 'url' : url, 'type' : model_type}

		content, status_code = util.post(self.trained_model_endpoint, raw_body, token=token)
		model_id = content['id']
		return id

	# Creates a prediction with specified id, name, epoch, url, and prediction type
	def create_prediction(self, job_id, name, epoch, url, prediction_type, token):
		raw_body = {'job' : job_id, 'name' : name, 'epoch' : epoch, \
		'url' : url, 'type' : prediction_type}

		content, status_code = util.post(self.prediction_endpoint, raw_body, token=token)
		return content

	# Creates an error log
	def create_error_log(self, job_id, text, token):
		raw_body = {'job' : job_id, 'text' : text}
		content, status_code = util.post(self.error_log_endpoint, raw_body, token=token)
		return content

	# Creates metadata with specified job id and text
	def create_metadata(self, job_id, text, token):
		raw_body = {'job' : job_id, 'text' : text}
		content, status_code = util.post(self.metadata_endpoint, raw_body, token=token)
		return content

	# Creates a point with specified x, y coordinates for line with line_id
	def create_point(self, line_id, x, y, token):
		raw_body = {'line' : line_id, 'x' : x, 'y' : y}
		content, status_code = util.post(self.point_endpoint, raw_body, token=token)
		return content

	def create_log(self, job_id, text, token):
		raw_data = {'job_id' : job_id, 'text' : text}
		content, status_code = util.post(self.log_endpoint, raw_data, token=token)
		return content
