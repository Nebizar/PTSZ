#!/usr/bin/env python

import sys
import math
import os
from timeit import default_timer as timer
import random


class Machine:
    def __init__(self):
        self.list = []
        self.now = 0
        self.due = 0


class Task:
    def __init__(self, id, p, r, d):
        self.id = id
        self.p = p
        self.r = r
        self.d = d


def count_due_on_machines(number_of_rows, task_list, machine_list):
    for g in range(number_of_rows):
        choose_minimum = [max(0,(machine_list[0].now - task_list[g].r)),
        max(0,(machine_list[1].now - task_list[g].r)),
        max(0,(machine_list[2].now - task_list[g].r)),
        max(0,(machine_list[3].now - task_list[g].r))]
        choosen = choose_minimum.index(min(choose_minimum))
        machine_list[choosen].list.append(task_list[g])
        if machine_list[choosen].now < machine_list[choosen].list[-1].r:
            machine_list[choosen].now = machine_list[choosen].list[-1].r + machine_list[choosen].list[-1].p
        else:
            machine_list[choosen].now = machine_list[choosen].now + machine_list[choosen].list[-1].p
        machine_list[choosen].due = machine_list[choosen].due + max(machine_list[choosen].now - machine_list[choosen].list[-1].d,0)
    return 0


def do_better(task_list, original_due, original_machine, number_of_rows):
    new_task_list = []
    new_machines = []
    new_due = []
    times = 10
    if number_of_rows < 101:
        times = 5
    for swap_n_times in range (0,times):
        new_task_list.append(task_list.copy())
        index_value = random.randint(0, len(task_list)-1)
        change_index = random.randint(-5, 5)
        if (index_value + change_index)>len(task_list) -1:
            swap_index = len(task_list) -1
        elif (index_value + change_index)<0:
            swap_index = 0
        else:
            swap_index = index_value + change_index

        new_task_list[swap_n_times][index_value], new_task_list[swap_n_times][swap_index] = new_task_list[swap_n_times][swap_index], new_task_list[swap_n_times][index_value]
        new_machines.append([Machine(), Machine(), Machine(), Machine()])
        count_due_on_machines(number_of_rows, new_task_list[swap_n_times], new_machines[swap_n_times])
        new_due.append(new_machines[swap_n_times][0].due + new_machines[swap_n_times][1].due + new_machines[swap_n_times][2].due + new_machines[swap_n_times][3].due)

    if original_due < min(new_due):
        return task_list, original_due, original_machine
    else:
        return new_task_list[new_due.index(min(new_due))], min(new_due), new_machines[new_due.index(min(new_due))]


def main():
    start = timer()
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "rU")
    number_of_rows = int(file.readline())
    machine_list = [Machine(), Machine(), Machine(), Machine()]
    task_list = []
    total_due = 0
    for i in range(number_of_rows):
        temporary = file.readline().split()
        task_list.append(Task(i + 1, int(temporary[0]), int(temporary[1]), int(temporary[2])))
    file.close()
    task_list.sort(key = lambda Task: Task.r)

    count_due_on_machines(number_of_rows, task_list, machine_list)

    total_due = machine_list[0].due + machine_list[1].due + machine_list[2].due + machine_list[3].due

    while(timer() - start < 0.01 * (number_of_rows-5)):
        task_list, total_due, machine_list = do_better(task_list, total_due, machine_list, number_of_rows)


    if not os.path.exists("results/" + "/132247/a2/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132247/a2/" + sys.argv[1] + "/")
    file = open("results/" + "/132247/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(total_due) + "\n")
    for z in range(len(machine_list)):
        temporary = ""
        for y in range(len(machine_list[z].list)):
            temporary = temporary + str(machine_list[z].list[y].id) + " "
        temporary = temporary[:len(temporary) - 1]
        file.write(temporary + "\n")
    file.close()


if __name__ == '__main__':
    main()
