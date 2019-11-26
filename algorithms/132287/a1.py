from sys import argv
from copy import copy 
from operator import attrgetter
import os

class Task:
	def __init__(self, id, p, r, d):
		self.id = id
		self.p = p
		self.r = r
		self.d = d


class Machine: 
	def __init__(self, id, current_time=0, tasks_submited=None):
		self.id = id
		self.current_time = current_time
		self.tasks_submited = tasks_submited or []


def calculate_error(tasks):
	error = 0
	time = 0
	for task in tasks:
		if task.r < time:
			time += task.p
		else:
			time = task.r + task.p
		if time - task.d > 0:
			error += time - task.d
	return error


def find_first_available(machines, task):
	least_occupied = sorted(machines.values(), key=attrgetter('current_time'))[0]
	least_occupied.tasks_submited.append(copy(task))
	if task.r < least_occupied.current_time:
		least_occupied.current_time += task.p
	else:
		least_occupied.current_time = task.r + task.p


def assign(machines, tasks):
	tasks.sort(key=attrgetter('r', 'p'))
	tasks.sort(key=lambda task: task.d - task.r + task.p)
	while tasks:
		find_first_available(machines, tasks[0])
		tasks.pop(0)

def run():
	machines = {i: Machine(id=i) for i in range(1, 5)}
	tasks = []

	_, index, n = argv

	input_file = open('instances/{index}/{n}.txt'.format(index=index, n=n))
	for idx, line in enumerate(input_file.readlines()[1:]):
		p, r ,d = map(int, line.split())
		tasks.append(Task(idx + 1, p, r, d))

	assign(machines, tasks)

	error = sum((calculate_error(m.tasks_submited) for m in machines.values()))

	output_dir = 'results/132287/a1/{index}'.format(index=index)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	output = open('{output_dir}/{n}.txt'.format(output_dir=output_dir, n=n), 'w')
	output.write(str(error))
	output.write('\n')
	for machine in machines.values():
		output.write(' '.join((str(task.id) for task in machine.tasks_submited)))
		output.write('\n')


if __name__ == '__main__':
	run()
