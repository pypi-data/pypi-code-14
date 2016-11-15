from IBMQuantumExperience import IBMQuantumExperience

api = IBMQuantumExperience("admin@ibm.quantum.com", "7N75G\\c!", {"url": 'https://qcwi-develop.mybluemix.net/api'})
print(api.getImageCode('6a762de4151fc9ab01efacf69a17dfdd'))