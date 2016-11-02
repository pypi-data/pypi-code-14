import datetime
from SeasObjects.model.Request import Request
from SeasObjects.model.Activity import Activity
from SeasObjects.seasexceptions.InsufficientDataException import InsufficientDataException

from SeasObjects.common.RESOURCE import RESOURCE


class RequestFactory(object):
	
	def __init__(self):
		pass
	
	def create(self, generatedBy):
		evaluation = Request()
		if (generatedBy is None or (generatedBy is not None and generatedBy == "")):
			raise InsufficientDataException("Invalid seas:generatedBy URI.")

		g = Activity(generatedBy)
		g.clearTypes()
		evaluation.setGeneratedBy(g)
		
		# timestamp of when this message is being generated (now)
		evaluation.setGeneratedAt(datetime.datetime.now())

		evaluation.addType(RESOURCE.SEAS_REQUEST)
		
		return evaluation;

	
	def fromString(self, data, serialization):
		try:
			return Request().parse(Tools().getResourceByType(RESOURCE.SEAS_REQUEST, Tools().fromString(data, serialization)))
		except:
			print "Unable to parse Evaluation by type seas:Request from the given string."
			traceback.print_exc()
			return None

	def createRegistrationRequest(self, generatedBy):
		req = Request()
		if (generatedBy is None or (generatedBy is not None and generatedBy == "")):
			raise InsufficientDataException("Invalid registrant (seas:generatedBy) URI.");
		
		req.setGeneratedBy(Activity(generatedBy))
		
		# timestamp of when this message is being generated (now)
		req.setGeneratedAt(datetime.datetime.now())

		req.addType(RESOURCE.SEAS_REQUEST)
		
		return req
	

	def createWeatherForecastTimeserie(self, generatedBy):
		evaluation = Evaluation();
		if (generatedBy is None or (generatedBy is not None and generatedBy == "")):
			raise InsufficientDataException("Invalid registrant (seas:generatedBy) URI.");

		evaluation.setGeneratedBy(Activity(generatedBy))

		# timestamp of when this message is being generated (now)
		evaluation.setGeneratedAt(datetime.datetime.now());

		evaluation.addType(RESOURCE.SEAS_EVALUATION)
		evaluation.addCategory(RESOURCE.SEAS_FORECAST)
		systemOfInterest = SystemOfInterest()
		systemOfInterest.setType(RESOURCE.SEAS_WEATHER)
		evaluation.setSystemOfInterest(systemOfInterest)
		
		return evaluation
