from dataclasses import dataclass, field
from sys import argv
from typing import List, Tuple, Dict
from copy import copy 
from operator import attrgetter
from time import time as now

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
	return least_occupied, task


def assign(machines: Dict[int, Machine], tasks: List[Task]) -> int:
	tasks.sort(key=attrgetter('r', 'p'))
	tasks.sort(key=lambda task: task.d - task.r + task.p)
	while tasks:
		find_first_available(machines, tasks[0])
		tasks.pop(0)

def run():
	for n in range(50, 501, 50):
		machines: Dict[int, Machine] = {i: Machine(id=i) for i in range(1, 5)}
		tasks: List[Task] = []

		input_file = open(f'in/{n}.txt')
		for idx, line in enumerate(input_file.readlines()[1:]):
			p, r ,d = map(int, line.split())
			tasks.append(Task(idx + 1, p, r, d))

		start = now()
		assign(machines, tasks)
		end = now()

		error = sum((calculate_error(m.tasks_submited) for m in machines.values()))
		print(error)
		print(f'{end - start:.5f}')

		output = open(f'out/{n}.txt', 'w')
		output.write(str(error))
		output.write('\n')
		for machine in machines.values():
			for task in machine.tasks_submited:
				output.write(f'{task.id} ')
			output.write('\n')


if __name__ == '__main__':
	run()
