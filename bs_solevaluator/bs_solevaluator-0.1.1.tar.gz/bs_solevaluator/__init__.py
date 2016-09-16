import os
from calc_durs import *
from calc_pis import *
from eval_solutil import *



def soleval(csv_file):
    """ Evaluates a solutions and exports the corresponding Performance Indicators."""
    parentdir = input("Input the main directory of the instances:")
    exportdir = input("Input the export directory:")
    sol_rows = read_solution(csv_file)  # Reads the solution.csv file
    export_data = list()
    for row in sol_rows:
        path = os.path.join(parentdir, row[0])
        file = row[1] + ".txt"
        path = os.path.join(path, file)
        rooms = eval(row[1].split("_")[2])  # Gathers the number of ORs from the filename of the instance
        sol = decoder(row[2])  # Decodes the code for the cost_eval() function
        durations = export_stats(path)  # Reads the file that contains the surgeries durations
        overtime, idletime, makespan = cost_eval(sol, durations, rooms)  # Calculates the PIs
        export_data.append(ExpFile(row[0], row[1], overtime, idletime, makespan))  # Keeps the results in a class
    csv_exporter(export_data, exportdir)  # Exports in csv
    print("Successfully exported!")


name = "/Users/DjPanosG/Desktop/Database/Experiments/FF_FCFS_Overtime/1 RealLifeSurgeryTypesDatabase_SOLUTIONS_.csv"
soleval(name)