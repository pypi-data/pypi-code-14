import os
import calc_durs
import calc_pis
import eval_solutil


def soleval(csv_file):
    """ Evaluates a solutions and exports the corresponding Performance Indicators."""
    parentdir = input("Input the main directory of the instances:")
    exportdir = input("Input the export directory:")
    sol_rows = eval_solutil.read_solution(csv_file)  # Reads the solution.csv file
    export_data = list()
    for row in sol_rows:
        path = os.path.join(parentdir, row[0])
        file = row[1] + ".txt"
        path = os.path.join(path, file)
        rooms = eval(row[1].split("_")[2])  # Gathers the number of ORs from the filename of the instance
        sol = eval_solutil.decoder(row[2])  # Decodes the code for the cost_eval() function
        durations = calc_durs.export_stats(path)  # Reads the file that contains the surgeries durations
        overtime, idletime, makespan = calc_pis.cost_eval(sol, durations, rooms)  # Calculates the PIs
        export_data.append(eval_solutil.ExpFile(row[0], row[1], overtime, idletime, makespan))  # Keeps the results in a class
        eval_solutil.csv_exporter(export_data, exportdir)  # Exports in csv
    print("Successfully exported!")
