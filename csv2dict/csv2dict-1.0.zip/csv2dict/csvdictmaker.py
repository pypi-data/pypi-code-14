import csv

def read(path, fields, keyField, delimiter=','):
	with open(path, 'r') as csvFile:
		reader = csv.DictReader(csvFile, fieldnames=fields)
		csvDict = {}
		for line in reader:
			lineDict = {}
			for field in fields:
				lineDict[field] = line[field]
			csvDict[line[keyField]] = lineDict
	return csvDict
