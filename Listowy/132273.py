import time

class Task(object):
    def __init__(self, id, p, r, d):
        self.r = r
        self.p = p
        self.d = d
        self.id = id  
        self.param = 0.75*int(r) + 0.25*int(d)


def algorithm(tasksNumbers):
    tasksFile = open("in/" + str(tasksNumbers) + ".txt", "r")
    result = open("out/" + str(tasksNumbers) + ".txt", "w+")
    # Skipping Line
    query = tasksFile.readline()
    tasksList = []
    # Getting task list to array (r,p,d) as object
    for number in range(0, tasksNumbers):
        line = tasksFile.readline()
        line = line.strip().split(' ')
        tasksList.append(Task(number, int(line[0]), line[1], line[2]))
    
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


    end = time.time()
    
    
    result.write(str(sum(D)) + '\n')
    for i in range(0, 4):
        for j in range(0, len(M[i])):
            if j == 0:
                result.write(str(M[i][j]+1)) 
            else:
                result.write(' ' + str(M[i][j]+1))
        result.write('\n')
    return (sum(D))

    


results = []
print("Czasy:")
for instance in range(50, 501, 50):
    start=time.time()
    result = algorithm(instance)
    results.append(result)
    end=time.time()
    print("%.5f"%(end-start))
print("\nWyniki:")
for i in results:
    print(i)
