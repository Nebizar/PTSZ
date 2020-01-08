import os
import sys
import random
import math
from copy import deepcopy
from timeit import default_timer as timer


class BestOrder:
    def __init__(self, order, tardiness, tardinessOnEachProcessor):
        self.order = order
        self.tardiness = tardiness
        self.tardinessOnEachProcessor = tardinessOnEachProcessor


class RandomTask:
    def __init__(self, index, procIndex, value):
        self.index = index
        self.procIndex = procIndex
        self.value = value


def readTasks(i, instance_file_path):
    tasks = []
    p = []
    r = []
    d = []
    file = open(instance_file_path, "r")
    noTasks = file.readline()
    lines = file.readlines()
    for line in lines:
        line = line.split()
        p.append(line[0])
        r.append(line[1])
        d.append(line[2])
    p = list(map(int, p))
    r = list(map(int, r))
    d = list(map(int, d))
    tasks.append(p)
    tasks.append(r)
    tasks.append(d)
    return tasks, noTasks


def sortTasks(tasks, i):
    indexes = []
    tempArray = []
    reformedTasks = []
    tasks_r = []
    for x in range(0, int(i)):
        tempArray.append(x)
        tempArray.append(tasks[0][x])
        tempArray.append(tasks[1][x])
        tempArray.append(tasks[2][x])
        indexes.append(x + 1)
        reformedTasks.append(tempArray)
        tasks_r.append(tempArray)
        tempArray = []
    reformedTasks.sort(key=lambda x: (x[3], x[2]))
    tasks_r.sort(key=lambda x: (x[2], x[3]))
    return reformedTasks, tasks_r


def orderTasks(tasks_d, tasks_r, i, times, taskOrder, ds):
    for y in range(0, int(i)):
        processor_no = times.index((min(times)))
        if times[processor_no] >= tasks_d[0][2]:
            times[processor_no] = times[processor_no] + tasks_d[0][1]
            taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
            del tasks_r[tasks_r.index(tasks_d[0])]
            del tasks_d[0]
        else:
            if (times[processor_no] >= tasks_r[0][2]):
                times[processor_no] = times[processor_no] + tasks_r[0][1]
                taskOrder[processor_no].append(str(tasks_r[0][0] + 1))
                del tasks_d[tasks_d.index(tasks_r[0])]
                del tasks_r[0]
            elif ((tasks_d[0][3] - tasks_d[0][2] - tasks_d[0][1]) > (tasks_r[0][3] - tasks_r[0][2] - tasks_r[0][1])):
                times[processor_no] = tasks_r[0][2] + tasks_r[0][1] + times[processor_no]
                taskOrder[processor_no].append(str(tasks_r[0][0] + 1))
                del tasks_d[tasks_d.index(tasks_r[0])]
                del tasks_r[0]
            else:
                times[processor_no] = tasks_d[0][2] + tasks_d[0][1] + times[processor_no]
                taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
                del tasks_r[tasks_r.index(tasks_d[0])]
                del tasks_d[0]


def save_result(algorithm_author, algorithm, instance_author, instance_size, taskOrder, ds, tardiness):
    filename = os.path.join("results",
                            str(algorithm_author),
                            str(algorithm),
                            str(instance_author),
                            "{}.txt".format(instance_size))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(str(tardiness) + "\n")
        for x in range(0, 4):
            for y in range(0, len(taskOrder[x])):
                f.write(str(taskOrder[x][y]) + " ")
            f.write("\n")


def checkTardinessForOneProcessor(order, tasks):
    tardiness = 0
    start = 0
    for t in order:
        t = int(t) - 1
        start = max(tasks[1][t], start)
        end = start + tasks[0][t]
        tardiness = tardiness + max(0, end - tasks[2][t])
        start = end
    return tardiness


def tardinessForOrder(inorder, tasks):
    totalAmount = 0
    for i in range(0, 4):
        inorder.tardinessOnEachProcessor[i] = checkTardinessForOneProcessor(inorder.order[i], tasks)
        totalAmount += inorder.tardinessOnEachProcessor[i]
        inorder.tardiness = totalAmount
    return inorder


def generateTaskPair(bestOrder):
    randProcIndex = random.randint(0, 3)
    while len(bestOrder.order[randProcIndex]) < 2:
        randProcIndex = random.randint(0, 3)
    randTaskIndex = random.randint(0, len(bestOrder.order[randProcIndex]) - 1)
    randomTask1 = RandomTask(randTaskIndex, randProcIndex, bestOrder.order[randProcIndex][randTaskIndex])
    return randomTask1


def insertNewTask(inOrder, randomTask):
    randProcIndex = random.randint(0, 3)
    randTaskIndex = random.randint(0, len(inOrder.order[randProcIndex]) - 1)
    del inOrder.order[randomTask.procIndex][randomTask.index]
    inOrder.order[randProcIndex].insert(randTaskIndex, randomTask.value)
    return inOrder


def main():
    start = timer()
    algorithm_author = "132274"
    algorithm = "a2"
    instance_author = sys.argv[1]
    instance_size = sys.argv[2]
    instance_file_path = os.path.join("instances",
                                      instance_author,
                                      "{}.txt".format(instance_size))
    total_time = 0.0
    max_time = (10.0 * float(instance_size) * 0.001) - 0.004

    tasks, noTasks = readTasks(instance_size, instance_file_path)
    tasks_d, tasks_r = sortTasks(tasks, instance_size)
    times = []
    ds = []
    taskOrder = [[], [], [], []]
    for x in range(0, 4):
        times.append(0)
        ds.append(0)
    orderTasks(tasks_d, tasks_r, instance_size, times, taskOrder, ds)
    tardiness = 0
    tard = 0
    taProc = []
    for i in range(0, 4):
        tard = checkTardinessForOneProcessor(taskOrder[i], tasks)
        tardiness += tard
        taProc.append(tard)
    end = timer()
    total_time += (end - start)
    bestOrder = BestOrder(taskOrder, tardiness, taProc)

    # begin advanced algorithm
    while True:
        start = timer()
        t1 = generateTaskPair(bestOrder)
        newOrder = insertNewTask(deepcopy(bestOrder), t1)
        newOrder = tardinessForOrder(newOrder, tasks)
        delta_tardiness = bestOrder.tardiness - newOrder.tardiness
        if delta_tardiness >= 0:
            bestOrder = deepcopy(newOrder)
        else:
            licznik = delta_tardiness * 100000
            czas = ((max_time - total_time) / max_time) * 100.0
            mianownik = newOrder.tardiness * czas
            ulamek = licznik / mianownik
            ulamek = math.exp(ulamek)
            if (ulamek > random.random()):
                bestOrder = deepcopy(newOrder)
        end = timer()
        total_time += (end - start)
        if total_time >= max_time:
            break
    # end advanced algorithm

    save_result(algorithm_author,
                algorithm,
                instance_author,
                instance_size, bestOrder.order, ds, bestOrder.tardiness)


if __name__ == "__main__":
    main()
