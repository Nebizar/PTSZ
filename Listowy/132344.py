import sys
import math
import os
import time

machineNumbers = 4

class Task(object):
    def __init__(self, p, r, d, id):
        self.r = r
        self.p = p
        self.d = d
        self.id = id


class Machine(object):
    def __init__(self, id, isOcuppied, shouldEnd):
        self.id = id
        self.isOcuppied = isOcuppied
        self.tasks = []
        self.shouldEnd = shouldEnd

def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r")
    number_of_rows = int(file.readline())
    tasksList = []
    # Getting task list to array (r,p,d) as object
    for number in range(0, int(number_of_rows)):
        line = file.readline()
        line = line.strip().split(' ')
        tasksList.append(Task(int(line[0]), line[1], line[2], number))
    file.close()
    # Calculated Value from file
    calculatedE = 0
    timeLine = 0
    machinesList = []
    # Create machines
    for id in range(0, machineNumbers):
        machinesList.append(Machine(id, False, 0))

    # Sort tasks based on d
    tasksList = sorted(tasksList, key=lambda x: int(x.d))

    # Continue if there is any task to put on machine
    while len(tasksList) != 0:
        # Check every machine
        for machine in machinesList:
            if(machine.isOcuppied): 
                if(machine.shouldEnd <= timeLine):
                    machine.isOcuppied = False

            if(not(machine.isOcuppied)):
                # Get task with lowest 'd' value
                testedTask = tasksList[0]
                if(timeLine >= int(testedTask.r)):
                    # Start task on machine
                    machine.isOcuppied = True
                    machine.tasks.append(testedTask)
                    machine.shouldEnd = timeLine + int(testedTask.p)
                    calculatedE = calculatedE + max(0, machine.shouldEnd - int(testedTask.d))
                    tasksList.pop(0)
                    if (len(tasksList) == 0):
                        break
        timeLine = timeLine + 1
    
    if not os.path.exists("results/" + "/132344/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132344/a1/" + sys.argv[1] + "/")
    file = open("results/" + "/132344/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(calculatedE) + "\n")
    for machine in machinesList:
        for task in machine.tasks:
            file.write(str(task.id + 1) + ' ')
        if(machine.id != 3):
            file.write('\n')
    file.close()



if __name__ == '__main__':
    main()
