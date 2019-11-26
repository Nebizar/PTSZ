import time
import os
import sys

class Task(object):
    def __init__(self, id, p, r, d):
        self.r = r
        self.p = p
        self.d = d
        self.id = id  
        self.param = 0.75*int(r) + 0.25*int(d)

def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r")
    number_of_rows = int(file.readline())
    tasksList = []
    # Getting task list to array (r,p,d) as object
    for number in range(0, int(number_of_rows)):
        line = file.readline()
        line = line.strip().split(' ')
        tasksList.append(Task(number, int(line[0]), int(line[1]), int(line[2])))
    file.close()
    
    tasksList = sorted(tasksList, key=lambda x: (x.param, x.p))
    
    M = [[], [], [], []]
    TIME = [0, 0, 0, 0]
    D = [0, 0, 0, 0]
    m = 0
    for task in tasksList:
            time_min = TIME[0]
            m = 0
            for k in range(1, 4):
                if TIME[k] < time_min:
                    time_min = TIME[k]
                    m = k

            if TIME[m] < int(task.r):
                TIME[m] = int(task.r)
            TIME[m] += int(task.p)
            if TIME[m] > int(task.d):
                D[m] += TIME[m] - int(task.d)

            M[m].append(int(task.id))


    
    if not os.path.exists("results/" + "/132273/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132273/a1/" + sys.argv[1] + "/")
    result = open("results/" + "/132273/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    result.write(str(sum(D)) + '\n')
    for i in range(0, 4):
        for j in range(0, len(M[i])):
            if j == 0:
                result.write(str(M[i][j]+1)) 
            else:
                result.write(' ' + str(M[i][j]+1))
        result.write('\n')
    result.close()


    
if __name__ == '__main__':
    main()


