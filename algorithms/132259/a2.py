import sys
import os
from time import time
from random import randint, random
from copy import deepcopy
from math import exp


class Processor:
    def __init__(self):
        self.zad = []
        self.D = 0


class Task:
    def __init__(self, id, p, r, d):
        self.id = id
        self.p = p
        self.r = r
        self.d = d
        self.key = 0
        self.delay = 0


def suma(e):
    return e.r + e.d

def klucz(e):
    return e.key

def opoz(e):
    return e.delay


def main():
    start = time()
    file = open("instances/" + str(sys.argv[1]) + "/" + str(sys.argv[2]) + ".txt", "r")
    n = int(file.readline())
    zad = []
    proc = [Processor(), Processor(), Processor(), Processor()]
    D = 0

    for i in range(n):
        temp = file.readline().split()
        zad.append(Task(i + 1, int(temp[0]), int(temp[1]), int(temp[2])))

    file.close()
    zad.sort(key=suma)

    for i in range(n):
        zad[i].key = i
        mini = min([[max(proc[0].D, zad[i].r), zad[i].r - proc[0].D, 0],
                    [max(proc[1].D, zad[i].r), zad[i].r - proc[1].D, 1],
                    [max(proc[2].D, zad[i].r), zad[i].r - proc[2].D, 2],
                    [max(proc[3].D, zad[i].r), zad[i].r - proc[3].D, 3]])[2]
        proc[mini].zad.append(zad[i].id)
        proc[mini].D = max(zad[i].r, proc[mini].D) + zad[i].p
        zad[i].delay = max(0, proc[mini].D - zad[i].d)
        D += zad[i].delay

    output_path = "results/132259/a2/" + str(sys.argv[1])
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file = open(output_path + "/" + str(sys.argv[2]) + ".txt", "w+")
    file.write(str(D) + "\n")

    for i in range(4):
        temp = ""
        for j in range(len(proc[i].zad)):
            temp += str(proc[i].zad[j]) + " "
        temp = temp[:len(temp) - 1]
        file.write(temp + "\n")

    file.close()

    best_proc = deepcopy(proc)
    last_proc = deepcopy(proc)
    best_D = D
    last_D = D
    for i in range(4):
        proc[i].D = 0
    T = 100
    offset = 0

    while(time() - start < 300):
        D = 0
        for i in range(4):
            proc[i].zad = []
            proc[i].D = 0
        zad.sort(key=opoz)
        maxi = randint(n - 6, n - 1)
        mini = randint(0, 5)
        temp = zad[maxi].key
        zad[maxi].key = zad[mini].key
        zad[mini].key = temp

        zad.sort(key=klucz)
        for i in range(n):
            mini = min([[max(proc[0].D, zad[i].r), zad[i].r - proc[0].D, 0],
                        [max(proc[1].D, zad[i].r), zad[i].r - proc[1].D, 1],
                        [max(proc[2].D, zad[i].r), zad[i].r - proc[2].D, 2],
                        [max(proc[3].D, zad[i].r), zad[i].r - proc[3].D, 3]])[2]
            proc[mini].zad.append(zad[i].id)
            proc[mini].D = max(zad[i].r, proc[mini].D) + zad[i].p
            zad[i].delay = max(0, proc[mini].D - zad[i].d)
            D += zad[i].delay

        if D < best_D:
            file = open(output_path + "/" + str(sys.argv[2]) + ".txt", "w+")
            file.write(str(D) + "\n")

            for i in range(4):
                temp = ""
                for j in range(len(proc[i].zad)):
                    temp += str(proc[i].zad[j]) + " "
                temp = temp[:len(temp) - 1]
                file.write(temp + "\n")

            file.close()
            best_proc = deepcopy(proc)
            best_D = D
            offset = 0
        elif D < last_D:
            last_proc = deepcopy(proc)
            last_D = D
            offset = 0
        elif T != 0:
            prob = 0
            try:
                prob = exp(100*(best_D - D)/(best_D*T))
            except:
                T = 0
            if prob > random():
                last_proc = deepcopy(proc)
                last_D = D
                T -= 1
                offset = 0
            else:
                proc = deepcopy(last_proc)
                if offset < n // 3 - 1:
                    offset += 1
        else:
            proc = deepcopy(last_proc)
            if offset < n // 3 - 1:
                offset += 1


main()
