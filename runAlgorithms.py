import os
import sys
from subprocess import Popen, PIPE


def main():
    # Run all algorithms from folder for given instance author
    # example: python runAlgorithms.py 132344 a1
    instance_author = str(sys.argv[1])
    algorithm = str(sys.argv[2])
    directory_list = list()
    for root, dirs, files in os.walk("algorithms/", topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(name))

    for algorithm_author in directory_list:
        for n in range(50, 501, 50):
            cmd = "python3 algorithms/{}/{}.py {} {}" \
                .format(algorithm_author,
                        algorithm,
                        instance_author,
                        n)
            p = Popen(cmd, shell=True, stdin=PIPE,
                      stdout=PIPE, stderr=PIPE)
            p.communicate()


if __name__ == "__main__":
    main()
