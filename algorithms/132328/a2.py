from operator import itemgetter
import sys
import os
import time
import random

def find_ready_task(task,l,machine_time, grasp):
    find=0
    j=0
    min_r=task[0][1]
    min_indeks=0
    ready_task_indeks=[]
    while find<grasp and j<l:
        if task[j][1]<=machine_time:
            ready_task_indeks.append(j)
            find+=1
        elif task[j][1]<min_r:
            min_r=task[j][1]
            min_indeks=j
        j+=1
    #j-=1
    if find>0:
        j=ready_task_indeks[random.randrange(len(ready_task_indeks))]
    else:
        k=0
        while k<min_r and task[k][1]>task[min_indeks][1]+task[min_indeks][0]*0.4:
            k+=1
        if grasp==1 or task[k][1]>task[min_indeks][1]+task[min_indeks][0]*0.4:
            j=min_indeks
        else:
            if random.randrange(grasp)==0:
                j=k
            else:
                j=min_indeks
    return j

def two_phase_scheduling(n, param, grasp):
    sumP=[[0,0],[0,1],[0,2],[0,3]]
    tasks=[[],[],[],[]]
    task_list=[[],[],[],[]]
    machine_time=[[0,0],[0,1],[0,2],[0,3]]
    param.sort(key=itemgetter(3))
    sumD=0
    
    for i in range(n):
        mini_indeks=min(sumP)[1]
        mini=max(sumP)[0]
        mini_indeks2=-1
        for k in range(4):
            if k!=mini_indeks and sumP[k][0]<=mini:
                mini=sumP[k][0]
                mini_indeks2=k
          
        if random.randrange(grasp)==0:
            j=mini_indeks
        else:
            j=mini_indeks2

        task_list[j].append(param[i])
        sumP[j][0]+=param[i][0]               
                    
    for j in range(4):
        task_list[j].sort(key=itemgetter(0))
            
    for k in range(4):
        i=0
        while i<len(task_list[k]):            
            j=find_ready_task(task_list[k],len(task_list[k]),machine_time[k][0], grasp)
                    
            machine_time[k][0]=max(task_list[k][j][1],machine_time[k][0])+task_list[k][j][0]
            sumD+=max(0,machine_time[k][0]-task_list[k][j][2])
            tasks[machine_time[k][1]].append(task_list[k][j][4])
            task_list[k].pop(j)
            
    return tasks,sumD
            
            
def one_phase_scheduling(n, param, grasp):
    tasks=[[],[],[],[]]
    machine_time=[[0,0],[0,1],[0,2],[0,3]]
    param.sort(key=itemgetter(0))
    param.sort(key=itemgetter(3))
    sumD=0
    
    for i in range(n):
        machine_time.sort()
        j=find_ready_task(param,len(param),machine_time[0][0], grasp)
                    
        machine_time[0][0]=max(param[j][1],machine_time[0][0])+param[j][0]
        sumD+=max(0,machine_time[0][0]-param[j][2])
        tasks[machine_time[0][1]].append(param[j][4])
        param.pop(j)
    
    return tasks,sumD

if __name__ == "__main__": 
    start_time = time.time()           
    indeks=sys.argv[1]
    n=int(sys.argv[2])

    max_time=start_time+0.01*n-0.25
    
    file = open("instances/"+indeks+"/"+str(n)+".txt", "r")
    if not os.path.exists("results/132328/a2/" + indeks + "/"):
        os.makedirs("results/132328/a2/" + indeks + "/")
    output = open("results/132328/a2/" + indeks + "/" + str(n) + ".txt", "w")
    
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
    
    grasp=2
    if r/n<=p/4*0.4:
        best_solution,best_solution_delay=two_phase_scheduling(n,param.copy(),1) 
    else:
        best_solution,best_solution_delay=one_phase_scheduling(n,param.copy(),1) 
        
    if r/n<=p/4*0.4:
        while(time.time()<max_time):
            tasks,sumD=two_phase_scheduling(n,param.copy(), grasp)
            if sumD<best_solution_delay:
                best_solution=tasks
                best_solution_delay=sumD
    else:
        while(time.time()<max_time):
            tasks,sumD=one_phase_scheduling(n,param.copy(), grasp)  
            if sumD<best_solution_delay:
                best_solution=tasks
                best_solution_delay=sumD
    
    output.write(str(best_solution_delay)+'\n')
    for i in best_solution:
        for j in i:
            output.write(str(j)+' ')
        output.write('\n')
    output.close()
    #stop_time = time.time()
    #print(stop_time-start_time)
    #print(sumD)


