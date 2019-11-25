#!/usr/bin/env python

import sys
import math
import os
import time

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
        choose_minimum = [(machine_list[0].now - task_list[g].r),
        (machine_list[1].now - task_list[g].r),
        (machine_list[2].now - task_list[g].r),
        (machine_list[3].now - task_list[g].r)]
        choosen = choose_minimum.index(min(choose_minimum))
        machine_list[choosen].list.append(task_list[g])
        if machine_list[choosen].now < machine_list[choosen].list[-1].r:
            machine_list[choosen].now = machine_list[choosen].list[-1].r + machine_list[choosen].list[-1].p
        else:
            machine_list[choosen].now = machine_list[choosen].now + machine_list[choosen].list[-1].p
        machine_list[choosen].due = machine_list[choosen].due + max(machine_list[choosen].now - machine_list[choosen].list[-1].d,0)
    return 0


def main():
    file = open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "rU")
    number_of_rows = int(file.readline())
    machine_list = [Machine(), Machine(), Machine(), Machine()]
    task_list = []
    total_due = 0
    for i in range(number_of_rows):
        temporary = file.readline().split()
        task_list.append(Task(i + 1, int(temporary[0]), int(temporary[1]), int(temporary[2])))
    file.close()
    task_list.sort(key = lambda Task: Task.d)

    count_due_on_machines(number_of_rows, task_list, machine_list)

    total_due = machine_list[0].due + machine_list[1].due + machine_list[2].due + machine_list[3].due

    if not os.path.exists("results/" + "/132247/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132247/a1/" + sys.argv[1] + "/")
    file = open("results/" + "/132247/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
    file.write(str(total_due) + "\n")
    for z in range(len(machine_list)):
        temporary = ""
        for y in range(len(machine_list[z].list)):
            temporary = temporary + str(machine_list[z].list[y].id) + " "
        temporary = temporary[:len(temporary) - 1]
        file.write(temporary + "\n")
    file.close()
    #return(total_due)



if __name__ == '__main__':
    main()
