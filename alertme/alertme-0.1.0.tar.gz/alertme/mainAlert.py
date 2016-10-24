import sys, traceback, getpass, smtplib, argparse, importlib, subprocess
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from datetime import datetime
from email.MIMEBase import MIMEBase
from email import encoders
from subprocess import Popen

sys.dont_write_bytecode = True #Prevents .pyc files from cluttering the cwd

parser = argparse.ArgumentParser()
parser.add_argument("file",help="alert when this script is done running")
parser.add_argument("-o","--output", action="store_true",help="redirect output to a file from stdout")
parser.add_argument("-s","--subject",action="store_true",help="add a subject on the notification email")
parser.add_argument("-b","--bash",action="store_true",help="run a bash script instead of a python script")
commandLineArgs = parser.parse_args()
executeFile = commandLineArgs.file

#Check if its a bash or python script
if commandLineArgs.bash:
	if not executeFile.endswith('.sh'):
		print("File must end in .sh")
		sys.exit(0)
	pythonOrBash = "bash"
	if executeFile.startswith("./"):
		executeFile = executeFile[2:]
elif not commandLineArgs.bash:
	if not executeFile.endswith('.py'):
		print("File must end in .py")
		sys.exit(0)
	elif executeFile.endswith('.sh'):
		print("Bash option [-b] must be used")
	pythonOrBash = "python"
	if executeFile.startswith("./"):
		executeFile = executeFile[2:]

#Get Gmail Information
fromaddr = raw_input("Enter your gmail address: ")
fromaddr = fromaddr.strip()
while not fromaddr.endswith('@gmail.com'):
	fromaddr = raw_input("Please enter a valid Gmail address: ")
	fromaddr = fromaddr.strip()
psswd = getpass.getpass("Password: ")

#If -s option is given
if commandLineArgs.subject:
	sub = raw_input("Enter a subject line: ")
else: sub = "Your " + executeFile + " script from AlertMe"

#Create message
message = MIMEMultipart()
message['From'] = fromaddr
message['To'] = fromaddr #Currently the script will send an email from your own account
message['Subject'] = sub
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

#Login to server with the given credentials
try:
	server.login(fromaddr,psswd)
	print("Logged in successfully!")
except Exception:
	print("Login failed. Please check your username or password")
	server.quit()
	sys.exit(0)

#Run the executeFile
err = None
if pythonOrBash == "bash":
	try:
		#Check for file output option
		if commandLineArgs.output:
			with open(executeFile + ".AlertMe.out.txt","w") as outfile:
				outfile.write("AlertMe: Script started on: " + str(datetime.today()) + " at " + str(datetime.now().time()) + "\n\n")
				proc = subprocess.Popen(["./" + executeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				out, err = proc.communicate()
				outfile.write(out)
				if not err == "":
					with open(executeFile + ".AlertMe.err.txt","w") as errfile:
						errfile.write(err)
						err="check_file"
		else:
			proc = subprocess.Popen(["./" + executeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			out, err = proc.communicate()
			print(out)
			if not err == "":
				print("Errors in your script: " + "\n")
				print(err)
	except OSError: #Will be raised when trying to execute a non-existent file
		print("Bash script could not be imported. Make sure the file exists in the current directory")
		sys.exit(0)
	except Exception:
		err = traceback.format_exc()
else:
	try:
		#Check for file output option
		'''if commandLineArgs.output:
			with open(executeFile + ".AlertMe.out.txt","w") as outfile:
				outfile.write("AlertMe: Script started on: " + str(datetime.today()) + " at " + str(datetime.now().time()) + "\n\n")
				try:
					outfile.write(subprocess.check_output(["python", executeFile],stderr=subprocess.STDOUT))
				except subprocess.CalledProcessError as e:
					outfile.write(e.output)
					err = "out"
		else:
			if executeFile.endswith(".py"):
				executeFile = executeFile[:-3]
			try:
				module = __import__(executeFile)
			except Exception as e:
				err = str(e)'''
		if commandLineArgs.output:
			with open(executeFile + ".AlertMe.out.txt","w") as outfile:
				outfile.write("AlertMe: Script started on: " + str(datetime.today()) + " at " + str(datetime.now().time()) + "\n\n")
				proc = subprocess.Popen(["python", executeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
				out, err = proc.communicate()
				outfile.write(out)
				if not err == "":
					with open(executeFile + ".AlertMe.err.txt","w") as errfile:
						errfile.write(err)
						err="check_file"
		else:
			proc = subprocess.Popen(["python", executeFile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			out, err = proc.communicate()
			print(out)
			if not err == "":
				print("Errors in your script: " + "\n")
				print(err)
	except NameError: #Raise ImportError and terminate program
		#IMPORTERROR WILL BE THROWN IF EXECUTEFILE IS NOT IN THE SAME DIRECTORY
		print("Python script could not be imported. Make sure the file exists in the current directory")
		sys.exit(0)
	except Exception:
		err = traceback.format_exc()

#Format body of the email
if err == "":
	if commandLineArgs.output:
		body = "Your " + pythonOrBash + " script has finished running! There were no errors. Your output file is attached." + "\n\n" + "Happy coding, " + "\n\n" + "AlertMe"
	else:
		body = "Your " + pythonOrBash + " script has finished running! There were no errors." + "\n\n" + "Happy coding, " + "\n\n" + "AlertMe"
elif err == "check_file":
	body = "Your " + pythonOrBash + " script has encountered an error. Both the output and the error file have been attached. Please check the error file (.err) to see what went wrong." + "\n\n" + "Happy coding, " + "\n\n" + "AlertMe"
else:
	body = "Your " + pythonOrBash + " script has encountered the following error: " + "\n\n" + err + "\n\n" + "Happy coding, " + "\n\n" + "AlertMe"

message.attach(MIMEText(body,'plain'))


#Attach output file
if commandLineArgs.output:
	outfilename = executeFile + ".AlertMe.out.txt"
	attachments = [outfilename]
	if err == "check_file":
		errfilename = executeFile + ".AlertMe.err.txt"
		attachments.append(errfilename)
	#all of this needs to run for every attachment
	for attachFile in attachments:
		with open(attachFile) as f:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((f).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % attachFile)
			message.attach(part)

text = message.as_string()

#Send the email
try:
	server.sendmail(fromaddr, fromaddr, text)
	print("Email sent successfully")
except Exception:
	print("Email could not be sent")
	server.quit()
	sys.exit(0)
