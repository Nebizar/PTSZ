import os
import math
import sys

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

    def __init__(self, path):
        self.machines = [[] for x in range(self.num_machines)]
        self.machines_ready = [0 for x in range(self.num_machines)]
        self.path = path
        self.min_end = 0

    def push_task(self, task, machine_num):
        task_start = max(task.min_start, self.machines_ready[machine_num])
        task_end = task_start + task.duration


        self.machines_ready[machine_num] = task_end
        self.machines[machine_num].append(task)

        self.min_end = min(self.machines_ready)
    
    def get_ready_time(self, machine_num):
        return self.machines_ready[machine_num]
    
    def close_ready(self, time):
        # Returns machine ready as close as possible

        min_difference = abs(self.machines_ready[0] - time)
        min_machine = 0

        for i in range(self.num_machines):
            absolute_difference =  abs(self.machines_ready[i] - time)

            if absolute_difference < min_difference:
                min_difference = absolute_difference
                min_machine = i
        
        return min_machine
    
    def get_solution(self):
        self.total_delay = 0

        for machine in self.machines:
            for task_data in enumerate(machine):
                task_num = task_data[0]
                task = task_data[1]

                last_task_finished_time = 0

                if task_num > 0:
                    last_task_finished_time = machine[task_num - 1].end

                task_start = max(task.min_start, last_task_finished_time)
                task.set_start(task_start)

                self.total_delay += max(0, task.end - task.max_end)

        return self
    
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
            line = [str(x.id) for x in machine]
            line = " ".join(line)
            line += "\n"
            f.write(line)
        
        f.close()


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

        solution = Solution(self.data_source)

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



filename = "instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt"
instances = Instances()
instances.read_single(filename)
results = instances.simple_alghoritm()
solution = results[0]["solution"]

# Create dir if not exist
if not os.path.exists("results/132242/a1/" + sys.argv[1] + "/"):
    os.makedirs("results/132242/a1/" + sys.argv[1] + "/")

solution.save_to_file("results/132242/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt")