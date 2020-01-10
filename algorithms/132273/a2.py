import time
import os
import sys
import random
import copy

class Task(object):
    def __init__(self, id, p, r, d):
        self.r = r
        self.p = p
        self.d = d
        self.id = id  
        self.param = 0.75*int(r) + 0.25*int(d)
        
def schedule_all(tasksList):
    
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

            M[m].append(Task(int(task.id), int(task.p), int(task.r), int(task.d)))
    
    return D, sum(D), M

def schedule_one(machine, M, D):
    D[machine] = 0
    TIME = 0
    for task in M[machine]:
        if TIME < int(task.r):
                TIME = int(task.r)
        TIME += int(task.p)
        if TIME > int(task.d):
                D[machine] += TIME - int(task.d)
                
    return D, sum(D)
        

def save_schedule(Tardiness, M):
    if not os.path.exists("results/" + "/132273/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132273/a2/" + sys.argv[1] + "/")
    result = open("results/" + "/132273/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    result.write(str(Tardiness) + '\n')
    for i in range(0, 4):
        for j in range(0, len(M[i])):
            if j == 0:
                result.write(str(M[i][j].id+1)) 
            else:
                result.write(' ' + str(M[i][j].id+1))
        result.write('\n')
    result.close()

    

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
    D_p, Tardiness_p, M_p = schedule_all(tasksList)
    
    tasksList = sorted(tasksList, key=lambda x: (x.d, x.r))    
    D_d, Tardiness_d, M_d = schedule_all(tasksList)

    tasksList = sorted(tasksList, key=lambda x: (x.r, x.d))    
    D_r, Tardiness_r, M_r = schedule_all(tasksList)

    if Tardiness_p < Tardiness_d and Tardiness_p < Tardiness_r:
        tasksList = sorted(tasksList, key=lambda x: (x.param, x.p))    
        D, Tardiness, M = schedule_all(tasksList)
    elif Tardiness_d < Tardiness_p and Tardiness_d < Tardiness_r:
        tasksList = sorted(tasksList, key=lambda x: (x.d, x.r))
        D, Tardiness, M = schedule_all(tasksList)
    else: 
        tasksList = sorted(tasksList, key=lambda x: (x.r, x.d))
        D, Tardiness, M = schedule_all(tasksList)
        
    print(Tardiness)

    start = time.time()
    maxTime = 10*number_of_rows*0.001
    
    while time.time()-start < maxTime:
        tasksList1 = tasksList        
        M1 = copy.deepcopy(M)
        D1 = copy.deepcopy(D)
        
        
        machine = random.sample(range(4), 2)
        m1 = machine[0]
        m2 = machine[1]
        minlen = min(len(M[m1]), len(M[m2]))
        a = random.randint(0, minlen-2)
        b = random.randint(a+1, min(minlen-1, a+30))

        part1 = M1[m1][a:b]
        part2 = M1[m2][a:b]            
        M1[m1][a:b] = part2
        M1[m2][a:b] = part1

            
        D1, Tardiness1 = schedule_one(m1, M1, D1)
        D1, Tardiness1 = schedule_one(m2, M1, D1)
        
            
            
        if Tardiness1 < Tardiness:
            M = copy.deepcopy(M1)
            D = copy.deepcopy(D1)
            Tardiness = Tardiness1
            print(Tardiness)
        else:
            tasksList = tasksList1
            


    save_schedule(Tardiness, M)
    
    
if __name__ == '__main__':
    main()