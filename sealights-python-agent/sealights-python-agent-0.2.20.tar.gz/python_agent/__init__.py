from python_agent.packages import requests
from python_agent.packages.requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "0.2.20"
