import os
import sys
from subprocess import Popen, PIPE
from timeit import default_timer as timer


class Job():
    def __init__(self, p, r, d):
        self.p = int(p)
        self.r = int(r)
        self.d = int(d)

    def __str__(self):
        return "{} {} {}".format(self.p, self.r, self.d)


class Machine():
    def __init__(self, id):
        self.id = id
        self.finished_jobs = []


def load_instance(file_path):
    with open(file_path, 'r') as f:
        data = f.readlines()

    data = [x.strip() for x in data]
    instance_size = int(data[0])
    raw_jobs = data[1:instance_size + 1]

    jobs = {}
    for i, line in enumerate(raw_jobs, 1):
        jobs[i] = Job(*line.split(" "))

    return instance_size, jobs


def load_result(file_path, machines=4):
    with open(file_path) as f:
        data = f.readlines()

    data = [x.strip() for x in data]
    tardiness = int(data[0])
    raw_assignments = data[1:machines + 1]

    machines = []
    for i, line in enumerate(raw_assignments, 1):
        machines.append(Machine(i))
        machines[-1].finished_jobs = list(map(int, line.split(" ")))

    return tardiness, machines


def calculate_tardiness(machines, jobs):
    total = 0
    for machine in machines:
        time = 0
        for job_id in machine.finished_jobs:
            time = jobs[job_id].r if time < jobs[job_id].r else time
            time += jobs[job_id].p
            total += 0 if time <= jobs[job_id].d else time - jobs[job_id].d
    return total


def print_verificator_output(mode, input_tardiness, actual_tardiness,
                             time_elapsed):
    print(actual_tardiness)
    if mode == 2:
        print(input_tardiness == actual_tardiness)
        print("{} ms".format(time_elapsed * 1000))


def main():
    # mode 1 example: python verificator.py 1 132279
    # mode 2 example: python verificator.py 2 132279 132279 a1
    mode = int(sys.argv[1])
    instance_author = str(sys.argv[2])
    try:
        algorithm_author = str(sys.argv[3])
        algorithm = str(sys.argv[4])
    except IndexError:
        if mode != 1:
            raise IndexError

    for n in range(50, 501, 50):
        instance_file_path = os.path.join(
            "instances",
            instance_author,
            "{}.txt".format(n))
        time_elapsed = 0
        if mode == 1:
            result_file_path = os.path.join(
                "test_results",
                "{}.txt".format(n))
        else:
            result_file_path = os.path.join(
                "results",
                str(algorithm_author),
                str(algorithm),
                str(instance_author),
                "{}.txt".format(n))

            start = timer()
            cmd = "python3 algorithms/{}/{}.py {} {}" \
                  .format(algorithm_author,
                          algorithm,
                          instance_author,
                          n)
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            p.communicate()
            end = timer()
            time_elapsed = end - start

        try:
            instance_size, jobs = load_instance(instance_file_path)
        except IOError:
            print("Instance {}.txt missing".format(n))
            continue

        input_tardiness, machines = load_result(result_file_path)
        actual_tardiness = calculate_tardiness(machines, jobs)
        print_verificator_output(mode, input_tardiness, actual_tardiness,
                                 time_elapsed)


if __name__ == "__main__":
    main()