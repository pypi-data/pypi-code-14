import os
import random
import zipfile
import argparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import json
from Table import Table
from ConfigParser import SafeConfigParser
import time
from sys import stdout
from os.path import expanduser

# functions for writing files, creating the zip
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file), os.path.join(path, '.')))
            
def writeFile(path, string):
    f = open(path, "w")
    f.write(string)
    f.close()

def authRest(host, un, pw, dom):
	# authentication
        URI = host+"/api/login"
        auth = {"username":un,"password":pw,"domain":dom}
        headers = {"Content-Type":"application/json"}
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        ar = requests.put(URI, data=json.dumps(auth), headers=headers, verify=False)
        token = str(ar.content).replace('"','')
	if ("Login failed for user" in str(token)):
		print
		print "Your authentication credentials to the server were bad"
		print
		exit(1)
	return token

def cli():
	# Build CLI parser to get info. Should be passed in via CLI from PHP
	parser = argparse.ArgumentParser(description='CLI Tool for Quali CloudShell Sandboxes v0.7')
	# creds
	parser.add_argument('-q', action="store", dest="host", help="server hostname for API session")
	parser.add_argument('-u', action="store", dest="un", help="username for API session")
	parser.add_argument('-p', action="store", dest="pw", help="password for API session")
	parser.add_argument('-d', action="store", dest="dom", help="domain for API session")
	# possibilities
	parser.add_argument('task', metavar='task', help="start, list, running, or publish")
	parser.add_argument('-s', action="store", dest="infile", help="in python script")
	parser.add_argument('-o', action="store", dest="outfile", help="name of script in portal")
	parser.add_argument('-i', action="store", dest="id", help="sandbox/blueprint id")
	parser.add_argument('-l', action="store", dest="length", help="sandbox duration length in min. Default is 30")
	parser.add_argument('-n', action="store", dest="name", help="Name of sandbox to be given. Default is From CLI")
	# flags
	parser.add_argument("-w", "--wait", help="wait until sandbox is completed until script returns", action="store_true")
	
	arg = parser.parse_args()

	phrases = {}
	phrases["start"] = ["start","run"]
	phrases["list"] = ["list","blueprint","blueprints"]
	phrases["running"] = ["running","ps","sandboxes","sandbox"]
	phrases["publish"] = ["publish","upload"]
	phrases["stop"] = ["stop","end","kill","rm","rmi"]

	homedir = expanduser("~")
    
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	
	if ((arg.host != None) and (arg.un != None) and (arg.pw != None) and (arg.dom != None)):
		QSHost = arg.host
		QSUn = arg.un
		QSPw = arg.pw
		QSDom = arg.dom
		
		cp = SafeConfigParser()
		cp.add_section("quali")
		cp.set('quali', 'host', QSHost)
		cp.set('quali', 'un', QSUn)
		cp.set('quali', 'pw', QSPw)
		cp.set('quali', 'dom', QSDom)
		
		with open(homedir+"/.qsclicreds", 'wb') as configfile:
			cp.write(configfile)
	
	elif (os.path.isfile(homedir+"/.qsclicreds")):
		cp = SafeConfigParser()
		cp.read(homedir+"/.qsclicreds")
		QSHost = cp.get('quali', 'host')
		QSUn = cp.get('quali', 'un')
		QSPw = cp.get('quali', 'pw')
		QSDom = cp.get('quali', 'dom')
	else:
		print "\nMust provide credentials or have a credential file\n"
		parser.print_help()
		exit(4)
	
	if (arg.task in phrases["list"]):
		# authentication
		token = authRest(QSHost, QSUn, QSPw, QSDom)
	
	        headers = {}
	        headers["Content-Type"] = "application/json"
	        headers["Accept"] = "application/json"
	        headers["Authorization"] = "Basic "+token
	
	        URI = QSHost+"/api/v1/blueprints"
	
	        # sandbox start request
	        sbsr = requests.get(URI, headers=headers, verify=False)
	        
	        sbrobj = json.loads(sbsr.text)
	
		tbl = Table()
		tbl.AddHeader(["Blueprint Name","Blueprint ID", "Availability"])
		for sandbox in sbrobj:
			tbl.AddRow([sandbox["name"] , sandbox["id"], sandbox["availability"]])
	
		tbl.Draw()
	
	elif (arg.task in phrases["running"]):
		token = authRest(QSHost, QSUn, QSPw, QSDom)
	
		headers = {}
		headers["Content-Type"] = "application/json"
		headers["Accept"] = "application/json"
		headers["Authorization"] = "Basic "+token
	
		URI = QSHost+"/api/v1/sandboxes"

		sbsr = requests.get(URI, headers=headers, verify=False)
		sbrobj = json.loads(sbsr.text)
	
		tbl = Table()
		tbl.AddHeader(["Sandbox ID","Sandbox Name", "From Blueprint", "Status"])
		for sandbox in sbrobj:
			tbl.AddRow([sandbox["id"] , sandbox["name"], sandbox["blueprint"]["name"], sandbox["state"]])
	
		tbl.Draw()s.get(URI, headers=headers, verify=False)
		sbrobj = json.loads(sbsr.text)
	
		tbl = Table()
		tbl.AddHeader(["Sandbox ID","Sandbox Name", "From Blueprint", "Status"])
		for sandbox in sbrobj:
			tbl.AddRow([sandbox["id"] , sandbox["name"], sandbox["blueprint"]["name"], sandbox["state"]])
	
		tbl.Draw()
	
	elif (arg.task in phrases["start"]):
		token = authRest(QSHost, QSUn, QSPw, QSDom)
	
		headers = {}
		headers["Content-Type"] = "application/json"
		headers["Accept"] = "application/json"
		headers["Authorization"] = "Basic "+token
	
		# reserve sandbox
	        body = {}
		if (arg.length != None):
			body["duration"] = "PT"+arg.length+"M"
		else:
	        	body["duration"] = "PT30M"  # ISO 8601 for 30 minutes
	
		if (arg.name != None):
	        	body["name"] = arg.name
		else:
			body["name"] = "From CLI"
	
		URI = QSHost+"/api/v1/blueprints/"+arg.id+"/start"
	
	        # sandbox start request
	        sbsr = requests.post(URI, data=json.dumps(body), headers=headers, verify=False)
	        
	        sbsrobj = json.loads(sbsr.text)
	
	        sandboxID = sbsrobj["id"]
	
		# wait to see if done
		if arg.wait:
			stdout.write("Starting sandbox and waiting for it to come up")
			stdout.flush()
			URI = QSHost+"/api/v1/sandboxes/"+sandboxID
			sbstate = "unknown"
			while (("Active" not in sbstate) and ("Ready" not in sbstate) and ("Error" not in sbstate)):
				sbsr = requests.get(URI, headers=headers, verify=False)
				sbrobj = json.loads(sbsr.text)
				sbstate = sbrobj["state"]
				stdout.write(".")
				stdout.flush()
				time.sleep(10)
			stdout.write("\n") 
			print
	
		print "\nStarted " + sandboxID + "\n"
	
	elif (arg.task in phrases["stop"]):
		token = authRest(QSHost, QSUn, QSPw, QSDom)
	
		headers = {}
		headers["Content-Type"] = "application/json"
		headers["Accept"] = "application/json"
		headers["Authorization"] = "Basic "+token
	
		URI = QSHost+"/api/v1/sandboxes/"+arg.id+"/stop"
		sbsr = requests.post(URI, headers=headers, verify=False)
		
		print "\nStopped " + arg.id + "\n"
	
	
	elif (arg.task in phrases["publish"]):
		# temp directory
		filename = "QS_PkgFile"+arg.outfile+"_"+str(random.randint(0,9999999))
		folder = "./"+filename
		os.makedirs(folder)
		
		# write the metadata out
		metadata = """<?xml version="1.0" encoding="utf-8"?>
		<Metadata xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.qualisystems.com/PackageMetadataSchema.xsd">
		  <CreationDate>18/03/2016 09:48:32</CreationDate>
		  <ServerVersion>6.4.0</ServerVersion>
		  <PackageType>CloudShellPackage</PackageType>
		</Metadata>"""
		writeFile(folder+"/metadata.xml", metadata)
		
		# write topo script
		os.makedirs(folder+"/Topology Scripts")
		os.rename(arg.infile, folder+"/Topology Scripts/"+arg.outfile+".py")
		
		# write tmp folder contents to zip
		zipf = zipfile.ZipFile(folder+".zip", 'w', zipfile.ZIP_DEFLATED)
		zipdir(folder+"/", zipf)
		zipf.close()
		
		# upload
		r = requests.put(QSHost+':9000/Api/Auth/Login', {"username": QSUn, "password": QSPw, "domain": QSDom}) 
		authcode = "Basic "+r._content[1:-1]
		fileobj = open(folder+".zip", 'rb')
		r = requests.post(QSHost+':9000/API/Package/ImportPackage',headers={"Authorization": authcode},files={"file": fileobj})
		
		print r._content
		print r.ok
		
		# delete temp folder and zip
		time.sleep(1)
		for root, dirs, files in os.walk(folder, topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))
		os.rmdir(folder)
		os.remove(folder+".zip")
	
	else:
		print "\nDidn't understand any task\n"
		parser.print_help()
		exit(5)
