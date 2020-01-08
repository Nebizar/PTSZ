import sys
import math
import os
import time
from random import randrange

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

class NewTask(object):
   def __init__(self, task, machine_index, task_index):
       self.task    = task
       self.machine_index = machine_index
       self.task_index    = task_index

def main():

   start = time.time()

   cur_machines      = []
   swapped_machines  = []
   best_cur_machines = []
   best_machines     = [] 
   pairs             = []
   tabu_pairs        = []
   TABU_SIZE         = 100
   TIME_LIMIT        = 0.01 * int(sys.argv[2])

   # generuj początkowe uporzatkowanie
   machines = generate_a1_schedule()
   # przepisz procesy z nową informacją (machine_index i task_index)
   for machine_index, machine in enumerate(machines):
       cur_machines.append(Machine())
       for task_index, task in enumerate(machine.tasks):
           cur_machines[machine_index].tasks.append(NewTask(task, machine_index, task_index))

   best_cur_machines  = copy_machines(cur_machines)
   best_cur_tardiness = calculate_tardiness(best_cur_machines)
   best_machines      = copy_machines(cur_machines)
   best_tardiness     = best_cur_tardiness   
   
   while(True):
       cur_machines = copy_machines(best_cur_machines)
       if (best_cur_tardiness <= best_tardiness):
           best_tardiness = best_cur_tardiness
           best_machines  = copy_machines(best_cur_machines)
       # pairs = generate_pairs(cur_machines)
       # pairs = select_pairs(pairs, 200)
       pairs = generate_x_pairs(cur_machines, 1, tabu_pairs)
       # print("Sprawdze " + str(len(pairs)) + " możliwych zamian")
       best_cur_machines  = copy_machines(cur_machines)
       best_cur_tardiness = calculate_tardiness(cur_machines)
       for pair in pairs:
           if (True):
               swapped_machines  = swap(cur_machines, pair)
               swapped_tardiness = calculate_tardiness(swapped_machines)
               if (swapped_tardiness <= best_cur_tardiness):
                   best_cur_machines  = copy_machines(swapped_machines)
                   best_cur_tardiness = swapped_tardiness 
                   if (len(tabu_pairs) > TABU_SIZE):
                       tabu_pairs.pop(0)
                       tabu_pairs.append(pair)
                   else:
                       tabu_pairs.append(pair)
               if (time.time() - start >= TIME_LIMIT):
                   # zapisz najlepszy wynik, jeżeli się pojawił w trakcie iterowania po zbiorze par
                   if (best_cur_tardiness < best_tardiness):
                       best_tardiness = best_cur_tardiness
                       best_machines  = copy_machines(best_cur_machines)
                       # print("!!! new best T: " + str(best_tardiness) + " real: " + str(calculate_tardiness(best_machines)))
                   break
       if (time.time() - start >= TIME_LIMIT):
           break
       # print(" --- next step --- ")

   # print("Best Tardiness, that I've found is " + str(best_tardiness) + " " + str(calculate_tardiness(best_machines)) + " my Master")

   if not os.path.exists("results/" + "132292/a2/" + sys.argv[1] + "/"):
       os.makedirs("results/" + "132292/a2/" + sys.argv[1] + "/")
   file = open("results/" + "132292/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
   file.write(str(best_tardiness))
   for machine in best_machines:
       file.write('\n')
       for task in machine.tasks:
           file.write(str(task.task.idx + 1) + ' ')
   file.close()

def copy_machines(machines):
   new_machines = []
   for machine in machines:
       new_machine = Machine()
       new_machine.tasks = machine.tasks.copy()
       new_machines.append(new_machine)
   return new_machines

def generate_x_pairs(machines, x, tabu_pairs):
   no_pairs = 0
   selected_pairs = []
   while (no_pairs < x):
       pair = choose_pair(machines)
       if ((not (pair in selected_pairs))
       and (not (pair in tabu_pairs))
       and (calculate_time(machines, pair[0]) >= pair[1].task.r) 
       and (calculate_time(machines, pair[1]) >= pair[0].task.r)):
           selected_pairs.append(pair)
           no_pairs = no_pairs + 1
   return selected_pairs

def generate_pairs(machines):
   pairs = []
   for machine1 in machines:
       for task1 in machine1.tasks:
           for machine2 in machines:
               for task2 in machine2.tasks:
                   if ((calculate_time(machines, task1) >= task2.task.r) and 
                       (calculate_time(machines, task2) >= task1.task.r)):
                       pairs.append([task1, task2])
   return pairs

def select_pairs(pairs, x):
   no_pairs = 0
   selected_pairs = []
   while (no_pairs < x):
       pair = pairs[randrange(len(pairs))]
       if not (pair in selected_pairs):
           selected_pairs.append(pair)
           no_pairs = no_pairs + 1
   return selected_pairs

def calculate_time(machines, task):
   time = 0
   for t in machines[task.machine_index].tasks:
       time = max(t.task.r, time)
       if (t == task):
           break        
       time = time + t.task.p
   return time

def calculate_tardiness2(machines):
   tardiness = 0
   for machine in machines:
       cur_time = 0
       for task in machine.tasks:
           start_time = max(cur_time, task.task.r)
           cur_time = start_time + task.task.p
           tardiness = tardiness + max(0, cur_time - task.task.d)
   return tardiness

def calculate_tardiness(machines):
   tardiness = 0
   for machine in machines:
       cur_time = 0
       for task in machine.tasks:
           start_time = max(cur_time, task.task.r)
           cur_time = start_time + task.task.p
           tardiness = tardiness + max(0, cur_time - task.task.d)
   return tardiness

def choose_pair(machines):
   machine_index = randrange(len(machines))
   task_index    = randrange(len(machines[machine_index].tasks))
   task1 = machines[machine_index].tasks[task_index]
   machine_index = randrange(len(machines))
   task_index    = randrange(len(machines[machine_index].tasks))
   task2 = machines[machine_index].tasks[task_index]
   return [task1, task2]

def swap(machines, pair):
   machines[pair[0].machine_index].tasks.pop(pair[0].task_index)
   machines[pair[0].machine_index].tasks.insert(pair[0].task_index, pair[1])
   machines[pair[1].machine_index].tasks.pop(pair[1].task_index)
   machines[pair[1].machine_index].tasks.insert(pair[1].task_index, pair[0])

   temp_machine_index    = pair[0].machine_index
   temp_task_index       = pair[0].task_index
   pair[0].machine_index = pair[1].machine_index
   pair[0].task_index    = pair[1].task_index
   pair[1].machine_index = temp_machine_index
   pair[1].task_index    = temp_task_index

   return machines

def print_tasks(machines):
   for machine in machines:
       for newtask in machine.tasks:
           print(str(newtask.machine_index) + " " + str(newtask.task_index) + " -> " + str(newtask.task.p) + " " + str(newtask.task.r) + " " + str(newtask.task.d))

def generate_a1_schedule():

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
           # print("add r = " + str(task.r) + " to machine")
           # add tardiness if task ends after due time
           tardiness = tardiness + max(0, (cur_time + task.p - task.d))
       # update cur_time (jump to a free machine)
       cur_time = min(machines, key=lambda x: x.free_at).free_at
   # print(tardiness)
   return machines

if __name__ == '__main__':
   main()
