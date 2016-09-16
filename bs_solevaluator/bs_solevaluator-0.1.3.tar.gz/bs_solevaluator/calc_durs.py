import math


def get_file_elements(lines):
    characteristics = list()
    parameters = list()
    for line_number, line in enumerate(lines):
        if "OR-days" in line and "Capacity" not in line:
            characteristics.append(float(line[0]))
        elif any(x in line for x in ["P1", "P2",  "P3"]):
            parameters = lines[line_number+1:]
            break
    for elem, param in enumerate(parameters):
        parameters[elem] = param[1:4]
    return parameters, characteristics


def read_file(instance):
    with open(instance, "r") as data_read:
        lines = data_read.readlines()
        return [line.split() for line in lines]


def parse_file(file_name):
    lines = read_file(file_name)
    return get_file_elements(lines)


def calc_mean(m, s, g):
    mean_t = g + math.e**(m+(s**2)/2)
    return mean_t


def export_stats(instance):
    parameters, characteristics = parse_file(instance)
    durations = list()
    for row in parameters:
        durations.append(calc_mean(float(row[0]), float(row[1]), float(row[2])))
    return durations
