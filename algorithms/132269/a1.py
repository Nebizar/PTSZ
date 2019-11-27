import sys
import math
import os
import time
from operator import itemgetter

machineCount = 4

def main():
  sum = 0
  procsT=[0, 0, 0, 0]
  procsTasks=[[],[],[],[]]
  with open("instances/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "r") as f:
    lines = f.readlines()
  size = int(lines.pop(0))
  for l in range(size):
    lines[l]=lines[l].split()
    lines[l] = list(map(int, lines[l]))
    lines[l].append(l+1)
  sortedList=sorted(lines, key=itemgetter(1,2))
  for i in range(size):
    task = sortedList.pop(0)
    taskId=task[3]
    taskDuration=task[0]
    taskReady=task[1]
    taskExpected=task[2]
    nextProc=procsT.index(min(procsT))
    if (procsT[nextProc]<taskReady):
      procsT[nextProc] = taskReady
    procsT[nextProc]=procsT[nextProc]+taskDuration
    if (procsT[nextProc]>taskExpected):
      sum = sum + procsT[nextProc]-taskExpected
    procsTasks[nextProc].append(taskId)

  
  if not os.path.exists("results/" + "/132269/a1/" + sys.argv[1] + "/"):
    os.makedirs("results/" + "/132269/a1/" + sys.argv[1] + "/")
  file1 = open("results/" + "/132269/a1/" + sys.argv[1] + "/" + sys.argv[2] + ".txt", "w+")
  file1.write(str(sum))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[0]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[1]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[2]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[3])) 
  file1.close() 
    
if __name__== "__main__":
  main()