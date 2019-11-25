from dataclasses import dataclass, field
from sys import argv
from typing import List, Tuple, Dict
from copy import copy 
from operator import attrgetter
import os

@dataclass
class Task:
	id: int
	p: int
	r: int
	d: int


@dataclass
class Machine: 
	id: int
	current_time: int = 0
	tasks_submited: List[Task] = field(default_factory=list)


def calculate_error(tasks: List[Task]) -> int:
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


def find_first_available(machines: Dict[int, Machine], task: Task):
	least_occupied = sorted(machines.values(), key=attrgetter('current_time'))[0]
	least_occupied.tasks_submited.append(copy(task))
	if task.r < least_occupied.current_time:
		least_occupied.current_time += task.p
	else:
		least_occupied.current_time = task.r + task.p


def assign(machines: Dict[int, Machine], tasks: List[Task]) -> int:
	tasks.sort(key=attrgetter('r', 'p'))
	tasks.sort(key=lambda task: task.d - task.r + task.p)
	while tasks:
		find_first_available(machines, tasks[0])
		tasks.pop(0)

def run():
	machines: Dict[int, Machine] = {i: Machine(id=i) for i in range(1, 5)}
	tasks: List[Task] = []

	_, index, n = argv

	input_file = open(f'instances/{index}/{n}.txt')
	for idx, line in enumerate(input_file.readlines()[1:]):
		p, r ,d = map(int, line.split())
		tasks.append(Task(idx + 1, p, r, d))

	assign(machines, tasks)

	error = sum((calculate_error(m.tasks_submited) for m in machines.values()))

	output_dir = f'results/132287/a1/{index}'
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	output = open(f'{output_dir}/{n}.txt', 'w')
	output.write(str(error))
	output.write('\n')
	for machine in machines.values():
		output.write(' '.join((str(task.id) for task in machine.tasks_submited)))
		output.write('\n')


if __name__ == '__main__':
	run()
