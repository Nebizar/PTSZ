import time
import sys
import os
import random
 
def get_data(input_file):
    file = open(input_file, "r")
    n=int(file.readline())
    tasks=file.readlines()
    for i in range(0,n):
        #tasks[i] = tasks[i].split()
        tasks[i] = [int(j) for j in tasks[i].split()]
        tasks[i] = [i+1] + tasks[i]
    file.close()
    return tasks, n
 
def sort(tasks):
    tasks.sort(key = lambda x: x[3] - x[2] + x[1])
    return tasks
 
def sort_d(tasks):
    tasks.sort(key = lambda x: x[3])
    return tasks
 
def sort_r(tasks):
    tasks.sort(key = lambda x: x[2])
    return tasks
 
def getReadyTasks(tasks, machine_time, grasp):
    readyTasks = []
    i = 0
    readyCount = 0
    while i < len(tasks) and readyCount < grasp:
        if tasks[i][2] <= machine_time:
            readyTasks.append(i)
            readyCount += 1
            #tasks.pop(i)
        i += 1
    if len(readyTasks) == 0:
        if grasp == 1:
            readyTasks = [0]
        elif len(tasks) > 3:
            readyTasks = [0,1,2]
        elif len(tasks) > 2:
            readyTasks = [0,1]
        else:
            readyTasks = [0]
        #tasks.pop()
 
    return readyTasks
 
def fastest_machine_org(machines):
    min = machines[0]
    idx = [0]
    for i in range(1,4):
        if machines[i] < min:
            min = machines[i]
            idx = [i]
        if machines[i] == min:
            idx.append(i)
    return idx
 
def assign_org(choice, tasks_om, counters, machines, task, latency):
    tasks_om[choice].append(task[0])
    counters[choice] += 1
    if machines[choice] < task[2]:
        machines[choice] = task[1] + task[2]
    else:
        machines[choice] += task[1]
    if machines[choice] > task[3]:
        latency += machines[choice] - task[3]
    return tasks_om, counters, machines, latency
 
def solution_org(tasks, n, grasp):
    machines = [0,0,0,0]
    counters = [0,0,0,0]
    tasks_om = [[],[],[],[]]
    latency = 0
    for _ in range(0,n):
        machine_choice = fastest_machine_org(machines)
        if len(machine_choice) > 1:
            mini = 9999999999
            choice = machine_choice[0]
            for m in machine_choice:
                if machines[m] != 0 and counters[m] != 0:
                    if counters[m]/machines[m] < mini:
                        mini = counters[m]/machines[m]
                        choice = m
                else:
                    choice = m
                    mini = 0
            #print(choice)
            rTasks = getReadyTasks(tasks, machines[choice], grasp)
            idx_rand = random.randrange(0, len(rTasks))
            randTask = rTasks[idx_rand]
            tasks_om, counters, machines, latency = assign_org(choice, tasks_om, counters, machines, tasks[randTask], latency)
            tasks.pop(randTask)
        else:
            rTasks = getReadyTasks(tasks, machines[machine_choice[0]], grasp)
            #randTask = np.random.choice(rTasks)
            idx_rand = random.randrange(0, len(rTasks))
            randTask = rTasks[idx_rand]
            tasks_om, counters, machines, latency = assign_org(machine_choice[0], tasks_om, counters, machines, tasks[randTask], latency)
            tasks.pop(randTask)
        #print(len(tasks))
    return tasks_om, latency
 
def fastest_machine(machines):
    min = machines[0]
    idx = 0
    for i in range(1,4):
        if machines[i] < min:
            min = machines[i]
            idx = i
    return idx
 
def assign(choice, tasks_om, machines, task, latency):
    tasks_om[choice].append(task[0])
    #counters[choice] += 1
    if machines[choice] < task[2]:
        machines[choice] = task[1] + task[2]
    else:
        machines[choice] += task[1]
    if machines[choice] > task[3]:
        latency += machines[choice] - task[3]
    return tasks_om, machines, latency
 
def solution(tasks, n, grasp):
    machines = [0,0,0,0]
    #counters = [0,0,0,0]
    tasks_om = [[],[],[],[]]
    latency = 0
    for _ in range(0,n):
        machine_choice = fastest_machine(machines)
        rTasks = getReadyTasks(tasks, machine_choice, grasp)
        #randTask = np.random.choice(rTasks)
        idx_rand = random.randrange(0, len(rTasks))
        randTask = rTasks[idx_rand]
        tasks_om, machines, latency = assign(machine_choice, tasks_om, machines, tasks[randTask], latency)
        tasks.pop(randTask)
    return tasks_om, latency
 
def save_results(tasks, latency, n):
    outputF = "results/132302/a2/" + sys.argv[1] + "/" + str(n) + ".txt"
    file = open(outputF,"w")
    file.write(str(latency) + '\n')
    for task in tasks:
        temp = ""
        for id in task:
            temp += str(id) + ' '
            #file.write(str(id)+ ' ' )
        file.write(temp[:len(temp)-1]+'\n')
 
 
def algorithm(instance):
    if not os.path.exists("results/132302/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/132302/a2/" + sys.argv[1] + "/")
    inputF = "instances/"+ sys.argv[1] + "/" + str(instance) + ".txt"
    tasks_list, n = get_data(inputF)
 
    start_time = time.time()
    max_time=start_time+0.01*n-0.05
 
    tasks_list = sort(tasks_list.copy())
    tasks_list_d = sort_d(tasks_list.copy())
    tasks_list_r = sort_r(tasks_list.copy())
 
    tasks_org, latency_org = solution_org(tasks_list.copy(), n, 1)
    #print(latency_org)
    tasks, latency = solution(tasks_list.copy(), n, 1)
    #print(latency)
    tasks_d, latency_d = solution(tasks_list_d.copy(), n, 1)
    #print(latency_d)
    tasks_r, latency_r = solution(tasks_list_r.copy(), n, 1)
    #print(latency_r)
 
    if latency < latency_d and latency < latency_r and latency < latency_org:
        #print('normal')
        while(time.time() < max_time):
            tasks_new, latency_new = solution(tasks_list.copy(), n, 3)
            if latency_new < latency:
                tasks = tasks_new
                latency = latency_new
            #print("Latency New: ", latency)
    elif latency_d < latency and latency_d < latency_r and latency_d < latency_org:
        #print('d')
        latency = latency_d
        tasks = tasks_d
        while(time.time() < max_time):
            tasks_new, latency_new = solution(tasks_list_d.copy(), n, 3)
            if latency_new < latency:
                tasks = tasks_new
                latency = latency_new
            #print("Latency New: ", latency)
    elif latency_org < latency and latency_org < latency_r and latency_org < latency_d:
        #print('org')
        latency = latency_org
        tasks = tasks_org
        while(time.time() < max_time):
            tasks_new, latency_new = solution_org(tasks_list.copy(), n, 3)
            if latency_new < latency:
                tasks = tasks_new
                latency = latency_new
            #print("Latency New: ", latency)
    else:
        #print('r')
        latency = latency_r
        tasks = tasks_r
        while(time.time() < max_time):
            tasks_new, latency_new = solution(tasks_list_r.copy(), n, 3)
            if latency_new < latency:
                tasks = tasks_new
                latency = latency_new
            #print("Latency New: ", latency)
 
    #print("Latency: ", latency)
    #print('Time:', time.time() - start_time)
    save_results(tasks, latency, n)
    #return latency
 
def main():
    algorithm(int(sys.argv[2]))
 
if __name__ == '__main__':
    main()