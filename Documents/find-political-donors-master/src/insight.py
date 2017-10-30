
# coding: utf-8

# In[130]:

from functools import reduce
import collections
from statistics import median
import sys

inFile = sys.argv[1]
out1File = sys.argv[2]
out2File = sys.argv[3]
with open(inFile,'r') as i:
    lines = i.readlines()

CMTE_ID=[]
ZIP_CODE=[]
TRANSACTION_DT=[]
TRANSACTION_AMT=[]
LENGTH=[]
TOTAL=[]

for line in lines:
    fields = line.split('|')
    if not fields[15]:
        CMTE_ID.append(fields[0]) # prints the first fields value
        ZIP_CODE.append(fields[10][:5]) # prints the 11th fields value
        TRANSACTION_DT.append(fields[13]) # prints the 12th fields value
        TRANSACTION_AMT.append(int(fields[14])) # prints the 13th fields value
        LENGTH.append(1) 
        TOTAL.append(int(fields[14]))
          
d_zip=[]
d_date=[]

duID=[item for item, count in collections.Counter(CMTE_ID).items() if count > 1]  
duZ=[item for item, count in collections.Counter(ZIP_CODE).items() if count > 1] 
duD=[item for item, count in collections.Counter(TRANSACTION_DT).items() if count > 1] 

def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

for i in duID:
    for j in duZ:
        IDl=duplicates(CMTE_ID, i)
        Zl=duplicates(ZIP_CODE, j)
        common1=list(set(IDl).intersection(Zl))
        if len(common1)>1:
            d_zip.append(common1)

for i in duID:
    for j in duD:
        ID2=duplicates(CMTE_ID, i)
        D2=duplicates(TRANSACTION_DT, j)
        common2=list(set(ID2).intersection(D2))
        if len(common2)>1:
            d_date.append(common2)
            
CMTE_IDz=list(CMTE_ID)
ZIP_CODEz=list(ZIP_CODE)
TRANSACTION_AMTz=list(TRANSACTION_AMT)
LENGTHz=list(LENGTH)
TOTALz=list(TOTAL)
CMTE_IDd=list(CMTE_ID)
TRANSACTION_DTd=list(TRANSACTION_DT)
TRANSACTION_AMTd=list(TRANSACTION_AMT)
LENGTHd=list(LENGTH)
TOTALd=list(TOTAL)

ex_ls=[]
for idz in d_zip:
    ex_ls.extend(idz[1:])
    MEAN_AMTz=[v for w,v in enumerate(TRANSACTION_AMT) if w in idz]
    TRANSACTION_AMTz[idz[0]]=round(median(MEAN_AMTz))
    LENGTHz[idz[0]]=len(MEAN_AMTz)
    TOTALz[idz[0]]=reduce(lambda x, y: x + y, MEAN_AMTz)
CMTE_IDz=[v for w,v in enumerate(CMTE_ID) if w not in ex_ls] 
ZIP_CODEz=[v for w,v in enumerate(ZIP_CODE) if w not in ex_ls] 
TRANSACTION_AMTz=[v for w,v in enumerate(TRANSACTION_AMTz) if w not in ex_ls] 
LENGTHz=[v for w,v in enumerate(LENGTHz) if w not in ex_ls] 
TOTALz=[v for w,v in enumerate(TOTALz) if w not in ex_ls] 

exd_ls=[]
for idd in d_date:
    exd_ls.extend(idd[1:])
    MEAN_AMTd=[v for w,v in enumerate(TRANSACTION_AMT) if w in idd]
    TRANSACTION_AMTd[idd[0]]=round(median(MEAN_AMTd))
    LENGTHd[idd[0]]=len(MEAN_AMTd)
    TOTALd[idd[0]]=reduce(lambda x, y: x + y, MEAN_AMTd)   
CMTE_IDd=[v for w,v in enumerate(CMTE_ID) if w not in idd[1:]] 
TRANSACTION_DTd=[v for w,v in enumerate(TRANSACTION_DT) if w not in exd_ls] 
TRANSACTION_AMTd=[v for w,v in enumerate(TRANSACTION_AMTd) if w not in exd_ls] 
LENGTHd=[v for w,v in enumerate(LENGTHd) if w not in exd_ls] 
TOTALd=[v for w,v in enumerate(TOTALd) if w not in exd_ls] 

with open(out1File,'w') as proc_zip:
    for a, b,c,d,e in zip(CMTE_IDd,TRANSACTION_DTd,TRANSACTION_AMTd,LENGTHd,TOTALd):
        proc_zip.write("{}|{}|{}|{}|{}\r\n".format(a, b,c,d,e))
with open(out2File,'w') as proc_date:
    for a, b,c,d,e in zip(CMTE_IDz,ZIP_CODEz,TRANSACTION_AMTz,LENGTHz,TOTALz):
        proc_date.write("{}|{}|{}|{}|{}\r\n".format(a, b,c,d,e))






