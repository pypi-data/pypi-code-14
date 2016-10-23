import json,httplib

try:
	connection = httplib.HTTPSConnection('api.notify.center', 443)

except:
	print "[NotifyCenter: error]"
def notify(pushIds,message,verbose=False):
	if not isinstance(message, basestring):
		print "[NotifyCenter Error: message must be a string]"
	else:
		try:
			if isinstance(pushIds, basestring):
				pushIds = [pushIds]
        		connection.connect()
        		connection.request('POST', '/notify', json.dumps({
                		"pushIds" : pushIds,
                		"message" : message})
        		)
        		result = json.loads(connection.getresponse().read())
        		if verbose:
                		print result
		except:
			print "[NotifyCenter: error]"


def main():
    """Entry point for the application script"""
