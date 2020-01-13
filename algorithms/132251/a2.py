#!/usr/bin/env python3
import math
import os
import random
import sys
import time
import copy


class Job:
    count = 1

    def __init__(self, proc_time, ready_time, due_time):
        self.proc_time = proc_time
        self.ready_time = ready_time
        self.due_time = due_time
        self.idx = self.count


    def __str__(self):
        times = (self.proc_time, self.ready_time, self.due_time)
        return '{} {} {}'.format(*times)


class Machine:
    def __init__(self, job_idxs, jobs):
        self.jobs = [jobs[i - 1] for i in job_idxs]
        self.scheduled = []
        self.time = 0
        self.tardiness = 0

    def __bool__(self):
        return self.done()

    def done(self):
        return len(self.jobs) == 0

    def consume(self):
        if len(self.jobs) == 0:
            return

        j = self.jobs[0]
        
        if j.ready_time > self.time:
            self.time = j.ready_time
        
        self.time += j.proc_time
        self.tardiness += max(0, self.time - j.due_time)
        self.jobs.pop(0)


def key_function(job, time):
    ret = job.due_time

    if job.ready_time <= time:
        ret -= time

    return ret / job.proc_time


def calculate_tardiness(machines):
    tardiness = 0

    for m in machines:
        time = 0

        for j in m.scheduled:
            time = time if time >= j.ready_time else j.ready_time
            time += j.proc_time
            tardiness += max(0, time - j.due_time)

    return tardiness


def random_swap(machines, n):
    # get machine
    m = random.choice(machines)

    # get random job from it
    j = random.choice(m.scheduled)
    m.scheduled.remove(j)

    # get new random machine
    m = random.choice(machines)

    # insert job at random index
    idx = random.randint(0, n - 1)
    m.scheduled.insert(idx, j)
    

def acceptance(current, new, temp):
    if current >= new:
        return 1
    else:
        try:
            ret = math.exp(-1000*(current - new) / temp)
        except OverflowError:
            ret = 0

        return ret


def main(instance, output):
    # read instance file
    jobs = []
    with open(instance) as f:
        for line in f:
            line = [int(x) for x in line.split()]
            if len(line) > 1:
                jobs.append(Job(*line))
                Job.count += 1

    # create machines
    n = len(jobs)
    machines = [Machine([], []) for i in range(4)]

    # initial calc
    cur_time = 0
    jobs_init = jobs[:]
    while len(jobs_init) > 0:
        available = [j for j in jobs_init if j.ready_time <= cur_time]
        if len(available) == 0:
            cur_time = min(jobs_init, key=lambda x: x.ready_time).ready_time
            continue

        for m in machines:
            if m.time <= cur_time and len(jobs) > 0 and len(available) != 0:
                j = min(available, key=lambda x: x.proc_time)
                available.remove(j)
                jobs_init.remove(j)

                m.jobs.append(j)
                m.scheduled.append(j)
            
            m.consume()

        cur_time = min(machines, key=lambda x: x.time).time

    tardiness = sum([m.tardiness for m in machines])

    # first test run for timing
    start = time.time()
    machines_n = copy.deepcopy(machines)#[Machine([], []) for i in range(4)]
    random_swap(machines_n, n)
    tardiness_n = calculate_tardiness(machines_n)

    if acceptance(tardiness, tardiness_n, 0.01) > random.random():
        tardiness = tardiness_n
        machines = machines_n

    duration = (time.time() - start) * 1000

    steps = int(10 * len(jobs) / duration)
    #steps = 10

    for i in range(steps):
        # calculate current temperature
        temp = steps / (i + 1)

        machines_n = copy.deepcopy(machines)#[Machine([], []) for i in range(4)]
        random_swap(machines_n, n)
        tardiness_n = calculate_tardiness(machines_n)

        if acceptance(tardiness, tardiness_n, temp) > random.random():
            tardiness = tardiness_n
            machines = machines_n

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as f:
        f.write(str(tardiness))
        f.write('\n')

        for m in machines:
            f.write(' '.join([str(j.idx) for j in m.scheduled]))
            f.write('\n')


if __name__ == '__main__':
    author = sys.argv[1]
    size = sys.argv[2]
    
    instance_path = os.path.join('instances', author, '{}.txt'.format(size))
    output_path = os.path.join('results', '132251', 'a2', author, '{}.txt'.format(size))

    main(instance_path, output_path)
