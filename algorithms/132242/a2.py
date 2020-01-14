import os
import math
import sys
import random
import copy
import math
import time


def print_solution(solution):
    for machine in solution.machines:
        id_arr = []
        for task in machine:
            if task:
                id_arr.append(task.id)
        print(id_arr)


class Task:
    def __init__(self, min_start, max_end, duration, id):
        self.min_start = min_start
        self.max_end = max_end
        self.duration = duration
        self.id = id
    
    def set_start(self, time):
        self.start = time
        self.end = time + self.duration

class Solution:
    num_machines = 4

    def __init__(self, path, num_tasks):
        self.machines = [[None for y in range(num_tasks * 2)] for x in range(self.num_machines)]
        self.machines_ready = [0 for x in range(self.num_machines)]
        self.machines_tasks_num = [0 for x in range(self.num_machines)]
        self.path = path
        self.min_end = 0
        self.num_tasks = num_tasks
        
        # [task, task_position, machine_num]
        self.tasks_info = [[]] * (num_tasks + 1)
        self.tasks_info[0] = 0

    def push_task(self, task, machine_num):
        task_start = max(task.min_start, self.machines_ready[machine_num])
        task_end = task_start + task.duration

        self.tasks_info[task.id] = [task, self.machines_tasks_num[machine_num], machine_num]

        self.machines_ready[machine_num] = task_end
        self.machines[machine_num][self.machines_tasks_num[machine_num]] = task

        self.min_end = min(self.machines_ready)

        self.machines_tasks_num[machine_num] += 1
    
    def get_ready_time(self, machine_num):
        return self.machines_ready[machine_num]
    
    def close_ready(self, time):
        # Returns machine ready as close as possible

        min_difference = self.machines_ready[0]
        min_machine = 0

        for i in range(self.num_machines):
            absolute_difference =  self.machines_ready[i]

            if absolute_difference < min_difference:
                min_difference = absolute_difference
                min_machine = i
        
        return min_machine
    
    def get_solution(self):
        self.total_delay = 0

        last_task_finished_time = 0
        machine_id = 0
        tasks_sum = 0
        total = 0

        for machine in self.machines:
            for task_data in enumerate(machine):
                task_num = task_data[0]
                task = task_data[1]

                if not task:
                    continue

                task_start = max(task.min_start, last_task_finished_time)
                task.set_start(task_start)
                total = total + 1

                self.total_delay += max(0, task.end - task.max_end)

                last_task_finished_time = task.end

                self.tasks_info[task.id][1] = tasks_sum
                tasks_sum += 1
            
            tasks_sum = 0
            last_task_finished_time = 0
            machine_id += 1

        if total != self.num_tasks:
            print("Invelid tasks number")
            quit()

        return self
    
    def get_matrix_solution(self):

        error = False
        
        self.machines = [[None for y in range(self.num_tasks * 2)] for x in range(self.num_machines)]
        for task in self.tasks_info[1:]:
            #print(task[1])
            if self.machines[task[2]][task[1]]:
                print('---')
                print(task[1])
                print(task[2])
                print("WTF")
                quit()
                
            self.machines[task[2]][task[1]] = task[0]
        
        return self.get_solution()
    
    def is_file_valid(self, solution_file, instance_file):
        tasks = []
        with open(instance_file) as file:
            data = file.read()
            rows = data.splitlines()
            num_tasks = int(rows[0])

            tasks = [0 for x in range(num_tasks + 1)]

            task_id = 1
            for row in rows[1:(num_tasks + 1)]:
                duration, min_start, max_end = row.split(' ')
                tasks[task_id] = Task(int(min_start), int(max_end), int(duration), task_id)
            
                task_id += 1

        file_delay = 0
        with open(solution_file) as file:
            data = file.read()
            rows = data.splitlines()
            file_delay = int(rows[0])

            machine_num = 0
            for row in rows[1:]:
                for task_id in row.split(' '):
                    self.push_task(tasks[int(task_id)], machine_num)

                machine_num += 1
        
        self.get_solution()

        if self.total_delay == file_delay:
            return True
        else:
            return False

    def save_to_file(self, path):
        if not self.total_delay and self.total_delay != 0:
            raise Exception("Solution doesn't exist yet")
        
        f = open(path, "w")
        f.write(str(self.total_delay) + "\n")
        
        for machine in self.machines:
            if not machine:
                continue
            
            line = []

            for x in machine:
                if x:
                    line.append(str(x.id))

            line = " ".join(line)
            line += "\n"
            f.write(line)
        
        f.close()

    def matrix_copy(self):
        mcopy = Solution(self.path, self.num_tasks)
        mcopy.tasks_info =  [list(p2) for p2 in self.tasks_info]

        return mcopy

class Instance:

    def __init__(self, path):
        self.path = path

        with open(path) as file:
            data = file.read()
            rows = data.splitlines()
            self.num_tasks = int(rows[0])
            self.tasks = []

            task_num = 1
            for row in rows[1:(self.num_tasks + 1)]:
                values = row.split()
                new_task = Task(int(float(values[1])), int(float(values[2])), int(float(values[0])), task_num)
                self.tasks.append(new_task)
                task_num += 1

class Genetics:
    population_size     = 5
    max_time            = 120  # s

    worst_evo_chance    = 1
    evo_chance_step     = 2

    evo_sum             = 0
    best_evo_chance     = 0

    mutation_chance     = 0
    mutation_similar    = 0
    similar_percent     = 1

    changes_limit = 1

    master_population = []
    population = []

    best                = None

    def __init__(self, instance, master_solutions = []):
        self.population_size = len(master_solutions) + 2
        self.best_evo_chance = self.worst_evo_chance + ((self.population_size - 1) * self.evo_chance_step)
        self.evo_sum = (self.worst_evo_chance + self.best_evo_chance) * (self.population_size / 2)

        self.instance = instance

        for member in master_solutions:
            self.master_population.append(member)
            self.population.append(member)

        for member in range(self.population_size - len(self.population)):
            first = self.population[random.randint(0, len(self.population) - 1)]
            second = self.population[random.randint(0, len(self.population) - 1)]
            self.population.append(self.solutionConnector(first, second))
    
    def evo(self):
        num_tasks = len(self.instance.tasks)

        start_time = time.time()

        while (True):
            newPopulation = []

            for member in self.master_population:
                newPopulation.append(member)

            self.population.sort(key=lambda a: a.total_delay)

            if self.best == None:
                self.best = self.population[0]
            
            if self.population[0].total_delay < self.best.total_delay:
                self.best = self.population[0]
                self.master_population.append(self.best)
                self.population_size += 1

            if (time.time() - start_time > self.max_time):
                # print_solution(self.best)
                break

            while (len(newPopulation) < self.population_size):
                first_random = self.getRandom()
                second_random = self.getRandom()

                while second_random == first_random:
                    second_random = self.getRandom()

                # new_one = self.solutionConnector(self.population[0], second_random)
                new_one = self.solutionConnector(first_random, second_random)

                newPopulation.append(new_one)
            
            self.population = newPopulation

    def getRandom(self):
        me = (random.random() * (self.evo_sum))
        move = math.floor(me / (self.worst_evo_chance + self.best_evo_chance))

        first_chance = move * self.evo_chance_step + self.worst_evo_chance
        second_chance = (len(self.population) - 1 - move) * self.evo_chance_step + self.worst_evo_chance

        found = None

        if (random.randint(0, second_chance) - first_chance + 1) > 0:
            found = self.population[move]
        else:
            found = self.population[len(self.population) - 1 - move]

        return found
    
    def solutionConnector(self, solution1, solution2):
        num_tasks = len(self.instance.tasks)
        # solution = solution1.matrix_copy()

        num_tasks = len(self.instance.tasks)
        solution = Solution(self.instance.path, num_tasks)

        tasks_from_second = []

        different = []

        for task_id in range(1, len(solution1.tasks_info)):
            if (solution1.tasks_info[task_id][1] != solution2.tasks_info[task_id][1] or solution1.tasks_info[task_id][2] != solution2.tasks_info[task_id][2]):
                different.append(task_id)

        if len(different) > 0:
            for i in range(self.changes_limit):
                random_id = random.choice(different)

                if random_id in tasks_from_second:
                    return

                solution.tasks_info[random_id] = [0, 0, 0]

                solution.tasks_info[random_id][0] = solution2.tasks_info[random_id][0]
                solution.tasks_info[random_id][1] = solution2.tasks_info[random_id][1] * 2 + 1
                solution.tasks_info[random_id][2] = solution2.tasks_info[random_id][2]
                
                tasks_from_second.append(random_id)

                if random.choice([True, False]):
                    replacement_id = solution1.machines[solution2.tasks_info[random_id][2]][solution2.tasks_info[random_id][1]]

                    if replacement_id and replacement_id != random_id:
                        replacement_id = replacement_id.id

                        solution.tasks_info[replacement_id] = [0, 0, 0]
                        solution.tasks_info[replacement_id][0] = solution1.tasks_info[replacement_id][0]
                        solution.tasks_info[replacement_id][1] = solution2.tasks_info[replacement_id][1] * 2 + 1
                        solution.tasks_info[replacement_id][2] = solution2.tasks_info[replacement_id][2]

                        tasks_from_second.append(replacement_id)

        for task_id in range(1, len(solution1.tasks_info)):
            rc = random.choice([True, False])

            if task_id not in tasks_from_second:
                #task from first
                solution.tasks_info[task_id] = [0, 0, 0]
                solution.tasks_info[task_id][0] = solution1.tasks_info[task_id][0]
                solution.tasks_info[task_id][1] = solution1.tasks_info[task_id][1] * 2
                solution.tasks_info[task_id][2] = solution1.tasks_info[task_id][2]

        solution.get_matrix_solution()

        # print(solution.total_delay)
        # time.sleep(1)
        return solution

class Instances:

    def read_all(self, data_source=".\sources"):

        self.instances = []
        self.files = []
        self.data_source = data_source

        for r, d, f in os.walk(data_source):
            for file in f:
                if '.txt' in file:
                    self.files.append(os.path.join(r, file))
                    self.instances.append(Instance(os.path.join(r, file)))
    
    def read_single(self, data_source):
        self.data_source = data_source
        self.files = [data_source]
        self.instances = [Instance(data_source)]

    def instance_iterator(self, function):
        if not self.instances:
            raise Exception('Instaces list is empty. Read instances first')

        results = []

        for instance in self.instances:
            result = {
                "file": instance.path,
                "solution": function(instance)
            }

            results.append(result)
        
        return results


    def simple_alghoritm(self, instance = None):
        if not instance:
            return self.instance_iterator(self.simple_alghoritm)
        
        # Ready time sort
        instance.tasks.sort(key=lambda x: (x.min_start))

        solution = Solution(self.data_source, len(instance.tasks))

        iterator = 0
        last_sorted = 0

        while iterator < len(instance.tasks):
            if instance.tasks[iterator].min_start <= solution.min_end:
                # find max less than min_end
                last_sorted = max(iterator, last_sorted)
                z = last_sorted

                while z < len(instance.tasks) and instance.tasks[z].min_start < solution.min_end:
                    last_sorted += 1
                    z += 1

                instance.tasks[iterator:last_sorted] = sorted(instance.tasks[iterator:last_sorted], key=lambda x: (x.duration))
            
            cool_machine = solution.close_ready(instance.tasks[iterator].min_start)
            solution.push_task(instance.tasks[iterator], cool_machine)
            iterator += 1

        return solution.get_solution()
    

    def simple_alghoritmV2(self, instance = None):
        if not instance:
            return self.instance_iterator(self.simple_alghoritmV2)
        
        # Ready time sort
        instance.tasks.sort(key=lambda x: (x.min_start))

        solution = Solution(self.data_source, len(instance.tasks))

        iterator = 0
        last_sorted = 0

        while iterator < len(instance.tasks):
            if instance.tasks[iterator].max_end <= solution.min_end:
                # find max less than min_end
                last_sorted = max(iterator, last_sorted)
                z = last_sorted

                while z < len(instance.tasks) and instance.tasks[z].min_start < solution.min_end:
                    last_sorted += 1
                    z += 1

                instance.tasks[iterator:last_sorted] = sorted(instance.tasks[iterator:last_sorted], key=lambda x: (x.duration))
            
            cool_machine = solution.close_ready(instance.tasks[iterator].min_start)
            solution.push_task(instance.tasks[iterator], cool_machine)
            iterator += 1

        return solution.get_solution()
    
    def ordered_start(self, instance = None):
        if not instance:
            return self.instance_iterator(self.ordered_start)
        
        # Ready time sort
        instance.tasks.sort(key=lambda x: (x.min_start))

        solution = Solution(self.data_source, len(instance.tasks))

        for task in instance.tasks:
            cool_machine = solution.close_ready(task.min_start)
            solution.push_task(task, cool_machine)

        return solution.get_solution()

    def ordered_end(self, instance = None):
        if not instance:
            return self.instance_iterator(self.ordered_end)
        
        # Ready time sort
        instance.tasks.sort(key=lambda x: (x.max_end))

        solution = Solution(self.data_source, len(instance.tasks))

        for task in instance.tasks:
            cool_machine = solution.close_ready(task.min_start)
            solution.push_task(task, cool_machine)

        return solution.get_solution()
    
    def basic_alghoritm(self, instance = None): # 1, 2, 3 solution
        if not instance:
            return self.instance_iterator(self.basic_alghoritm)

        num_tasks = len(instance.tasks)
        solution = Solution(self.data_source, num_tasks)
        num_machines = solution.num_machines


        for i in range(0, num_tasks):
            machine_number = int(math.floor(i // math.ceil(float(num_tasks) / float(num_machines))))
            solution.push_task(instance.tasks[i], machine_number)

        return solution.get_solution()

    def genetic(self, instance = None):
        if not instance:
            return self.instance_iterator(self.genetic)

        genetics = Genetics(instance)
        genetics.evo()

        solution = genetics.best
        return solution

    def grasp(self, instance = None):
        if not instance:
            return self.instance_iterator(self.grasp)

        num_tasks = len(instance.tasks)
        start_time = time.time()
        time_limit = (num_tasks * 10.0) / 1000

        start_solutions = []
        a = self.ordered_start(instance)
        b = self.ordered_end(instance)
        c = self.simple_alghoritm(instance)
        d = self.simple_alghoritmV2(instance)

        start_solutions.append(a)
        start_solutions.append(b)
        start_solutions.append(c)
        start_solutions.append(d)

        genetics = Genetics(instance, start_solutions)
        genetics.max_time = (time_limit - (time.time() - start_time)) - 0.008
        genetics.evo()

        return genetics.best

filename = "instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt"
instances = Instances()
instances.read_single(filename)
results = instances.grasp()
solution = results[0]["solution"]

# Create dir if not exist
if not os.path.exists("results/132242/a2/" + sys.argv[1] + "/"):
    os.makedirs("results/132242/a2/" + sys.argv[1] + "/")

solution.save_to_file("results/132242/a2/" + sys.argv[1] + "/" + sys.argv[2] + ".txt")


# start_time = time.time()
# taskSize = "500"
# time_limit = float(taskSize)
# filename = "ins/" + taskSize + ".txt"
# instances = Instances()
# instances.read_single(filename)
# results = instances.grasp()
# print(results[0]["solution"].total_delay)
# solution = results[0]["solution"]
# print(solution.total_delay)

# print(time.time() - start_time)