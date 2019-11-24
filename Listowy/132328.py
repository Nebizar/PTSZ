from operator import itemgetter
import sys

def find_ready_task(task,l,machine_time):
    find=False
    j=0
    min_r=task[0][1]
    min_indeks=0
    while not find and j<l:
        if task[j][1]<=machine_time:
            find=True
        elif task[j][1]<min_r:
            min_r=task[j][1]
            min_indeks=j
        j+=1
    j-=1
    if not find:
        j=min_indeks  
    return j

def two_phase_scheduling(n, param):
    sumP=[[0,0],[0,1],[0,2],[0,3]]
    tasks=[[],[],[],[]]
    task_list=[[],[],[],[]]
    machine_time=[[0,0],[0,1],[0,2],[0,3]]
    param.sort(key=itemgetter(3))
    sumD=0
        
    for i in range(n):
        j=min(sumP)[1]
        task_list[j].append(param[i])
        sumP[j][0]+=param[i][0]               
                    
    for j in range(4):
        task_list[j].sort(key=itemgetter(0))
            
    for k in range(4):
        i=0
        while i<len(task_list[k]):            
            j=find_ready_task(task_list[k],len(task_list[k]),machine_time[k][0])
                    
            machine_time[k][0]=max(task_list[k][j][1],machine_time[k][0])+task_list[k][j][0]
            sumD+=max(0,machine_time[k][0]-task_list[k][j][2])
            tasks[machine_time[k][1]].append(task_list[k][j][4])
            task_list[k].pop(j)
            
    return tasks,sumD
            
            
def one_phase_scheduling(n, param):
    tasks=[[],[],[],[]]
    machine_time=[[0,0],[0,1],[0,2],[0,3]]
    param.sort(key=itemgetter(0))
    param.sort(key=itemgetter(3))
    sumD=0
    
    for i in range(n):
        machine_time.sort()
        j=find_ready_task(param,len(param),machine_time[0][0])
                    
        machine_time[0][0]=max(param[j][1],machine_time[0][0])+param[j][0]
        sumD+=max(0,machine_time[0][0]-param[j][2])
        tasks[machine_time[0][1]].append(param[j][4])
        param.pop(j)
    
    return tasks,sumD

if __name__ == "__main__":            
    indeks=sys.argv[1]
    n=int(sys.argv[2])
    
    file = open("instances/"+indeks+"/"+str(n)+".txt", "r")
    output=open("results/"+indeks+"/"+str(n)+".txt", "w")
    param=[]
    lines=file.readline()
    lines=file.readlines()
    j=1
    p=0
    r=0
    for l in lines:
        line=l.split()
        pom=[]
        for i in line:
            pom.append(int(i))
        pom.append(pom[2]-0.75*pom[0])
        pom.append(j)
        p+=pom[0]
        r+=pom[1]
        param.append(pom)
        j+=1
    file.close()
    
       
    if r/n<=p/4*0.4:
        tasks,sumD=two_phase_scheduling(n,param)
    else:
        tasks,sumD=one_phase_scheduling(n,param)           
    
    output.write(str(sumD)+'\n')
    for i in tasks:
        for j in i:
            output.write(str(j)+' ')
        output.write('\n')
    output.close()
    #print(sumD)


