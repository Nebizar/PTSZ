#!/usr/bin/env python3

import time
import sys
import os
import random

def toSort(k):
    numb = int(k[1]/10)
    leng = int(k[0]/10)
    return [numb,leng,k[2]]


def wer(inst, kolej):
    k=[0,0,0,0]
    wynik=0
    for i in range(len(kolej)):
        for j in range(len(kolej[i])):
            k[i]=max(k[i],inst[kolej[i][j]-1][1])+inst[kolej[i][j]-1][0]
            wynik = wynik + max(0,k[i]-inst[kolej[i][j]-1][2])
    return wynik      

def alg(inst,inst_size):
    with open("instances/"+str(inst)+"/"+str(inst_size)+".txt") as f:
        n = [int(x) for x in next(f).split()]
        inst_ar = [[int(x) for x in line.split()] for line in f]
    for i in range(len(inst_ar)):
        inst_ar[i].append(i+1)
    q=0
    k=[0,0,0,0]
    ke=["","","",""]
    meh=[[],[],[],[]]
    wer_ar=inst_ar.copy()
    inst_ar.sort(key=toSort)
    for i in range(len(inst_ar)):
        m=k.index(min(k))
        n=i
        ke[m]=ke[m]+str(inst_ar[n][3])+" "
        k[m]=max(k[m],inst_ar[n][1])+inst_ar[n][0]
        meh[m].append(inst_ar[n][3])
    q=wer(wer_ar,meh)
    timeout = time.time() + len(inst_ar)*10*0.001-0.4
    while (timeout>time.time()):
        inst_ar1=inst_ar.copy()
        a1=random.randint(0,len(inst_ar1)-1)
        a2=random.randint(0,len(inst_ar1)-1)
        inst_ar1[a1], inst_ar1[a2] = inst_ar1[a2] , inst_ar1[a1]
        q1=0
        k1=[0,0,0,0]
        ke1=["","","",""]
        meh1=[[],[],[],[]]
        for i in range(len(inst_ar1)):
            m=k1.index(min(k1))
            n=i
            ke1[m]=ke1[m]+str(inst_ar1[n][3])+" "
            k1[m]=max(k1[m],inst_ar1[n][1])+inst_ar1[n][0]
            meh1[m].append(inst_ar1[n][3])
        q1=wer(wer_ar,meh1)
    
        if(q>q1):
            q=q1
            meh=meh1.copy()
            ke=ke1.copy()
            inst_ar=inst_ar1.copy()

    if not os.path.exists("results/" + "/132270/a2/" + str(inst) + "/"):
        os.makedirs("results/" + "/132270/a2/" +str(inst)+ "/")
    outFile = open("results/" +"132270/a2/"+str(inst)+"/"+str(inst_size) +".txt", "w+")
    outFile.write(str(q)+"\n")
    for i in range(len(ke)):
        outFile.write(ke[i]+"\n")

def main():
    alg(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
        
