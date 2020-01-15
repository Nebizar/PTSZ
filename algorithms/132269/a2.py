import sys
import time
import os
import random
from copy import deepcopy

machineNumbers = 4


class Task(object):
    def __init__(self, p, r, d, id):
        self.p = p
        self.r = r
        self.d = d
        self.id = id
        self.start = 0
        self.end = 0
        self.generatedDelay = 0


class Machine(object):
    def __init__(self, id):
        self.id = id
        self.tasks = []
        self.taskEnd = 0
        self.delay = 0

    def addTask(self, task):
        task.start = self.taskEnd
        if task.r > self.taskEnd:
            self.taskEnd = task.r
        self.taskEnd += task.p
        task.end = self.taskEnd
        if self.taskEnd > task.d:
            self.delay += (self.taskEnd - task.d)
            task.generatedDelay = (self.taskEnd - task.d)
        self.tasks.append(task)
    def simulateAddTask(self,task):
         return max(max(self.taskEnd,task.r) + task.p - task.d,0)


class Solution(object):
    def __init__(self, tardiness, tasksList, machinesList):
        self.tardiness = tardiness
        self.tasksList = tasksList
        self.machinesList = machinesList


def changeTasksList(tasks):
    idx = len(tasks)
    i1 = random.randrange(idx) - 1
    toChange = next((task for task in tasks if isWorthChanging(task, tasks[i1])), tasks[i1+1])
    i2 = tasks.index(toChange)
    tasks[i1], tasks[i2] = tasks[i2], tasks[i1]

def calculateSolution(tasksList):
    machinesList = [Machine(0),Machine(1),Machine(2),Machine(3)]
    for task in tasksList:
        delays = []
        for machine in machinesList:
            delay = machine.simulateAddTask(task)
            delays.append(delay)
        machinesList[delays.index(min(delays))].addTask(task)

    tardiness = sum(machine.delay for machine in machinesList)
    return Solution(tardiness, tasksList, machinesList)

def isWorthChanging(newTask, oldTask):
    if (max(max(newTask.start,oldTask.r) + oldTask.p - oldTask.d,0) + max(max(oldTask.start,newTask.r) + newTask.p - newTask.d,0) <= newTask.generatedDelay + oldTask.generatedDelay):
        return True
    return False

def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r")
    taskCount = int(file.readline())
    tasksList = []
    for number in range(0, int(taskCount)):
        task = file.readline()
        task = task.strip().split(' ')
        tasksList.append(Task(int(task[0]), int(task[1]), int(task[2]), number))
    file.close()

    tasksList = sorted(tasksList, key=lambda x: int(x.d))
    maxTime = time.time() + (0.01 * taskCount) - 0.3
    currentBestSolution = calculateSolution(deepcopy(tasksList))
    iterations = 0

    while (time.time() < maxTime ):
        oldTasksList = deepcopy(tasksList)
        changeTasksList(oldTasksList)
        solutionFitness = calculateSolution(oldTasksList)
        if(currentBestSolution.tardiness < solutionFitness.tardiness):
            print(solutionFitness.tardiness)
            print("Best solution: ", currentBestSolution.tardiness)
        else:
            currentBestSolution = solutionFitness
            tasksList = oldTasksList
            print("Best solution: ", solutionFitness.tardiness)
        iterations += 1
    print('Num of iterations: ',iterations)
    if not os.path.exists("results/" + "/132269/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132269/a2/" + sys.argv[1] + "/")
    file = open("results/" + "/132269/a2/" + sys.argv   [1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(currentBestSolution.tardiness) + "\n")
    for machine in currentBestSolution.machinesList:
        for task in machine.tasks:
            file.write(str(task.id + 1) + ' ')
        if (machine.id != 3):
            file.write('\n')
    file.close()


if __name__ == '__main__':
    main()