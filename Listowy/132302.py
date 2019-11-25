import time
import sys
import os

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
    tasks.sort(key = lambda x: x[2]) 
    return tasks 

def fastest_machine(machines):
    min = machines[0]
    idx = [0]
    for i in range(1,4):
        if machines[i] < min:
            min = machines[i]
            idx = [i]
        if machines[i] == min:
            idx.append(i)
    return idx

def assign(choice, tasks_om, counters, machines, task, latency):
    tasks_om[choice].append(task[0])
    counters[choice] += 1
    if machines[choice] < task[2]:
        machines[choice] = task[1] + task[2]
    else:
        machines[choice] += task[1]
    if machines[choice] > task[3]:
        latency += machines[choice] - task[3]
    return tasks_om, counters, machines, latency

def solution(tasks):
    machines = [0,0,0,0]
    counters = [0,0,0,0]
    tasks_om = [[],[],[],[]]
    latency = 0
    for task in tasks:
        machine_choice = fastest_machine(machines)
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
            tasks_om, counters, machines, latency = assign(choice, tasks_om, counters, machines, task, latency)
        else:
            tasks_om, counters, machines, latency = assign(machine_choice[0], tasks_om, counters, machines, task, latency)
    return tasks_om, latency

def save_results(tasks, latency, n):
    outputF = "results/132302/a1/" + sys.argv[1] + "/" + str(n) + ".txt"
    file = open(outputF,"w")
    file.write(str(latency) + '\n')
    for task in tasks:
        for id in task:
            file.write(str(id)+ ' ' )
        file.write('\n')


def algorithm(instance):
    if not os.path.exists("results/132302/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/132302/a1/" + sys.argv[1] + "/")
    inputF = "instances/"+ sys.argv[1] + "/" + str(instance) + ".txt"
    tasks_list, n = get_data(inputF)
    tasks_list = sort(tasks_list)
    tasks, latency = solution(tasks_list)
    save_results(tasks, latency, n)
    #return latency

def main():
    algorithm(int(sys.argv[2]))

if __name__ == '__main__':
    main()
