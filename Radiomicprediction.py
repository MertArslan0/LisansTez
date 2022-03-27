# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 23:08:54 2020

@author: mert
"""

import os
import numpy as np
from radiomics import featureextractor
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn import svm
import xlrd

def pearson_correlation(numbers_x, numbers_y):
    mean_x = numbers_x.mean()
    mean_y = numbers_y.mean()
    subtracted_mean_x = numbers_x - mean_x
    subtracted_mean_y = numbers_y - mean_y
    x_times_y = subtracted_mean_x * subtracted_mean_y
    x_squared = subtracted_mean_x**2
    y_squared = subtracted_mean_y**2
    return x_times_y.sum() / np.sqrt(x_squared.sum() * y_squared.sum())



imageName = []
maskName = []
TumorTypeLabel = []
testnum = 0
trainnum = 0

CurrPath1 = './cytoma/'
FileLst1 = os.listdir(CurrPath1)
for i in range(len(FileLst1)):
    CurFName = FileLst1[i]
    if (CurFName[-7:]=='_T2.nii'):
        imageName.append(CurrPath1 + CurFName)
        SegFName = CurFName[0:-4] + 'Segmentation.nii'
        maskName.append(CurrPath1 + SegFName)
        TumorTypeLabel.append('Oligoastrocytoma')
        trainnum = trainnum + 1
        

CurrPath = './glioma/'
FileLst=os.listdir(CurrPath)

for i in range(len(FileLst)):
    CurFName = FileLst[i]
    if (CurFName[-7:]=='_T2.nii'):
        imageName.append(CurrPath + CurFName)
        SegFName = CurFName[0:-4] + 'Segmentation.nii'
        maskName.append(CurrPath + SegFName)
        TumorTypeLabel.append('Oligodendroglioma')
        trainnum = trainnum + 1
        
        
#getanswerswith exel        
loc = ("C:/Users/yigit/Desktop/TCIA_LGG_cases_159.xlsx") 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
 

listfornames=[]
tumortype = []
 
for i in range(sheet.nrows-1): 
    listfornames.append(sheet.cell_value(i+1, 0)) 
   
for i in range(sheet.nrows-1): 
    tumortype.append(sheet.cell_value(i+1, 3))


tumorimageName = []
tumormaskName = []
imagenametrue = []

CurrPath2 = './test/'
FileLst2 = os.listdir(CurrPath2)
for i in range(len(FileLst2)):
    CurFName = FileLst2[i]
    if (CurFName[-7:]=='_T2.nii'):
        tumorimageName.append(CurrPath2 + CurFName)
        SegFName = CurFName[0:-4] + 'Segmentation.nii'
        tumormaskName.append(CurrPath2 + SegFName)
        testnum = testnum + 1
        
        
for i in range (0,testnum):
    imagenametrue.append(tumorimageName[i][7:-7])

typesoftest =[]

for x in range (0,159):
    if (listfornames[x] in imagenametrue[::]):
        typesoftest.append(tumortype[listfornames.index(listfornames[x])])        
        
        
        
        
extractor = featureextractor.RadiomicsFeaturesExtractor()        
        
print("Calculating features")
for numberofvectors in range(0,trainnum):
    vars()['featureVector%d' % numberofvectors] = extractor.execute(imageName[numberofvectors], maskName[numberofvectors])
    
    
    
for numberofvectors in range(0,testnum):
    vars()['featureVectortest%d' % numberofvectors] = extractor.execute(tumorimageName[numberofvectors], tumormaskName[numberofvectors])



lists = [[] for _ in range(trainnum)]


for x in range (0,trainnum):  
    lists[x] = list(vars()['featureVector%d' % x].values())




for row in range(10): 
    for a in range(0,trainnum):  
        lists[a].pop(0)

for a in range(0,trainnum):
    lists[a].pop(3)
    lists[a].pop(3)
    lists[a].pop(3)
    lists[a].pop(3)
    lists[a].pop(5)
    lists[a].pop(5)
    lists[a].pop(1)
    lists[a].pop(3)    
    lists[a].pop(19)
    lists[a].pop(31)
    lists[a].pop(34)
    lists[a].pop(64)
    lists[a].pop(64)

    
listsnew = [[] for _ in range(105)]    


for x in range(0,trainnum):
    for y in range(0,105):
        listsnew[y].append(lists[x][y])
    
image = np.zeros([105,105])    


for x in range(0,105):
    for y in range(0,105):    
        image[x,y] =  pearson_correlation(np.asarray(listsnew[x]),np.asarray(listsnew[y]))  


plt.imshow(image)
plt.colorbar()



#getnamesforpearson

namelist = []



for key in featureVector1:
    namelist.append(key)
    
    
 
for row in range(10):
       
    namelist.pop(0)

namelist.pop(3)
namelist.pop(3)
namelist.pop(3)    
namelist.pop(3)
namelist.pop(5)    
namelist.pop(5)    
namelist.pop(1) 
namelist.pop(3)   
namelist.pop(19) 
namelist.pop(31)
namelist.pop(34) 
namelist.pop(64)    
namelist.pop(64)    
    






Data2 = {}

for y in range(0,105):
    Data2.update({namelist[y]:listsnew[y]})

 
df2 = DataFrame(Data2)

df1 = DataFrame(Data2)


    
    

df2.insert(loc=0,column='type',value=TumorTypeLabel)



matrixdf = df1.as_matrix()
type_label = np.where(df2['type']=='Oligoastrocytoma', 0, 1)







model = svm.SVC(kernel ='rbf',C=1000,gamma =1)

model.fit(matrixdf, type_label)



listsfortest = [[] for _ in range(testnum)]

 


for x in range (0,testnum):  
    listsfortest[x] = list(vars()['featureVectortest%d' % x].values())




for row in range(10):
    for a in range(0,testnum):
        listsfortest[a].pop(0)
           
for a in range(0,testnum):
    listsfortest[a].pop(3)
    listsfortest[a].pop(3)
    listsfortest[a].pop(3)
    listsfortest[a].pop(3)
    listsfortest[a].pop(5)
    listsfortest[a].pop(5)
    listsfortest[a].pop(1)
    listsfortest[a].pop(3)
    listsfortest[a].pop(19)   
    listsfortest[a].pop(31)
    listsfortest[a].pop(34)
    listsfortest[a].pop(64)
    listsfortest[a].pop(64)


for x in range (0,testnum):
    vars()['test%d' % x] = listsfortest[x]



result = []


for test in range(0,testnum):
    if(model.predict([vars()['test%d' % test]]))==0:
        result.append('Oligoastrocytoma')        
    else:
        result.append('Oligodendroglioma')
        


percent=[]
a = 0
for x in range (0,testnum): 
    if(typesoftest[x] ==result[x]):
        a = a +1
    
percentresult = (a / testnum)*100

print('result is','%',percentresult)