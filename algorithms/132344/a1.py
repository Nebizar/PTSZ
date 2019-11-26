import sys
import math
import os
import time

machineNumbers = 4

class Task(object):
    def __init__(self, p, r, d, id):
        self.p = p
        self.r = r
        self.d = d
        self.id = id


class Machine(object):
    def __init__(self, id):
        self.id = id
        self.tasks = []
        self.taskEnd = 0
        self.delay = 0
    def addTask(self,task):
        self.tasks.append(task)
        if task.r > self.taskEnd:
            self.taskEnd = task.r
        self.taskEnd += task.p
        if self.taskEnd > task.d:
            self.delay += (self.taskEnd - task.d)



def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r")
    number_of_rows = int(file.readline())
    tasksList = []
    # Getting task list to array (r,p,d) as object
    for number in range(0, int(number_of_rows)):
        line = file.readline()
        line = line.strip().split(' ')
        tasksList.append(Task(int(line[0]), int(line[1]), int(line[2]), number))
    file.close()
    # Calculated Value from file
    tardiness = 0
    machinesList = []
    # Create machines
    for id in range(0, machineNumbers):
        machinesList.append(Machine(id))

    # Sort tasks based on d
    tasksList = sorted(tasksList, key=lambda x: int(x.d))

    # start
    for task in tasksList:
        machine_curr = next(machine for machine in machinesList if machine.taskEnd == min(m.taskEnd for m in machinesList))
        machine_curr.addTask(task)

    tardiness = sum(machine.delay for machine in machinesList)

    if not os.path.exists("results/" + "/132344/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132344/a1/" + sys.argv[1] + "/")
    file = open("results/" + "/132344/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(tardiness) + "\n")
    for machine in machinesList:
        for task in machine.tasks:
            file.write(str(task.id + 1) + ' ')
        if(machine.id != 3):
            file.write('\n')
    file.close()



if __name__ == '__main__':
    main()
