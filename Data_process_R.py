#-*- coding: utf-8 -*-
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *


def fileInCurrentDir(text):
    path = os.getcwd()
    fileName = os.listdir(path)
    file = []
    for f in fileName:
        if(os.path.splitext(f)[1]==text):
            file.append(f)
    return file

def UFtoES(uf, l, a):
    es = uf.copy()
    es[:,0] = es[:,0]/l
    es[:,1] = es[:,1]/a
    return es

def TRtoER(tr, l):
    er = tr.copy()
    t0 = er[0,0]
    r0 = er[0,1]
    er[:,0] = (er[:,0]-t0)*0.5/l
    er[:,1] = (er[:,1]-r0)/r0
    return er

def linearInterpolation(iniData, toX):
    data = []
    index = 0
    stop = len(iniData)-1
    br = 0
    for x in toX:
        while(x > iniData[index+1][0]):
            index = index + 1
            if index >= stop:
                br = 1
                break
        if br:
            break
        if(iniData[index+1][0]-iniData[index][0] == 0):
            slope = 0
        else:
            slope = (iniData[index+1][1]-iniData[index][1])/(iniData[index+1][0]-iniData[index][0])
        data.append([x, iniData[index][1]+slope*(x-iniData[index][0])])
    return data

def readData(fileName, startrow, encoding='utf-8'):

    with open(fileName, 'r', encoding=encoding) as f:
        file = list(csv.reader(f))
        if not file[-1]:
            file.pop()
    title = file[:startrow]
    data = np.array(file[startrow:]).astype(float)
        
    return title, data


#read data from .csv
files = fileInCurrentDir('.csv')
startrow = 1 #int(input('start row :'))
#startcol = 1 #int(input('start col :'))

title = {}
data = {}
for f in files:
    title[f], data[f] = readData(f, startrow)
    #Plot curves
    L = float(input('Length of '+f+' :'))
##############################################################
    x = np.where(data[f][:,2]>1e37)
    data[f]=np.delete(data[f],x,axis = 0)
    mpl.rcParams['font.sans-serif']=['SimHei']
    plt.plot(data[f][:,0],data[f][:,2])
    plt.title(f)
    plt.show()
    #get input
    t = int(input('Start num of '+f+' :'))
##############################################################
    #calculating ER
    data[f] = data[f][t:,1:]
    data[f] = TRtoER(data[f], L)
#find longgest X coodinate
n = len(files)
for i in range(n):
    for j in range(0,n-1-i):
        if data[files[j]][-1,0] >  data[files[j+1]][-1,0]:
            files[j], files[j+1] = files[j+1], files[j]
#interpolation data
toX = data[files[-1]][:,0]
okData = {}
for i in range(len(files)-1):
    okData[files[i]] = linearInterpolation(data[files[i]], toX)
okData[files[-1]] = data[files[-1]]

#write .csv
for i in files:
    csvfile = open('ok'+i,'w',newline = '')
    writer = csv.writer(csvfile)
    writer.writerow(['strain', 'deltaR/R0'])
    for j in okData[i]:
        writer.writerow(j)
    csvfile.close()

print('complete!')
os.system('pause')

