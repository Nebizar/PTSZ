import os
import sys


def readTasks(i, instance_file_path):
    tasks = []
    p = []
    r = []
    d = []
    file = open(instance_file_path, "r")
    noTasks = file.readline()
    lines = file.readlines()
    for line in lines:
        line = line.split()
        p.append(line[0])
        r.append(line[1])
        d.append(line[2])
    p = list(map(int, p))
    r = list(map(int, r))
    d = list(map(int, d))
    tasks.append(p)
    tasks.append(r)
    tasks.append(d)
    return tasks, noTasks


def sortTasks(tasks, i):
    indexes = []
    tempArray = []
    reformedTasks = []
    tasks_r = []
    for x in range(0, int(i)):
        tempArray.append(x)
        tempArray.append(tasks[0][x])
        tempArray.append(tasks[1][x])
        tempArray.append(tasks[2][x])
        indexes.append(x + 1)
        reformedTasks.append(tempArray)
        tasks_r.append(tempArray)
        tempArray = []
    reformedTasks.sort(key=lambda x: (x[3], x[2]))
    tasks_r.sort(key=lambda x: (x[2], x[3]))
    return reformedTasks, tasks_r


def orderTasks(tasks_d, tasks_r, i, times, taskOrder, ds):
    for y in range(0, int(i)):
        single_tardiness = 0
        processor_no = times.index((min(times)))
        if times[processor_no] >= tasks_d[0][2]:
            times[processor_no] = times[processor_no] + tasks_d[0][1]
            taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
            single_tardiness = times[processor_no] - tasks_d[0][3]
            del tasks_r[tasks_r.index(tasks_d[0])]
            del tasks_d[0]
        else:
            if tasks_d[0][2] >= tasks_r[0][2]:  # jesli d moze sie zaczac przed r
                times[processor_no] = tasks_d[0][2] + tasks_d[0][1]
                taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
                single_tardiness = times[processor_no] - tasks_d[0][3]
                del tasks_r[tasks_r.index(tasks_d[0])]
                del tasks_d[0]
            else:
                if times[processor_no] >= tasks_d[0][2]:  # jesli r mozna juz od razu wykonywac
                    if (tasks_d[0][1] + tasks_d[0][2]) < (times[processor_no] + tasks_r[0][1]):
                        times[processor_no] = tasks_d[0][2] + tasks_d[0][1]
                        taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
                        single_tardiness = times[processor_no] - tasks_d[0][3]
                        del tasks_r[tasks_r.index(tasks_d[0])]
                        del tasks_d[0]
                    else:
                        times[processor_no] = tasks_r[0][2] + tasks_r[0][1]
                        taskOrder[processor_no].append(str(tasks_r[0][0] + 1))
                        single_tardiness = times[processor_no] - tasks_r[0][3]
                        del tasks_d[tasks_d.index(tasks_r[0])]
                        del tasks_r[0]
                else:  # jesli r nie mozna od razu wykonywac
                    if (tasks_d[0][1] + tasks_d[0][2]) < (tasks_r[0][1] + tasks_r[0][2]):
                        times[processor_no] = tasks_d[0][2] + tasks_d[0][1]
                        taskOrder[processor_no].append(str(tasks_d[0][0] + 1))
                        single_tardiness = times[processor_no] - tasks_d[0][3]
                        del tasks_r[tasks_r.index(tasks_d[0])]
                        del tasks_d[0]
                    else:
                        times[processor_no] = tasks_r[0][2] + tasks_r[0][1]
                        taskOrder[processor_no].append(str(tasks_r[0][0] + 1))
                        single_tardiness = times[processor_no] - tasks_r[0][3]
                        del tasks_d[tasks_d.index(tasks_r[0])]
                        del tasks_r[0]
        if single_tardiness > 0:
            ds[processor_no] = ds[processor_no] + single_tardiness


# def saveToFile(i):
#     file = open(str(i) + "out.txt", "w+")
#     file.write(str(sum(ds)) + "\n")
#     for x in range(0, 4):
#         for y in range(0, len(taskOrder[x])):
#             file.write(str(taskOrder[x][y]) + " ")
#         file.write("\n")


def save_result(algorithm_author, algorithm, instance_author, instance_size, taskOrder, ds):
    print("zapisuje")
    filename = os.path.join("results",
                            str(algorithm_author),
                            str(algorithm),
                            str(instance_author),
                            "{}.txt".format(instance_size))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(str(sum(ds)) + "\n")
        for x in range(0, 4):
            for y in range(0, len(taskOrder[x])):
                f.write(str(taskOrder[x][y]) + " ")
            f.write("\n")


def main():
    print("zaczynam")
    algorithm_author = "132274"
    algorithm = "a1"
    instance_author = sys.argv[1]
    instance_size = sys.argv[2]
    instance_file_path = os.path.join("instances",
                                      instance_author,
                                      "{}.txt".format(instance_size))

    tasks, noTasks = readTasks(instance_size, instance_file_path)
    tasks_d, tasks_r = sortTasks(tasks, instance_size)
    times = []
    ds = []
    taskOrder = [[], [], [], []]
    for x in range(0, 4):
        times.append(0)
        ds.append(0)
    orderTasks(tasks_d, tasks_r, instance_size, times, taskOrder, ds)

    save_result(algorithm_author,
                algorithm,
                instance_author,
                instance_size, taskOrder, ds)


if __name__ == "__main__":
    main()

# for z in range(50, 550, 50):
#     instanceSize = z
#     # instanceSize = z
#     tasks, noTasks = readTasks(instanceSize)
#     tasks_d, tasks_r = sortTasks(tasks, instanceSize)
#     times = []
#     ds = []
#     taskOrder = [[], [], [], []]
#     for x in range(0, 4):
#         times.append(0)
#         ds.append(0)
#     start_time = time.time()
#     orderTasks(tasks_d, tasks_r, instanceSize, times, taskOrder, ds)
#     elapsed_time = time.time() - start_time
#     print(elapsed_time)
#     saveToFile(instanceSize)
