import requests


username, apikey = "ross", "092d980e2c9f4713a78052a7fb01408b"
url = "http://localhost:5000/verify"
data = {}
params = {}
headers = { "Content-Type": "application/json"}
r = requests.post(url=url, headers=headers, data=data, params=params, auth=(username, apikey))
print('response: ' + r.text)
