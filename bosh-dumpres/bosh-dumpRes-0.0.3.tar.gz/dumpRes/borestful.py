import requests
import json
import sys

def cmd2JSON(cmd,workspace):
	return json.dumps({'Stmt':cmd,'Workspace':workspace,'Opts':{}})

def getData(server,cmdStr,workspace):
	r = requests.post(server,data=cmd2JSON(cmdStr,workspace) , stream=True)
	for content in json_stream(r.raw):
		#print(content)
		print (json.dumps(content))
	#r = requests.post(server,data=cmd2JSON(cmdStr))
	#return json.dumps(r.text)
	#return json.dumps(r.json())

def json_stream(fp):
	for line in fp:
		yield json.loads(line)

if __name__ == "__main__":
	server = sys.argv[1]
	cmd = sys.argv[2]
	workspace = ""
	if len(sys.argv) > 3:
		workspace = sys.argv[3]
	getData(server,cmd,workspace)
