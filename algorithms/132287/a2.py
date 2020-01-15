from sys import argv
from copy import copy, deepcopy
import os
from time import time as now
from random import randrange
from operator import attrgetter


class Task:
	def __init__(self, id, p, r, d):
		self.id = id
		self.p = p
		self.r = r
		self.d = d

	def __repr__(self):
		return '<Task id {}>'.format(self.id)


class Machine: 
	def __init__(self, id, current_time=0, tasks_submited=None):
		self.id = id
		self.current_time = current_time
		self.tasks_submited = tasks_submited or []

	def __repr__(self):
		return '<Machine id {} tasks {}>'.format(self.id, self.tasks_submited)


class Solution:
	def __init__(self, machines, fitness):
		self.machines = machines
		self.fitness = fitness

	def __repr__(self):
		return '<Solution {} {}>'.format(self.fitness, self.machines)

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


def calculate_fitness(machines):
	return sum((calculate_error(m.tasks_submited) for m in machines))


def find_first_available(machines, task):
	least_occupied = sorted(machines, key=attrgetter('current_time'))[0]
	least_occupied.tasks_submited.append(copy(task))
	if task.r < least_occupied.current_time:
		least_occupied.current_time += task.p
	else:
		least_occupied.current_time = task.r + task.p


def assign(machines, tasks):
	tasks_sorted = sorted(tasks, key=attrgetter('r', 'p'))
	while tasks_sorted:
		find_first_available(machines, tasks_sorted[0])
		tasks_sorted.pop(0)


def generate_initial_solution(tasks):
	machines = [Machine(id=i) for i in range(4)]
	assign(machines, tasks)
	fitness = calculate_fitness(machines)
	return Solution(machines, fitness)


def generate_candidates(candidate, candidates_size, n):
	candidates = []
	for _ in range(candidates_size):
		machines = deepcopy(candidate.machines)
		num_of_exchanges = max(1, int(0.2 * (n // 50)**2))
		print(num_of_exchanges)
		for _ in range(num_of_exchanges):
			m0_idx = randrange(len(machines))
			m1_idx = randrange(len(machines))
			m0 = machines[m0_idx]
			m1 = machines[m1_idx]

			t0_idx = randrange(len(m0.tasks_submited))
			t1_idx = randrange(len(m1.tasks_submited))
			t0 = m0.tasks_submited[t0_idx]
			t1 = m1.tasks_submited[t1_idx]

			m0.tasks_submited[t0_idx] = t1
			m1.tasks_submited[t1_idx] = t0

		candidates.append(Solution(machines, calculate_fitness(machines)))
	return candidates


def schedule(n, tasks):
	start = now()
	limit = float(n) * 0.01 - 0.08
	time_taken = 0.0
	tabu_size = int(n) // 2.5
	candidates_size = int(n) // 4
	tabu_list = []
	initial_solution = generate_initial_solution(tasks)
	print(initial_solution.fitness)
	best_candidate = initial_solution
	best_solution = initial_solution
	while time_taken < limit:
		close_solutions = generate_candidates(best_candidate, candidates_size, int(n))
		for candidate in close_solutions:
			if not candidate in tabu_list and candidate.fitness < best_candidate.fitness:
				best_candidate = candidate
		if best_candidate.fitness < best_solution.fitness:
			best_solution = best_candidate
		if best_candidate not in tabu_list:
			tabu_list.append(best_candidate)
		if len(tabu_list) > tabu_size:
			tabu_list.pop(0)
		time_taken = now() - start
	return best_solution


def run():
	_, index, n = argv

	machines = [Machine(id=i) for i in range(4)]
	tasks = []

	input_file = open('instances/{index}/{n}.txt'.format(index=index, n=n))
	for idx, line in enumerate(input_file.readlines()[1:]):
		p, r ,d = map(int, line.split())
		tasks.append(Task(idx + 1, p, r, d))

	best = schedule(n, tasks)

	output_dir = 'results/132287/a1/{index}'.format(index=index)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	output = open('{output_dir}/{n}.txt'.format(output_dir=output_dir, n=n), 'w')
	output.write(str(best.fitness))
	output.write('\n')
	for machine in best.machines:
		output.write(' '.join((str(task.id) for task in machine.tasks_submited)))
		output.write('\n')


if __name__ == '__main__':
	run()
