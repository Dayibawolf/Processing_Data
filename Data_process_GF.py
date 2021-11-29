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

GF = {}
modulus = {}
for fileName in files:
    title, data = readData(fileName, startrow)
    #Plot curves
    L = float(input('Length of '+fileName+' :'))
##############################################################
    for i in range(len(data)-1,0,-1):
        if(data[i][2]<1e37):
            data = data[:i]
            break
    mpl.rcParams['font.sans-serif']=['SimHei']
    plt.plot(data[:,1],data[:,2])
    plt.title(fileName)
    plt.show()
    #get input
    t = float(input('Start time of '+fileName+' :'))
##############################################################
    #calculating GF
    R = linearInterpolation(data[:,1:], [t,t+L,t+L/0.5])
    GF50 = (R[1][1]-R[0][1])/R[0][1]/0.5
    GF100 = (R[2][1]-R[0][1])/R[0][1]
    #calculating modulus
    GF[fileName] = [GF50, GF100]

print('Results is writen to GF.txt')
with open('GF.txt', 'w') as f:
    for fileName in files:
        f.write(fileName+'\nGF50: '+ str(GF[fileName][0])+'\nGF100: '+str(GF[fileName][1])+'\n')

'''
#calculating strain and stress
L = {}
for i in files:
    L[i] = float(input('Length of '+i+' :'))
    data[i] = UFtoES(data[i], L[i], 0.01)

#find longgest X coodinate
n = len(files)
for i in range(n):
    for j in range(0,n-1-i):
        if data[files[j]][-1][0] >  data[files[j+1]][-1][0]:
            files[j], files[j+1] = files[j+1], files[j]

#interpolation data
toX = [x[0] for x in data[files[-1]]]
okData = {}
for i in range(len(files)-1):
    okData[files[i]] = linearInterpolation(data[files[i]], toX)
okData[files[-1]] = data[files[-1]]

#write .csv
for i in files:
    csvfile = open('ok'+i,'w',newline = '')
    writer = csv.writer(csvfile)
    writer.writerow(['strain', 'stress(kPa)'])
    for j in okData[i]:
        writer.writerow(j)
    csvfile.close()
'''
print('complete!')
os.system('pause')

