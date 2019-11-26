import sys
import math
import os
import time

class Task(object):
    def __init__(self, p, r, d, idx):
        self.p = p
        self.r = r
        self.d = d
        self.idx = idx
class Machine(object):
    def __init__(self):
        self.tasks = []
        self.free_at = 0


def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r")
    #get rid of 1st line
    no_tasks = int(file.readline())
    tasks = []
    idx   = 0
    lines = file.readlines()
    for line in lines:
        line = line.split()
        # p r d
        tasks.append(Task(int(line[0]), int(line[1]), int(line[2]), idx))
        idx = idx + 1
    file.close()


    # letsgo

    tardiness = 0
    cur_time = 0
    machines = []
    ready_tasks = []

    for i in range(4):
        machines.append(Machine())
    tasks = sorted(tasks, key=lambda x: x.r)

    while (len(tasks) != 0):
        # update ready tasks
        while tasks[0].r <= cur_time:
            ready_tasks.append(tasks.pop(0))
            # if there are no more waiting tasks
            if (len(tasks) == 0):
                break
        # sort ready tasks by p - ascending
        ready_tasks = sorted(ready_tasks, key=lambda x: x.p, reverse=True)
        # if all the tasks are ready to go
        if (len(tasks) == 0):
            break
        # update free machines
        free_machines = []
        for machine in machines:
            if (machine.free_at <= cur_time):
                free_machines.append(machine)
        # while there are ready tasks and free machines
        while (len(ready_tasks) != 0) and (len(free_machines) != 0):
            machine = free_machines.pop(0)
            task    = ready_tasks.pop(0)
            # assign task to free machine
            machine.free_at = cur_time + task.p
            machine.tasks.append(task)
            # add tardiness if task ends after due time
            tardiness = tardiness + max(0, (cur_time + task.p - task.d))
        # update cur_time (jump to a new task or a free machine)
        if (len(free_machines) == 0) and (len(ready_tasks) == 0):
            cur_time = min(tasks[0].r, min(machines, key=lambda x: x.free_at).free_at)
        elif (len(free_machines) == 0):
            cur_time = min(machines, key=lambda x: x.free_at).free_at
        else:
            cur_time = tasks[0].r
    # while there are still tasks to proceed
    while len(ready_tasks) != 0:
        # update free machines
        free_machines = []
        for machine in machines:
            if (machine.free_at <= cur_time):
                free_machines.append(machine)
        # while there are ready tasks and free machines
        while (len(ready_tasks) != 0) and (len(free_machines) != 0):
            machine = free_machines.pop(0)
            task    = ready_tasks.pop(0)
            # assign task to free machine
            machine.free_at = cur_time + task.p
            machine.tasks.append(task)
            print("add r = " + str(task.r) + " to machine")
            # add tardiness if task ends after due time
            tardiness = tardiness + max(0, (cur_time + task.p - task.d))
        # update cur_time (jump to a free machine)
        cur_time = min(machines, key=lambda x: x.free_at).free_at

    if not os.path.exists("results/" + "/132292/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132292/a1/" + sys.argv[1] + "/")
    file = open("results/" + "/132292/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(tardiness))
    for machine in machines:
        file.write('\n')
        for task in machine.tasks:
            file.write(str(task.idx + 1) + ' ')
    file.close()





if __name__ == '__main__':
    main()
