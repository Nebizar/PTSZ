
import time

numbers = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
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


def sortFile(tasksNumbers):
    tasksFile = open("in/" + str(tasksNumbers) + ".txt", "r")
    outFile = open("out/" + str(tasksNumbers) + ".txt", "w+")
    # Skipping Line
    query = tasksFile.readline()
    tasksList = []
    # Getting task list to array (r,p,d) as object
    for number in range(0, tasksNumbers):
        line = tasksFile.readline()
        line = line.strip().split(' ')
        tasksList.append(Task(int(line[0]), line[1], line[2], number))

    # Calculated Value from file
    calculatedE = 0
    timeLine = 0
    machinesList = []
    # Create machines
    for id in range(0, machineNumbers):
        machinesList.append(Machine(id, False, 0))

    # Sort tasks based on R
    tasksList = sorted(tasksList, key=lambda x: x.r)
    # print(list(map(lambda x: x.r, tasksList)))z

    # Continue if there is any task to put on machine
    while len(tasksList) != 0:
        # Check every machine
        for machine in machinesList:
            if(machine.isOcuppied): 
                if(machine.shouldEnd <= timeLine):
                    machine.isOcuppied = False

            if(not(machine.isOcuppied)):
                # Get task with lowest 'r' value
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
    

    outFile.write(str(calculatedE) + '\n')
    for machine in machinesList:
        for task in machine.tasks:
            outFile.write(str(task.id + 1) + ' ')
        if(machine.id != 3):
            outFile.write('\n')
    return calculatedE
    

print("Czas trwania algorytmu dla poszczegolnych instancji:")
results = []
for number in numbers:
    start = time.time()
    calc = sortFile(number)
    end = time.time()
    results.append(calc)
    print("%.5f" % (end - start))
print("\n")
print("Wynik E:")
for i in results:
    print(i)
