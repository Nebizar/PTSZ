import sys
import math
from operator import itemgetter

machineCount = 4


def sort(instance):
#  inF = str(indeks) + "/" +str(inst) + ".txt"
  de = 0
  procsT=[0, 0, 0, 0]
  procsTasks=[[],[],[],[]]
  inFile = str(instance) + ".txt"
  outFile = str(instance) + "_r.txt"
  with open(inFile, 'r') as f:
    lines = f.readlines()
  size = int(lines.pop(0))
  for l in range(size):
    lines[l]=lines[l].split()
    lines[l] = list(map(int, lines[l]))
    lines[l].append(l+1)
  sortedList=sorted(lines, key=itemgetter(1,0))
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
      de = de + procsT[nextProc]-taskExpected
    procsTasks[nextProc].append(taskId)

  out = " ".join(str(item) for item in procsTasks[0])
  

  file1 = open(outFile,"w")
  file1.write(str(de))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[0]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[1]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[2]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[3])) 
  file1.close() 
  print(str(de))
def main():
  instance = sys.argv[1]
  sort(instance)
#  instanceSizes = range(50,501,50)
#  for i in instanceSizes:
#    chek(i, instance)
if __name__== "__main__":
  main()