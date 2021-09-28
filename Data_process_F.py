import os
import csv

def fileInCurrentDir(text):
    path = os.getcwd()
    fileName = os.listdir(path)
    file = []
    for f in fileName:
        if(os.path.splitext(f)[1]==text):
            file.append(f)
    return file

def UFtoES(uf, l, a):
    es = []
    for i in uf:
        es.append([i[0]/l,i[1]/a])
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

def readData(files, startrow, startcol):
    file = {}
    data = {}
    for name in files:
        with open(name, 'r') as f:
            file[name] = list(csv.reader(f))
            if not file[name][-1]:
                file[name].pop()
        data[name] = []
        for i in range(startrow,len(file[name])):
            for j in range(len(file[name][i])):
                file[name][i][j] = float(file[name][i][j])
            data[name].append([file[name][i][startcol],file[name][i][startcol+1]])
    return [file, data]

#read data from .csv
files = fileInCurrentDir('.csv')
startrow = 2 #int(input('start row :'))
startcol = 1 #int(input('start col :'))
[file, data] = readData(files, startrow, startcol)

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
print('complete!')
os.system('pause')

