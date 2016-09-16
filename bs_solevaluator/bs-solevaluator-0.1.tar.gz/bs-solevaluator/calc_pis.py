def calc_duration(solution, duration, rooms):  # Calculates the ORs final capacity
    total_duration = [0]*rooms
    for room in range(rooms):
        for surgery in range(len(solution[room])):
            if solution[room][surgery] == -1:  # There are ORs that contain 0 surgeries
                total_duration[room] = -480  # -480 means Idletime of 480 minutes
            else:
                surg = solution[room][surgery]
                surg -= 1  # Substracts 1 cause Python starts from 0
                total_duration[room] += duration[surg]
    return total_duration


def calc_overtime(total_duration):  # Calculates the Overtime of the ORs
    over_time = list()
    for room_duration in total_duration:
        if room_duration == -480:
            over_time.append(0)
        else:
            if 480 - room_duration >= 0:
                over_time.append(0)
            else:
                over_time.append(room_duration - 480)
    return sum(over_time)/len(over_time)


def calc_idletime(total_duration):  # Calculates the Idletime of the ORs
    idle_time = list()
    for room_duration in total_duration:
        if room_duration == - 480:
            idle_time.append(480)
        else:
            if 480 - room_duration > 0:
                idle_time.append(480 - room_duration)
            else:
                idle_time.append(0)
    return sum(idle_time)/len(total_duration)


def calc_makespan(total_duration):  # Returns the max value from the Makespan list
    return max(total_duration)


def cost_eval(solution, duration, rooms):  # Main function - returns the PIs
    total_duration = calc_duration(solution, duration, rooms)
    overtime = calc_overtime(total_duration)
    idletime = calc_idletime(total_duration)
    makespan = calc_makespan(total_duration)
    return overtime, idletime, makespan
