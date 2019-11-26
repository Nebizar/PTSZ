import sys
import os

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

def suma(e):
    return e.r + e.d

def main():
    file = open("instances/132259/" + str(sys.argv[2]) + ".txt", "r")
    n = int(file.readline())
    zad = []
    proc = [Processor(), Processor(), Processor(), Processor()]
    D = 0

    for i in range(n):
        temp = file.readline().split()
        zad.append(Task(i + 1, int(temp[0]), int(temp[1]), int(temp[2])))

    file.close()
    zad.sort(key = suma)

    for i in range(n):
        mini = min([[max(proc[0].D, zad[i].r), 0], [max(proc[1].D, zad[i].r), 1],
                    [max(proc[2].D, zad[i].r), 2], [max(proc[3].D, zad[i].r), 3]])[1]
        proc[mini].zad.append(zad[i].id)
        proc[mini].D = max(zad[i].r, proc[mini].D) + zad[i].p
        D += max(0, proc[mini].D - zad[i].d)
    
    output_path = "results/132259/a1/" + str(sys.argv[1])
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

main()
