import glob
import os
import sys


class Task:
    def __init__(self, idT, d, rT, dD):
        self.id = idT
        self.readyTime = rT
        self.dueDate = dD
        self.duration = d

    def __lt__(self, other):
        if self.readyTime != other.readyTime:
            return self.readyTime + self.dueDate < other.readyTime + other.dueDate
        return (self.dueDate - self.readyTime - self.duration) < (other.dueDate - other.readyTime - other.duration)


class Machine:
    def __init__(self, time):
        self.time = time
        self.lineOfTasks = []
        self.penalty = 0

    def addTask(self, task):
        self.lineOfTasks.append(task.id)
        calculatedPoints = 0
        if task.readyTime < self.time:
            self.time += task.duration
        else:
            self.time = task.readyTime + task.duration
        if self.time - task.dueDate > 0:
            calculatedPoints += self.time - task.dueDate
        self.penalty += calculatedPoints


class Alg:
    def __init__(self, tasksList):
        self.tasksList = tasksList
        self.points = 0
        self.machines = []
        for i in range(0, 4):
            self.machines.append(Machine(0))

    def tasksline(self):
        self.tasksList.sort()
        for task in self.tasksList:
            self.machines[self.chooseMach()].addTask(task)

    def chooseMach(self):
        minMachTime = float('inf')
        minMachId = 1
        for m in range(0, 4):
            if minMachTime > self.machines[m].time:
                minMachTime = self.machines[m].time
                minMachId = m
        return minMachId

    def calcPoints(self):
        for m in range(0, 4):
            self.points += self.machines[m].penalty

    def summary(self, f):
        f.write("%d" % self.points)
        for i in range(0, 4):
            f.write("\n" + ' '.join(str(v) for v in self.machines[i].lineOfTasks))


if __name__ == "__main__":
    instance_path = os.path.join("instances", sys.argv[1], "{}.txt".format(sys.argv[2]))
    result_path = os.path.join("results", "132313", "a1", sys.argv[1])
    tasksList = []
    id = 1
    fr = open(instance_path, "r")
    fl = fr.readlines()
    for x in fl:
        splitted = x.rstrip().split(" ")
        if len(splitted) == 1:
            instance = splitted[0]
        else:
            t = Task(id, int(splitted[0]), int(splitted[1]), int(splitted[2]))
            tasksList.append(t)
            id += 1
    os.makedirs(os.path.dirname(result_path), exist_ok=True)
    w = Alg(tasksList)
    w.tasksline()
    w.calcPoints()
    if not os.path.exists("results/" + "/132313/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132313/a1/" + sys.argv[1] + "/")
    fw = open("results/" + "/132313/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    w.summary(fw)
    fw.close()
    fr.close()
