#!/usr/bin/env python3
import sys
import os


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

        if j.ready_time <= self.time:
            self.time += j.proc_time
            self.tardiness += max(0, self.time - j.due_time)
            self.jobs.pop(0)
        else:
            self.time = j.ready_time


def key_function(job, time):
    ret = job.due_time

    if job.ready_time <= time:
        ret -= time

    return ret / job.proc_time


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
    time = 0
    machines = [Machine([], []) for i in range(4)]

    while len(jobs) > 0:
        jobs.sort(key=lambda x: key_function(x, time))

        for m in machines:
            if m.time <= time and len(jobs) > 0:
                j = jobs.pop(0)
                m.jobs.append(j)
                m.scheduled.append(j)
            
            m.consume()

        time = min(machines, key=lambda x: x.time).time

    tardiness = sum([m.tardiness for m in machines])

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
    output_path = os.path.join('results', '132251', 'a1', author, '{}.txt'.format(size))

    main(instance_path, output_path)
