import glob
import os
import sys
import operator
import random
import copy
import time

class Task:
    def __init__(self, idT, d, rT, dD):
        self.id = idT
        self.readyTime = rT
        self.dueDate = dD
        self.duration = d

    def __str__(self):
        return str(self.id)


class Machine:
    def __init__(self):
        self.time = 0
        self.sumDurationTime = 0
        self.lineOfTasks = []
        self.penalty = 0

    def insertTask(self, index, task):
        self.lineOfTasks.insert(index, task)

    def addTask(self, task):
        self.lineOfTasks.append(task)
        calculatedPoints = 0
        if task.readyTime < self.time:
            self.time += task.duration
        else:
            self.time = task.readyTime + task.duration
        if self.time - task.dueDate > 0:
            calculatedPoints += self.time - task.dueDate
        self.penalty += calculatedPoints
        self.sumDurationTime += task.duration

    def calcPenalty(self):
        self.penalty = 0
        self.time = 0
        for task in self.lineOfTasks:
            if task.readyTime < self.time:
                self.time += task.duration
            else:
                self.time = task.readyTime + task.duration
            if self.time - task.dueDate > 0:
                self.penalty += self.time - task.dueDate


class Chromosome:
    def __init__(self):
        self.points = -1
        self.machines = []
        for i in range(0, 4):
            mach = Machine()
            self.machines.append(mach)

    def addMachines(self, machines):
        self.machines = machines

    def calcMachinePoints(self):
        self.points = 0
        for m in range(0, 4):
            self.machines[m].calcPenalty()
            self.points += self.machines[m].penalty


class GeneticAlgorithm:
    def __init__(self, tasksList, sumDurationPerMachine):
        self.bestChromosome = 0
        self.sumDurationPerMachine = sumDurationPerMachine
        self.population = []
        self.population.append(ListAlgorithm(tasksList).sortLambda12())
        self.population.append(ListAlgorithm(tasksList).sortLambda21())
        self.population.append(ListAlgorithm(tasksList).sortLambda13())
        self.population.append(ListAlgorithm(tasksList).sortLambda23())
        self.population.append(ListAlgorithm(tasksList).sortLambda1())
        self.population.append(ListAlgorithm(tasksList).sortLambda2())
        self.population.append(ListAlgorithm(tasksList).sortLambda3())
        self.population.append(ListAlgorithm(tasksList).groupMachines())

    def iteration(self):
        parent_1 = random.choice(self.population)
        parent_2 = random.choice(self.population)
        output = self.crossing(parent_1, parent_2)
        for ch in output:
            self.population.append(ch)
            self.population.append(self.balance(ch))
        for _ in range(10):
            mutation_parent = random.choice(self.population)
            child = self.mutation(mutation_parent);
            self.population.append(child)
        for gen in self.population:
            gen.calcMachinePoints()
        self.population = sorted(self.population, key=lambda x: (x.points))
        self.population = self.population[:100]


    def crossing(self, parent_1, parent_2):
        listOftasks = [1 for i in range(1, instance + 2)]
        machinesPoints = [-1 for i in range(4)]
        if(self.sumDurationPerMachine > 10):
            timeStamp = 10 + random.randrange(int(self.sumDurationPerMachine) - 10)
        else:
            timeStamp = random.randrange(int(self.sumDurationPerMachine))
        child1 = Chromosome()
        machineList = self.checkSimilarity(parent_1, parent_2)
        count = 0
        for i in range(0, 4):
            j = 0
            while child1.machines[i].sumDurationTime < timeStamp and j < len(parent_1.machines[i].lineOfTasks):
                task = parent_1.machines[i].lineOfTasks[j]
                j += 1
                if listOftasks[task.id] == 1:
                    listOftasks[task.id] = 0
                    child1.machines[i].addTask(task)
                    count+=1
                    machinesPoints[i] = j
            currentTime = 0
            for x in parent_2.machines[machineList[i]].lineOfTasks:
                currentTime += x.duration
                if currentTime > timeStamp and listOftasks[x.id] == 1:
                    listOftasks[x.id] = 0
                    child1.machines[i].addTask(x)
                    count+=1
        output = [child1]
        if count != instance:
            missing_list = [i for i in range(1, len(listOftasks)) if listOftasks[i] == 1]
            middleChild = copy.deepcopy(child1)
            permutChild = copy.deepcopy(child1)
            endChild = copy.deepcopy(child1)
            randomChild = copy.deepcopy(child1)
            for i in range(0, 4):
                insertedElements = []
                for x in missing_list:
                    for y in parent_2.machines[i].lineOfTasks:
                        if x == y.id:
                            insertedElements.append(y)
                sequence = self.makeSequence(insertedElements)
                middleChild.machines[i].lineOfTasks[machinesPoints[i]:machinesPoints[i]] = sequence
                for seq in sequence:
                    endChild.machines[i].lineOfTasks.append(seq)
                permSeq = random.sample(sequence, len(sequence))
                permutChild.machines[i].lineOfTasks[machinesPoints[i]:machinesPoints[i]] = permSeq
                for t in sequence:
                    randomPlace = random.randrange(len(randomChild.machines[i].lineOfTasks))
                    randomChild.machines[i].lineOfTasks.insert(randomPlace, t)
            output = [middleChild, permutChild, endChild, randomChild]
        return output

    def crossing1(self, parent_1, parent_2):
        listOftasks = [1 for i in range(1, instance + 2)]
        machinesList1 = [0, 1, 2, 3]
        machinesList2 = random.sample(machinesList1, len(machinesList1))
        child1 = copy.deepcopy(parent_1)
        child2 = copy.deepcopy(parent_2)
        count1 = 0
        count2 = 0
        for i in range(0,4):
            minNumber = min(len(parent_1.machines[machinesList1[i]].lineOfTasks),len(parent_2.machines[machinesList2[i]].lineOfTasks))
            randomCut = random.randrange(minNumber)
            child1.machines[machinesList1[i]].lineOfTasks = child1.machines[machinesList1[i]].lineOfTasks[:randomCut] + child2.machines[machinesList2[i]].lineOfTasks[-randomCut:]
            child2.machines[machinesList2[i]].lineOfTasks = child2.machines[machinesList2[i]].lineOfTasks[:randomCut] + child1.machines[machinesList1[i]].lineOfTasks[-randomCut:]
            output = [child1, child2]
            count1 += len(child1.machines[machinesList1[i]].lineOfTasks)
            count2 += len(child2.machines[machinesList2[i]].lineOfTasks)
        if count1 != instance:
            missing_list = [i for i in range(1, len(listOftasks)) if listOftasks[i] == 1]
            for i in range(0, 4):
                insertedElements = []
                for x in missing_list:
                    for y in parent_2.machines[i].lineOfTasks:
                        if x == y.id:
                            insertedElements.append(y)
                sequence = self.makeSequence(insertedElements)
                point = len(child1.machines[machinesList1[i]].lineOfTasks) - 1
                child1.machines[machinesList1[i]].lineOfTasks[point:point] += sequence
        if count2 != instance:
            missing_list = [i for i in range(1, len(listOftasks)) if listOftasks[i] == 1]
            for i in range(0, 4):
                insertedElements = []
                for x in missing_list:
                    for y in parent_2.machines[i].lineOfTasks:
                        if x == y.id:
                            insertedElements.append(y)
                sequence = self.makeSequence(insertedElements)
                point = len(child2.machines[machinesList2[i]].lineOfTasks) - 1
                child2.machines[machinesList2[i]].lineOfTasks[point:point] += sequence
        return output


    def mutation(self, parent):
        child = copy.deepcopy(parent)
        randomMachine1 = random.randrange(4)
        randomMachine2 = random.randrange(4)
        randomTask1 = random.randrange(len(child.machines[randomMachine1].lineOfTasks))
        randomTask2 = random.randrange(len(child.machines[randomMachine2].lineOfTasks))
        tmp = child.machines[randomMachine1].lineOfTasks[randomTask1]
        child.machines[randomMachine1].lineOfTasks[randomTask1] = child.machines[randomMachine2].lineOfTasks[randomTask2]
        child.machines[randomMachine2].lineOfTasks[randomTask2] = tmp
        return child

    def balance(self, parent):
        child = copy.deepcopy(parent)
        level = 0
        min = 10000
        min_index = 0
        max = 0
        max_index = 0
        while level > 1:
            for i in range(0, 4):
                if min > len(child.machines[i].lineOfTasks):
                    min = len(child.machines[i].lineOfTasks)
                    min_index = i
                if max < len(child.machines[i].lineOfTasks):
                    max = len(child.machines[i].lineOfTasks)
                    max_index = i
            level = max - min
            for _ in range(0, level):
                child.machines[max_index].lineOfTasks.append(child.machines[min_index].lineOfTasks)
        return child

    def makeSequence(self, insertedElements):
        insertedElements = sorted(insertedElements, key=lambda x: (x.readyTime, x.duration))
        return insertedElements

    def checkSimilarity(self, chromosome1, chromosome2):
        machinesOutput = [-1 for i in range(4)]
        machinesList = [0, 1, 2, 3]
        for i in range(0, 4):
            listOfX = [0 for i in range(1, instance + 2)]
            for x in chromosome1.machines[i].lineOfTasks:
                listOfX[x.id] = 1
            index = -1
            max = -1
            for machine in machinesList:
                count = 0
                for x in chromosome2.machines[machine].lineOfTasks:
                    if listOfX[x.id] == 1:
                        count += 1
                if count > max:
                    max = count
                    index = machine
            machinesOutput[i] = index
            machinesList.remove(index)
        return machinesOutput


    def calcMachinePoints(self):
        for m in range(0, 4):
            self.points += self.machines[m].penalty

    def summary(self, f):
        f.write("%d" % self.population[0].points)
        for i in range(0, 4):
            f.write("\n" + ' '.join(str(v.id) for v in self.population[0].machines[i].lineOfTasks))


class ListAlgorithm:
    def __init__(self, tasksList):
        self.tasksList = tasksList
        self.points = 0
        self.machines = []
        for i in range(0, 4):
            self.machines.append(Machine())

    def groupMachines(self):
        while len(self.tasksList) > 0:
            mach = self.chooseMach()
            proposal = [task for task in self.tasksList if task.readyTime <= self.machines[mach].time]
            if not proposal:
                minReady = min(self.tasksList, key=operator.attrgetter('readyTime'))
                proposal = [task for task in self.tasksList if task.readyTime == minReady.readyTime]
            task = min(proposal, key=operator.attrgetter('duration'))
            self.machines[mach].addTask(task)
            self.tasksList.remove(task)
        chromo = Chromosome()
        chromo.addMachines(self.machines)
        chromo.calcMachinePoints()
        return chromo

    def sortLambda12(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.readyTime, x.dueDate))
        return self.tasksLine()

    def sortLambda21(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.dueDate, x.readyTime))
        return self.tasksLine()

    def sortLambda13(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.readyTime, x.duration))
        return self.tasksLine()

    def sortLambda23(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.dueDate, x.duration))
        return self.tasksLine()

    def sortLambda1(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.readyTime, x.dueDate - x.readyTime - x.duration))
        return self.tasksLine()

    def sortLambda2(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.readyTime + x.dueDate, x.dueDate - x.readyTime - x.duration))
        return self.tasksLine()

    def sortLambda3(self):
        self.tasksList = sorted(self.tasksList, key=lambda x: (x.readyTime + x.dueDate, x.dueDate - x.readyTime))
        return self.tasksLine()

    def tasksLine(self):
        for task in self.tasksList:
            self.machines[self.chooseMach()].addTask(task)
        chromo = Chromosome()
        chromo.addMachines(self.machines)
        return chromo

    def chooseMach(self):
        minMachTime = float('inf')
        minMachId = 1
        for m in range(0, 4):
            if minMachTime > self.machines[m].time:
                minMachTime = self.machines[m].time
                minMachId = m
        return minMachId


instance = -1

if __name__ == "__main__":
    start_time = time.time()
    instance_path = os.path.join("instances", sys.argv[1], "{}.txt".format(sys.argv[2]))
    result_path = os.path.join("results", "132313", "a2", sys.argv[1])
    tasksList = []
    id = 1
    fr = open(instance_path, "r")
    fl = fr.readlines()
    sumDuration = 0
    for x in fl:
        splitted = x.rstrip().split(" ")
        if len(splitted) == 1:
            instance = int(splitted[0])
        else:
            t = Task(id, int(splitted[0]), int(splitted[1]), int(splitted[2]))
            sumDuration += int(splitted[0])
            tasksList.append(t)
            id += 1
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    genetic = GeneticAlgorithm(tasksList, sumDuration / 4)
    bound = start_time + 0.01 * (instance - 4)
    while(time.time() < bound):
        genetic.iteration()
    print(time.time() - start_time)
    if not os.path.exists("results/" + "/132313/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132313/a2/" + sys.argv[1] + "/")
    fw = open("results/" + "/132313/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    genetic.summary(fw)
    fw.close()
    fr.close()