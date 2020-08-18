'''
Description: 
Author: CheeReus_11
Date: 2020-08-18 11:07:35
LastEditTime: 2020-08-18 11:14:03
LastEditors: CheeReus_11
'''
import codecs
path="data/result_chr.txt"
f=codecs.open(path,mode="r",encoding="utf-8")
line=f.readline()
list=[]
while line:
    a=line.split()
    b=a[3]
    list.append(b)
    line=f.readline()
f.close()

from math import log
def calcShannonEnt(list):
    ShannonEnt=0
    for maf in list:
        maf = float(maf)
        ShannonEnt=ShannonEnt-maf*log(maf,2)-(1-maf)*log((1-maf),2)
    return ShannonEnt
ShannonEnt=calcShannonEnt(list)
print(ShannonEnt)
