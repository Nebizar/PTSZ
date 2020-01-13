import os
import sys
import random
import copy
import shutil
from timeit import default_timer as timer


class Machine:
    def __init__(self):
        self.clear()

    def clear(self):
        self.time = 0
        self.tardiness = 0
        self.current_job_end_time = 0
        self.current_job = None
        self.past_jobs = []

    def __str__(self):
        output_template = "{} "*len(self.past_jobs)
        output_template = output_template.strip()
        return output_template.format(*[j[0] for j in self.past_jobs])

    def is_busy(self):
        return False if self.current_job is None else True

    def finish_job(self):
        if self.current_job is not None:
            self.tardiness += 0 \
                if self.current_job_end_time <= self.current_job[3] \
                else self.current_job_end_time - self.current_job[3]

            self.past_jobs.append(self.current_job)
            self.current_job = None

    def start_job(self, job):
        self.current_job = job
        self.current_job_end_time = self.time + self.current_job[1]

    def update(self, new_time):
        self.time = new_time
        if self.time >= self.current_job_end_time and \
                self.current_job is not None:
            self.finish_job()


def load_instance(file_path):
    with open(file_path, "rU") as f:
        data = f.readlines()

    data = [x.strip() for x in data]
    instance_size = int(data[0])
    raw_jobs = data[1:instance_size + 1]

    jobs = []
    for i, line in enumerate(raw_jobs, 1):
        s = line.split(" ")
        s2 = tuple(map(int, s))
        jobs.append((i, s2[0], s2[1], s2[2]))

    return instance_size, jobs


def get_free_machine(machines):
    for m in machines:
        if not m.is_busy():
            return m
    else:
        return None

def update_machines(machines, time):
    for m in machines:
        m.update(time)

def save_result(result,
                algorithm_author,
                algorithm,
                instance_author,
                instance_size):
    filename = os.path.join("results",
                            str(algorithm_author),
                            str(algorithm),
                            str(instance_author),
                            "{}.txt".format(instance_size))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(result)

def main():
    algorithm_author = "132279"
    algorithm = "a2"
    instance_author = sys.argv[1]
    instance_size = sys.argv[2]
    instance_file_path = os.path.join("instances",
                                      instance_author,
                                      "{}.txt".format(instance_size))
    instance_size, loaded_jobs = load_instance(instance_file_path)

    start = timer()
    loaded_jobs.sort(key=lambda j: j[2])
    machines = [Machine() for i in range(4)]
    best_tardiness = None
    best_result = None
    while True:
        jobs = copy.deepcopy(loaded_jobs)
        for m in machines:
            m.clear()
        time = 0
        for n in range(instance_size):
            # choose machine
            update_machines(machines, time)
            chosen_machine = get_free_machine(machines)
            if chosen_machine is None:
                time = min([m.current_job_end_time for m in machines])
                update_machines(machines, time)
                chosen_machine = get_free_machine(machines)

            # choose job
            availible_jobs = [j for j in jobs if j[2] <= time]
            if len(availible_jobs) < 1:
                time = jobs[0][2]
                availible_jobs = [j for j in jobs if j[2] <= time]

            availible_jobs.sort(key=lambda j: j[1])
            chosen_job = random.choice(availible_jobs[:3])
            update_machines(machines, time)
            chosen_machine.start_job(chosen_job)
            jobs.remove(chosen_job)

        for m in machines:
            m.finish_job()
        tardiness = sum([m.tardiness for m in machines])

        if (best_tardiness is None) or (tardiness < best_tardiness):
            best_tardiness = tardiness
            best_result = "{}\n{}\n{}\n{}\n{}\n" \
                .format(best_tardiness, *machines)

        end = timer()
        time_elapsed = end - start
        if time_elapsed > (int(instance_size)*0.01):
            break

    save_result(best_result,
                algorithm_author,
                algorithm,
                instance_author,
                instance_size)


if __name__ == "__main__":
    main()
