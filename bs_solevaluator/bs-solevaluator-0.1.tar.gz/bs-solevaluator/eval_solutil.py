import csv
import os


class ExpFile:  # Class keeping the PIs
    def __init__(self, type, filename, overtime, idletime, makespan):
        self.type = type
        self.filename = filename
        self.overtime = overtime
        self.idletime = idletime
        self.makespan = makespan


def read_solution(csv_file):  # Reads the solution.csv file
    with open(csv_file, "r", newline='') as out:
        data = csv.reader(out, delimiter=",")
        next(data, None)  # Will not input contain the headers
        solution = [[row[0], row[1], eval(row[2])] for row in data]
    return solution


def decoder(sol):  # Decodes to list of lists
    rooms = sol.count("#")
    solution = [[] for i in range(rooms)]
    count = 0
    for i in sol:
        if i == "#":
            count += 1
        else:
            solution[count-1].append(i)
    return solution


def read_instance(instance_path): # Reads the durations from the instance
    print('Reading {} ...'.format(instance_path))
    with open(instance_path, "r") as out:
        data = csv.reader(out)
        next(data, None)  # Will not input contain the headers to the list.
        durations = [eval(row[1]) for row in data] # Reads mean and standard deviation
    return durations


def csv_exporter(export_data, exportdir):  # Exports the results, in predefined path
    path = os.path.join(exportdir, 'pis_output.csv')
    data = open(path, 'w')
    output = csv.writer(data)
    output.writerow(["Type", "Name", "Overtime/OR", "Idletime/OR", 'Makespan'])
    for row in export_data:
        outrow = list()
        outrow.append(row.type)
        outrow.append(row.filename)
        outrow.append(row.overtime)
        outrow.append(row.idletime)
        outrow.append(row.makespan)
        output.writerow(outrow)
    data.close()
