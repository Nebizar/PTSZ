import os
import sys


class Machine:
    def __init__(self):
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
        jobs.append((i, *tuple(map(int, line.split(" ")))))

    return instance_size, jobs


def get_free_machine_id(machines):
    for i, m in enumerate(machines, 0):
        if not m.is_busy():
            return i
    else:
        return None


def update_machines(machines, time):
    for m in machines:
        m.update(time)


def finish_last_jobs(machines):
    for m in machines:
        m.finish_job()


def sum_tardiness(machines):
    total = 0
    for m in machines:
        total += m.tardiness
    return total


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
    algorithm = "a1"
    instance_author = sys.argv[1]
    instance_size = sys.argv[2]
    instance_file_path = os.path.join("instances",
                                      instance_author,
                                      "{}.txt".format(instance_size))
    instance_size, jobs = load_instance(instance_file_path)
    machines = [Machine() for i in range(4)]
    time = 0

    for n in range(instance_size):
        # choose machine
        update_machines(machines, time)
        chosen_machine_id = get_free_machine_id(machines)
        while chosen_machine_id is None:
            time += min([m.current_job_end_time for m in machines]) - time
            update_machines(machines, time)
            chosen_machine_id = get_free_machine_id(machines)

        # choose job
        availible_jobs = [j for j in jobs if j[2] <= time]
        while len(availible_jobs) < 1:
            time += min([j[2] for j in jobs]) - time
            availible_jobs = [j for j in jobs if j[2] <= time]

        chosen_job = min(availible_jobs, key=lambda j: j[1])
        update_machines(machines, time)
        machines[chosen_machine_id].start_job(chosen_job)
        jobs.remove(chosen_job)

    finish_last_jobs(machines)
    tardiness = sum_tardiness(machines)

    result = "{}\n{}\n{}\n{}\n{}\n" \
        .format(tardiness, *machines)

    save_result(result,
                algorithm_author,
                algorithm,
                instance_author,
                instance_size)


if __name__ == "__main__":
    main()
