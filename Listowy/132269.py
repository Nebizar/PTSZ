import sys
import math
from operator import itemgetter
import time

def sortFile(instance):
#  inF = str(indeks) + "/" +str(inst) + ".txt"
  res = 0
  procsT=[0, 0, 0, 0]
  procsTasks=[[],[],[],[]]
  inFile = "in/" + str(instance) + ".txt"
  outFile = "out/" +str(instance) + ".txt"
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
      res = res + procsT[nextProc]-taskExpected
    procsTasks[nextProc].append(taskId)

  out = " ".join(str(item) for item in procsTasks[0])
  

  file1 = open(outFile,"w+")
  file1.write(str(res))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[0]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[1]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[2]))
  file1.write( "\n")
  file1.write( " ".join(str(item) for item in procsTasks[3])) 
  file1.close() 
  return(res)
def main():
#  instance = sys.argv[1]
#  sortFile(instance)
  instanceSizes = range(50,501,50)
  results = []
  print("Czasy:")
  for instance in instanceSizes:
    start=time.time()
    result = sortFile(instance)
    end=time.time()
    print("%.5f"%(end-start))
    results.append(result)
  print("\nWyniki:")
  for i in results:
    print(i)
if __name__== "__main__":
  main()