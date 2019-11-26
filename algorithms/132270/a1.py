#!/usr/bin/env python3


import sys
import os

def toSort(k):
    numb = int(k[1]/10)
    leng = int(k[0]/10)
    return [numb,leng,k[2]]

def listowy(inst,inst_size):
    with open("instances/"+str(inst)+"/"+str(inst_size)+".txt") as f:
        n = [int(x) for x in next(f).split()]
        inst_ar = [[int(x) for x in line.split()] for line in f]
    for i in range(len(inst_ar)):
        inst_ar[i].append(i+1)
    k=[0,0,0,0]
    ke=["","","",""]
    meh=[[],[],[],[]]
    inst_ar.sort(key=toSort)
    for i in range(len(inst_ar)):
        m=k.index(min(k))
        ke[m]=ke[m]+str(inst_ar[i][3])+" "
        meh[m].append(inst_ar[i][3])
        k[m]=max(k[m],inst_ar[i][1])+inst_ar[i][0]
    if not os.path.exists("results/" + "/132270/a1/" + sys.argv[1] + "/"):
        os.makedirs("results/" + "/132270/a1/" + sys.argv[1] + "/")
    outFile = open("results/" +"132270/a1/"+str(inst)+"/"+str(inst_size) +".txt", "w+")
    q=wer2("instances/"+str(inst)+"/"+str(inst_size)+".txt", meh)
    outFile.write(str(q)+"\n")
    for i in range(len(ke)):
        outFile.write(ke[i]+"\n")
    
def wer2(inst, kolej):
    k=[0,0,0,0]
    wynik=0
    with open(inst) as f:
        n = [int(x) for x in next(f).split()]
        inst_ar = [[int(x) for x in line.split()] for line in f]
    array = kolej
    for i in range(len(array)):
        for j in range(len(array[i])):
            k[i]=max(k[i],inst_ar[array[i][j]-1][1])+inst_ar[array[i][j]-1][0]
            wynik = wynik + max(0,k[i]-inst_ar[array[i][j]-1][2])
    return wynik

def main():
    listowy(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    main()
        
