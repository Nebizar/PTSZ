import sys
import math
import os
import time
import random

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

class Solution(object):
    def __init__(self, tardiness, tasksList, machinesList):
        self.tardiness = tardiness
        self.tasksList = tasksList
        self.machinesList = machinesList

def swapArray(seq):
    idx = range(len(seq))
    i1, i2 = random.sample(idx, 2)
    seq[i1], seq[i2] = seq[i2], seq[i1]

def calculateSolution(tasksList):
    tardiness = 0
    machinesList = []

    for id in range(0, machineNumbers):
        machinesList.append(Machine(id))

    for task in tasksList:
        machine_curr = next(machine for machine in machinesList if machine.taskEnd == min(m.taskEnd for m in machinesList))
        machine_curr.addTask(task)

    tardiness = sum(machine.delay for machine in machinesList)
    return Solution(tardiness, tasksList, machinesList)

def generatePopulation(tasksList, numOfSwaps, populationSize):
    population = []
    for _ in range(populationSize):
        newList = tasksList
        for _ in range(numOfSwaps):
            swapArray(newList)
        population.append(newList)
    return population

def calculatePopulation(population):
    solutionsList = []
    for item in population:
        solutionsList.append(calculateSolution(item))
    return solutionsList

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

    # Sort tasks based on d - first input EDD
    tasksList = sorted(tasksList, key=lambda x: int(x.d))

    # Magic below - parameters
    populationSize = 1000
    numOfGenerations = 10
    numOfSwaps = int(len(tasksList) * 0.05)

    bestSolutionEver = None

    for generation in range(numOfGenerations):
        print("Generation : ", generation)
        population = []
        solutions = []

        population = generatePopulation(tasksList, numOfSwaps, populationSize)
        solutions = calculatePopulation(population)

        bestSolutionFromPopulation = min(solutions, key=lambda x: x.tardiness)
        print("Best solution : ", bestSolutionFromPopulation.tardiness)

        if(bestSolutionEver == None or bestSolutionEver.tardiness > bestSolutionFromPopulation.tardiness):
            bestSolutionEver = bestSolutionFromPopulation
            tasksList = bestSolutionEver.tasksList

    # Output to file
    print("Best solution ever: ", bestSolutionEver.tardiness)
    if not os.path.exists("results/" + "/132344/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132344/a2/" + sys.argv[1] + "/")
    file = open("results/" + "/132344/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(bestSolutionEver.tardiness) + "\n")
    for machine in bestSolutionEver.machinesList:
        for task in machine.tasks:
            file.write(str(task.id + 1) + ' ')
        if(machine.id != 3):
            file.write('\n')
    file.close()



if __name__ == '__main__':
    main()
