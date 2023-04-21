import random
import math
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import xlwt
import os
from xlutils.copy import copy

def readRSTWeightwithNoisefromExcel (pathOfNoiseWeightMat):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfNoiseWeightMat)
    table = readbook.sheets()[0]
    noiseWeighMat = np.zeros((1000, 16))
    meanValue = 0.461066
    for i in range (0,16):
        for j in range (0,999):
            noiseWeighMat[j][i] = (table.cell(j,i).value - meanValue)#/meanValue
    return noiseWeighMat

def readRSTConductancewithNoisefromExcel (pathOfNoiseWeightMat):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfNoiseWeightMat)
    table = readbook.sheets()[0]
    noiseWeighMat = np.zeros((1000, 16))
    for i in range (0,16):
        for j in range (0,999):
            noiseWeighMat[j][i] = table.cell(j,i).value
    return noiseWeighMat


def readWeightwithNoisefromExcel (pathOfNoiseWeightMat):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfNoiseWeightMat)
    table = readbook.sheets()[0]
    noiseWeighMat = np.zeros((1600, 24))
    for i in range (0,24):
        meanValue = table.cell(1, i).value
        #print(meanValue)
        for j in range (2,1602):
            noiseWeighMat[j-2][i] = (table.cell(j,i).value - meanValue)/meanValue
    return noiseWeighMat

def readConductancewithNoisefromExcel (pathOfNoiseWeightMat):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfNoiseWeightMat)
    table = readbook.sheets()[0]
    noiseWeighMat = np.zeros((1600, 24))
    for i in range (0,24):
        meanValue = table.cell(1, i).value
        #print(meanValue)
        for j in range (2,1602):
            noiseWeighMat[j-2][i] = table.cell(j,i).value
    return noiseWeighMat

def readMinTestfromExcel (pathOfminTest,n):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfminTest)
    table = readbook.sheets()[0]
    minTest = np.zeros(n)
    for i in range (0,n):
            minTest[i] = table.cell(i+2,0).value
    return minTest

#plot energy trace to excel
def SaveEnergy (savePath, Energy, dataType, step):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('dataType')
    for i in range(step):
        sheet.write(i,dataType,Energy[i])
    workbook.save(savePath)

#plot success percent to excel
def SaveResultnew (savePath, Energy, dataType, step,poss):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet1')
    for j in range(dataType):
        sheet.write(0, j, poss[j])
        for i in range(step):
            sheet.write(i+1,j,Energy[i,j])
    workbook.save(savePath)

def SaveResult (savePath, Energy, dataType, step,poss):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('sheet1')
    sheet.write(0, dataType, poss)
    for i in range(step):
            sheet.write(i+1,dataType,Energy[i])
    workbook.save(savePath)

#creat a test sample
def getSample ( n , d):
    # d for edge density 0<d<1
    totalNode = (1+n)*n/2
    edge = d * (1+n)*n/2
    #print(edge)
    testArray = np.zeros(int(totalNode))
    i = 0
    while i < int(edge):
        x = random.randint(0,totalNode-1)
        if testArray[x] != -1:
            testArray[x] = -1
            i += 1

    weightMat = np.zeros((n, n))
    x = 0
    for i in range(n - 1):
        for j in range(i):
            weightMat[i][j] = testArray[x]
            weightMat[j][i] = weightMat[i][j]
            x += 1
            #print(x)
    return weightMat

#save weightmat to excel
def saveSample (n,weightMat,path):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet1')
    for i in range(n):
         for j in range (n):
               worksheet.write(i,j,weightMat[i][j])
    workbook.save(path)
def saveTest (n,Test,path):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet1')
    for i in range(n):
               worksheet.write(i,0,Test[i])
    workbook.save(path)


def saveTest_mul(n, Test, path, maxCut, updatecount):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet1')
    worksheet.write(0, 0, maxCut)
    worksheet.write(1, 0, updatecount)
    for i in range(n):
        worksheet.write(i+2, 0, Test[i])
    workbook.save(path)

def saveWrongRate(n, path, wrongRate):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('sheet1')
    for i in range(n):
        worksheet.write(i, 0, wrongRate[i])
    workbook.save(path)

def readWeightfromExcelofMine(path , n):
    readbook = xlrd.open_workbook(path)
    table = readbook.sheets()[0]
    array = np.zeros((n,n))
    for i in range (n):
        for j in range (n):
            array[i][j]=table.cell(i,j).value
    return array

def verifySample (test,edge):
    sum = 0
    result = 'Same'
    for i in range (len(test)):
        if test[i-1] == 1:
            sum += 1
    if sum != edge:
        result = 'Different'
    print (result)

def readWeightfromExcel (pathOfExcel,s,e):
    #s for size of node
    #e for number of edge
    readbook = xlrd.open_workbook(pathOfExcel)
    table = readbook.sheets()[0]
    array = 1 * np.zeros((s,s))

    for i in range(s):
        for j in range(s):
            if i == j:
                array[i][j] = 0

    for i in range(2,e):
        array_x = table.cell(i,0).value
        array_y = table.cell(i,1).value

        array[int(array_x)-1][int(array_y)-1] = -1 # table.cell(i,2).value
        array[int(array_y)-1][int(array_x)-1] = array[int(array_x)-1][int(array_y)-1]

    return array

def calcWeight(savedsample):
    N = len(savedsample)
    #print (N)
    #P = len(savedsample)
    mat = [0]*N
    returnMat = []
    for i in range(N):
        m = mat[:]
        returnMat.append(m)
    for i in range(N):
        for j in range(N):
            if i==j:
                continue
            sum = 0
            sum += savedsample[i]*savedsample[j]
           # for u in range(P):
           #     sum += savedsample[u][i] * savedsample[u][j]
            returnMat[i][j] = sum/float(N)
    return returnMat

def calcEnergy(inMat , weighMat):
    matEnergy = 0
    for j in range(len(inMat)):
        for i in range(j):
            matEnergy += -1/2 * weighMat[i][j] * inMat[i] * inMat[j]
            #print (weighMat[i][j],inMat[i],inMat[j])
    return matEnergy

def calcMaxcut(inMat , weightMat , s):
    matEnergy = 0
    maxCut = 0
    weightEnergy = 0
    for j in range(len(inMat)):
        for i in range(j):
            matEnergy += -1/2 * weightMat[i][j] * inMat[i] * inMat[j]
    #print (matEnergy)
    for j in range(len(inMat)):
        for i in range(j):
            weightEnergy += -1/2 * weightMat[i][j]
    #print (weightEnergy)
    maxCut = weightEnergy-matEnergy
    #maxCut = s * maxCut
    return maxCut

def calcXi(inMat , weighMat):
    returnMat = inMat
    choose = []
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithRand(inMat , weighMat  , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
            sum *= random.randint(-1,9)
            #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseDecaySublinear(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            decayRate = 10*noiseLevel*(interation+1)**1/2 / ((maxInteration+1) ** 1/2)
            r = random.randint(-noiseLevel ,100-noiseLevel)+ decayRate +0.00001   # 0.00001 for in case division by zero
            r = r / abs(r)
            sum += weighMat[i][j] * inMat[j] * r
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseDecaySuperlinear(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    noiseData = [maxInteration]
    for i in range(len(inMat)/4): #(len(inMat)//64):
        #随机改变N/4个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
        #print(sum)
        decayRate = (0.3 - 0.3 * (interation ** 3) / (maxInteration ** 3))*noiseLevel
        sum = random.normalvariate(sum, decayRate)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseDecaylinearly(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(1): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
        y =  1-interation/100 #change possibility of linearly
        r = random.random()
        if r  < y:
            sum *= -1
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseInmat(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            decayRate = (interation+1)**2 / ((maxInteration+1) ** 2) #sublinear
            r = (random.random()-0.5)/50 * noiseLevel / decayRate
            #print(r)
            sum += weighMat[i][j] * (inMat[j] + r)
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseofPaper(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            r = random.randint(-1 , 9) + ((10.0001-noiseLevel)/10) #intrinsic noiselevel = 0 cant change ;nosielevel = 10 10%change
            #if r / abs(r) == -1
            #    print ("change")
            sum += (weighMat[i][j] * r / abs(r)) * inMat[j]
        wt = -4.5 + 5.9/maxInteration * i
        y = - inMat[i] * wt
        #print(sum)
        if sum >= y:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseInmatV2(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            if (interation+1)**2 / ((maxInteration+1) ** 2) <= 0.125:
                decayRate = 1
            elif  0.125 < (interation+1)**2 / ((maxInteration+1) ** 2) <= 0.25 :
                decayRate = 0.4
            elif 0.25 < (interation + 1) ** 2 / ((maxInteration + 1) ** 2) <= 0.375:
                decayRate = 0.3
            elif 0.375 < (interation + 1) ** 2 / ((maxInteration + 1) ** 2) <= 0.5:
                decayRate = 0.2
            elif 0.5 < (interation + 1) ** 2 / ((maxInteration + 1) ** 2) <= 0.625:
                decayRate = 0.1
            elif 0.75 < (interation + 1) ** 2 / ((maxInteration + 1) ** 2) <= 0.875:
                decayRate = 0.01
            else:
                decayRate = 0

            r = (random.random()-0.5)/50 * noiseLevel * decayRate
            sum += weighMat[i][j] * (inMat[j] + r)
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseInmatV3(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(5): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            if (interation+1)**3 / ((maxInteration+1) ** 3) < 0.05/0.35:
                decayRate = 0.35
            elif  0.05/0.35 <= (interation+1)**3 / ((maxInteration+1) ** 3) < 0.1/0.35 :
                decayRate = 0.3
            elif 0.25/0.35 <= (interation + 1) ** 3 / ((maxInteration + 1) ** 3) < 0.2/0.35:
                decayRate = 0.2
            elif 0.2/0.35 <= (interation + 1) ** 3 / ((maxInteration + 1) ** 3) < 0.15/0.35:
                decayRate = 0.15
            elif 0.15/0.35 <= (interation + 1) ** 3 / ((maxInteration + 1) ** 3) < 0.1/0.35:
                decayRate = 0.1
            elif 0.1/0.35 <= (interation + 1) ** 3 / ((maxInteration + 1) ** 3) < 0.05/0.35:
                decayRate = 0.05
            else:
                decayRate = 0.17

            Noise = random.normalvariate(weighMat[i][j],decayRate*noiseLevel/5)
            sum +=  Noise * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithsimulateAnnealing(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            Noise = random.normalvariate(weighMat[i][j], (-0.43095*(interation/maxInteration)+0.43095))  #
            #Noise = random.normalvariate(weighMat[i][j], (0.3300))  #
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithfixednoise(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    deviation = [0.01731,0.01838,0.02308,0.03246,0.04522,0.05868,0.07594,0.0849,0.08506,0.09038,0.09046,0.0913,0.09571,0.09453,
                 0.09678,0.10737,0.11976,0.13679,0.15162,0.1664,0.18365,0.19442,0.20069,0.21528,0.22112,0.22447]
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            if weighMat[i][j] == -1:
                Noise = random.normalvariate(weighMat[i][j], 0.0000000001)  #
            else:
                Noise = random.normalvariate(weighMat[i][j], 0.22)
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithchangenoise(inMat , weighMat , interation , noiseLevel , maxInteration, leveltrace):
    returnMat = inMat
    choose = []
    level = interation / maxInteration
    NoiseLevel = 25-25*level**(0.6)
    #level = interation + 1
    #NoiseLevel = 25 / level ** (0.2 * noiseLevel)
    deviation = [0.09829,0.18016,0.19228,0.23034,0.24954,0.25356,0.25412,0.2641,0.2651,0.27679,0.29299,0.29494,0.30143,0.3026,0.30917,
                 0.32234,0.3266,0.3271,0.33813,0.33976,0.33992,0.34306,0.35109,0.39207,0.39563,0.42292,0.43095]
    leveltrace.append(deviation[int(NoiseLevel)])
    #deviation = [0.01731,0.01838,0.02308,0.03246,0.04522,0.05868,0.07594,0.0849,0.08506,0.09038,0.09046,0.0913,0.09571,0.09453,
    #             0.09678,0.10737,0.11976,0.13679,0.15162,0.1664,0.18365,0.19442,0.20069,0.21528,0.22112,0.22447]
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            if (weighMat[i][j] == -1):
                Noise = random.normalvariate(-1, deviation[int(NoiseLevel)])  #
            #Noise = random.normalvariate(weighMat[i][j], deviation[25-int(25*interation/maxInteration)])
            else :
                Noise = weighMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithNoiseBest(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    level = interation / maxInteration
    NoiseLevel = 25-25*level**(0.8)
    #level = interation + 1
    #NoiseLevel = 25 / level ** (0.2 * noiseLevel)
    #deviation = [0.18016,0.19228,0.23034,0.24954,0.25356,0.25412,0.2641,0.2651,0.27679,0.29299,0.29494,0.30143,0.3026,0.30917,
    #             0.32234,0.3266,0.3271,0.33813,0.33976,0.33992,0.34306,0.35109,0.39207,0.39563,0.42292,0.43095]
    deviation = [0.01731,0.01838,0.02308,0.03246,0.04522,0.05868,0.07594,0.0849,0.08506,0.09038,0.09046,0.0913,0.09571,0.09453,
                 0.09678,0.10737,0.11976,0.13679,0.15162,0.1664,0.18365,0.19442,0.20069,0.21528,0.22112,0.22447]
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
           # if (weighMat[i][j] == -1):
                #Noise = random.normalvariate(-1, deviation[int(NoiseLevel)])  #
            Noise = random.normalvariate(weighMat[i][j], deviation[25-int(25*interation/maxInteration)])
            #else :
            #    Noise = weighMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithexperimentnoise(inMat , weighMat , interation , noiseLevel , maxInteration,noiseWeightMat):
    returnMat = inMat
    choose = []
    level = interation / maxInteration
    level = 25-25*level**(-1*noiseLevel)
    #print(noiseWeighMat[0][0])
    #for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
    #    choose.append(random.randint(0,len(inMat)-1))
    for i in range(len(inMat)):
        sum = 0
        for j in range(len(inMat)):
            if (weightMat[i][j] == -1):
                Noise = -1 + noiseWeightMat[random.randint(0,1599),int(level)]
                #print(noiseWeightMat[interation+2,25])
            else:
                Noise = weightMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithchangenoiseV2(inMat , weighMat , interation , noiseLevel , maxInteration):
    returnMat = inMat
    choose = []
    ReadDeviation = [0.054738]
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
        choose.append(i)
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            #if (weighMat[i][j] == -1):
            #    Noise = random.normalvariate(-1, ReadDeviation[0])  #
            Noise = random.normalvariate(weighMat[i][j], ReadDeviation[0])
            #else :
            #    Noise = weighMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

def calcXiwithchangenoiseV3(inMat , weighMat , interation , noiseLevel , maxInteration, currentState):
    returnMat = inMat
    choose = []
    ReadDeviation = [0.054738]
    #print(HighLimit,currentState)
    for i in range(currentState): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,currentState))
    for i in range(currentState):
        sum = 0
        for j in range(len(inMat)):
            #if (weighMat[i][j] == -1):
            #    Noise = random.normalvariate(-1, ReadDeviation[0])  #
            Noise = random.normalvariate(weighMat[i][j], ReadDeviation[0])
            #else :
            #    Noise = weighMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat
def calcXiwithexperimentnoiseV2(inMat , weighMat , interation , noiseLevel , maxInteration, wrongRate):
    returnMat = inMat
    wrongCounter = 0
    choose = []
    ReadDeviation = [0.0054738]
    for i in range(len(inMat)): #(len(inMat)//64):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in range(len(inMat)):
        sum = 0
        for j in range(len(inMat)):
            #if (weighMat[i][j] == -1):
            #    Noise = random.normalvariate(-1, ReadDeviation[0])  #
            Noise = random.normalvariate(weighMat[i][j], ReadDeviation[0])
            #else :
            #    Noise = weighMat[i][j]
            sum += Noise * inMat[j]
            #sum += weighMat[i][j] * inMat[j]
        #print(sum)
        if sum>=0:
            returnMat[i] = 1
        else:
            returnMat[i] = -1
        #if sum < 0:
        #    print(i)
        if sum != 0 and i == 49:
            wrongCounter = sum
            wrongRate.append(wrongCounter)
        if wrongCounter >= 1000:
            print(idealSum,sum)
    return returnMat
'''
sample =  [1,-1,-1,-1,1,-1,-1,1,
           1,1,-1,-1,1,-1,-1,1,
           1,-1,1,-1,1,-1,-1,1,
           1,-1,-1,1,1,-1,-1,1,
            1,1,-1,-1,1,-1,-1,1,
            1,-1,1,-1,1,-1,-1,1,
            1,-1,-1,1,1,-1,-1,1,
           1,-1,-1,-1,1,-1,-1,1]
'''

def addnoise(mytest_data,n):
    noise_data = [1]*n*n
    for x in range(n):
        for y in range(n):
            if random.randint(0, 10) > 5:
                noise_data[x * n + y] = -mytest_data[x * n + y]
    return noise_data

def initialSample(mytest_data,n):
    for x in range(n):
        for y in range(n):
            if random.randint(0, 10) > 7:
                mytest_data[x * n + y] = -mytest_data[x * n + y]

def regularout(data,N):
    for j in range(N):
        ch = ""
        for i in range(N):
            ch += " " if data[j*N+i] == -1 else "X"
        print (ch)

def arrayCom (initArray,testArray):
    B = "True"
    for i in range(len(initArray)):
        if initArray[i] == testArray[i]:
            #print(initArray[i],testArray[i])
            continue
        else:
            B = "False"
            break
    print(B)

'''
sample = -np.ones(81)
initialSample(sample,9)
#print(sample)

weightMat =  calcWeight(sample)
#regularout(sample[0],5)

E1 = calcEnergy(sample,weightMat)
print  (E1)
'''



'''
test = addnoise(sample,8)
test = -np.ones(81)
#regularout(test,5)
#arrayCom(sample,test)
E2 = calcEnergy(test,weightMat)
print(E2)
'''
def HNNtestBlock(interation,test,weightMat,s, savePath):
    Energy = np.zeros(interation)
    for i in range(interation):
        test = calcXi(test,weightMat)
        #test = calcXiwithRand(test,weightMat)
        Energy[i] = calcEnergy(test,weightMat)
    maxCut = calcMaxcut(test,weightMat,s)
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    if saveEnergyValid:
        SaveEnergy(EnergySavePath,Energy,0,interation)
    if printPlot == 1:
        plt.plot(Energy)
        plt.show()
    return maxCut

def HNNtestBlockwithAnnealing_before(interation, test, weightMat, n , noiseLevel , noiseType ):
    Energy = np.zeros(interation)
    noiseData = np.zeros(interation)
    min_energy = 100000
    delta_e = 0
    test_new = test
    rdint = 0
    choose = []
    for i in range(interation):
        #test = calcXi(test,weightMat)
        test_new = calcXiwithsimulateAnnealing(test, weightMat,  i , noiseLevel , interation)
        #decayRate = (0.3 - 0.3 * (i ** 5) / (interation ** 5)) / 10
        #noiseData[i] = decayRate
        Energy[i] = calcEnergy(test_new,weightMat)
        delta_e = Energy[i] - min_energy
        if delta_e < 0:
            min_energy = Energy[i]
            test = test_new
        else:
            for j in range(len(test_new)):  # (len(inMat)//64):
                # 随机改变5个神经元的值，该参数可调，也可同时改变所有神经元的值
                choose.append(random.randint(0, len(test_new) - 1))
            for j in choose:
                rdint = random.random() - 0.0001
                if (rdint) < 0 :
                    #print(rdint,i)
                    test_new[j] *= -1
            test_new = calcXiwithsimulateAnnealing(test_new, weightMat, i, noiseLevel, interation)
            Energy[i] = calcEnergy(test_new, weightMat)
            delta_e = Energy[i] - min_energy
            p = math.exp(-delta_e / (noiseLevel))
            #print(p)
            r = np.random.uniform(low = 0,high = 1)
            if r < p:
                test = test_new
        #print(Energy[i],i)
    maxCut = calcMaxcut(test, weightMat, n)
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if printPlot == 1:
        plt.plot(Energy)
        plt.show()
    return maxCut

def HNNtestBlockwithAnnealing(interation, test, weightMat, n , noiseLevel , noiseType ):
    Energy = np.zeros(interation)
    minEnergy = 0
    mintest = np.ones(n)
    for i in range(interation):
        test = calcXiwithsimulateAnnealing(test, weightMat, i, noiseLevel, interation)
        Energy[i] = calcEnergy(test, weightMat)
        if Energy[i] < minEnergy:
            mintest = test.copy()
            minEnergy = Energy[i]
            maxCut = calcMaxcut(mintest, weightMat, n)
    maxCut = calcMaxcut(mintest, weightMat, n)
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(EnergySavePath, Energy, 0, interation)
    if printPlot == 1:
        plt.plot(Energy)
        plt.show()
    return maxCut

def HNNtestBlockwithNoiseDecay(interation, test, weightMat, n , nosieLevel , noiseType , printPlot, savePath):
    Energy = np.zeros(interation)
    leveltrace = []
    updatetrace = []
    updatetracey = []
    updatetraceDeviation = []
    CurrentLeveltrace = []
    HighLimitTrace = []
    backtrace = []
    backtracey = []
    minEnergy = 0
    mintest = np.ones(n)
    minIteration = 0
    optimalNoiseLevel = 22
    UpdateCount = 0
    maxCut = 0
    Back = 0
    if noiseType == 0:
        for i in range(interation):
            test = calcXi(test,weightMat)
            Energy[i] = calcEnergy(test,weightMat)
    elif noiseType == 1:
        for i in range(interation):
            test = calcXiwithRand(test,weightMat, i , nosieLevel , interation)
            Energy[i] = calcEnergy(test,weightMat)
    elif noiseType == 2:
        for i in range(interation):
            test = calcXiwithNoiseDecaySublinear(test,weightMat,  i , nosieLevel , interation)
            Energy[i] = calcEnergy(test,weightMat)
    elif noiseType == 3:
        for i in range(interation):
            test = calcXiwithNoiseDecaySuperlinear(test,weightMat,  i , nosieLevel , interation)
            Energy[i] = calcEnergy(test,weightMat)
    elif noiseType == 4:
        for i in range(interation):
             test = calcXiwithNoiseInmat(test,weightMat,  i , nosieLevel , interation)
             Energy[i] = calcEnergy(test, weightMat)
    elif noiseType == 5:
        for i in range(interation):
            test = calcXiwithNoiseofPaper(test,weightMat,  i , nosieLevel , interation)
            Energy[i] = calcEnergy(test, weightMat)
            #print(Energy[i],i)
    elif noiseType == 6:
        for i in range(interation):
            test = calcXiwithNoiseInmatV2(test, weightMat, i, nosieLevel, interation)
            Energy[i] = calcEnergy(test, weightMat)
            # print(Energy[i],i)
    elif noiseType == 7:
        for i in range(interation):
            test = calcXiwithNoiseInmatV3(test, weightMat, i, nosieLevel, interation)
            Energy[i] = calcEnergy(test, weightMat)
    elif noiseType == 8:
        deviation = [0.09829, 0.18016, 0.19228, 0.23034, 0.24954, 0.25356, 0.25412, 0.2641, 0.2651, 0.27679, 0.29299,
                     0.29494, 0.30143, 0.3026, 0.30917,
                     0.32234, 0.3266, 0.3271, 0.33813, 0.33976, 0.33992, 0.34306, 0.35109, 0.39207, 0.39563, 0.42292,
                     0.43095]
        for i in range(interation):
            noise = 0
            test = calcXiwithchangenoise(test, weightMat, i, nosieLevel, interation,leveltrace)
            Energy[i] = calcEnergy(test, weightMat)
    elif noiseType == 9:
        for i in range(interation):
            test = calcXiwithfixednoise(test, weightMat, i, nosieLevel, interation)
            Energy[i] = calcEnergy(test, weightMat)
            if Energy[i] < minEnergy:
                mintest = test.copy()
                minEnergy = Energy[i]
        # print(Energy[i],i)
    elif noiseType == 10:
        currentNoiseLevel = 23
        optimalNoiseLevel = currentNoiseLevel
        NeedUpdate = 0
        Type1Count = 0
        Type2Count = 0
        Type3Count = 0
        '''
        DeviceDeviation = [0.098,0.18016, 0.19228, 0.23034, 0.24954, 0.25356, 0.25412, 0.2641, 0.2651, 0.27679, 0.29299,
                           0.29494, 0.30143, 0.3026, 0.30917,
                           0.32234, 0.3266, 0.3271, 0.33813, 0.33976, 0.33992, 0.34306, 0.35109, 0.39207, 0.39563,
                           0.42292, 0.43095]
        '''
        DeviceDeviation = [0.102,0.18016, 0.19228, 0.23034, 0.24954, 0.25356, 0.25412, 0.2641, 0.2651, 0.27679, 0.29299,
                           0.29494, 0.3026, 0.3026, 0.32709, 0.32709, 0.32709, 0.32709, 0.33202, 0.33366, 0.34306, 0.35109, 0.39207, 0.43095]
        DeviceConductance = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                           9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393] #to modulate the 0 weights
        PCMweightMat = np.zeros((n, n))
        matrixcount = 0
        for i in range(interation):
            #print(i,maxCut)
            level = i / interation
            choose = []
            LevelSet = [23,1,0]
            Step = 5
            #NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
            NoiseLevel = 23 - 23 * level
            '''
            if(NoiseLevel <= (optimalNoiseLevel-Step)):
                optimalNoiseLevel = optimalNoiseLevel-Step
                Step += 1
            if optimalNoiseLevel <= Step :
                optimalNoiseLevel = 0
            #leveltrace.append(DeviceDeviation[int(optimalNoiseLevel)])
            '''
            if level <= 0.25:
                optimalNoiseLevel = LevelSet[0]
            elif level <= 0.4:
                optimalNoiseLevel = LevelSet[2]
            else:
                optimalNoiseLevel = LevelSet[2]

            seletLevel = optimalNoiseLevel
            #seletLevel = currentNoiseLevel
            leveltrace.append(DeviceDeviation[int(seletLevel)])
            CurrentLeveltrace.append(NoiseLevel)
            #leveltrace.append(int(NoiseLevel))
            if NoiseLevel <= currentNoiseLevel :
            #if NeedUpdate == 1  or i == 0:
                #onecount = 0
                #zerocount = 0
                #matrixcount += 1
                for ii in range(n):
                    for jj in range(ii):
                        if(weightMat[ii][jj] == -1):
                            PCMweightMat[ii][jj] = random.normalvariate(weightMat[ii][jj], DeviceDeviation[int(seletLevel)])
                            #PCMweightMat[ii][jj] = weightMat[ii][jj]
                            PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                            #onecount += 1
                            #print(PCMweightMat[i][j])
                        else:
                            PCMweightMat[ii][jj] = random.normalvariate(0.461006/DeviceConductance[int(seletLevel)], 0.22) #0.461006 is the meanvalue of rst conductance
                            #PCMweightMat[ii][jj] = random.normalvariate(0, 0.22)+ 1/DeviceConductance[int(seletLevel)]
                            PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                            #zerocount += 1

                '''
                if (currentNoiseLevel <= 1):
                    currentNoiseLevel -= 1
                    UpdateCount += 1
                    updatetrace.append(i)
                else:
                    currentNoiseLevel -= 0.5
                    UpdateCount += 1
                    updatetrace.append(i)
                
                if (currentNoiseLevel > 10):
                    currentNoiseLevel -= 0.45
                    UpdateCount += 1
                    updatetrace.append(i)
                else:
                    currentNoiseLevel -= 1
                    UpdateCount += 1
                    updatetrace.append(i)
                
                #step type 1
                #print(PCMweightMat)
                currentNoiseLevel -= 0.35
                UpdateCount += 1
                updatetrace.append(i)
                '''
                if (level <= 0.5):
                    currentNoiseLevel -= 0.6 #0.4
                    UpdateCount += 1
                    updatetrace.append(i)
                else:
                    currentNoiseLevel -= 0.5 #0.3
                    UpdateCount += 1
                    updatetrace.append(i)

                #updatetracey.append(DeviceDeviation[int(seletLevel)])

            if saveWeightMatrix and (i == 1 or i == 999):
                PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-HNN-Node' + str(
                currentNoiseLevel) + '-' + '-WeightMatrix.xls'
                saveSample(n,PCMweightMat,PCMweightMatpath)
            #print('one',onecount,'zero',zerocount,'matrixcount',matrixcount)
            #HighLimit = int(len(test) * (1 - level**20) - 1)
            if i < 499:
                HighLimit = len(test)
            else:
                HighLimit = len(test)
            HighLimitTrace.append(HighLimit)
            test = calcXiwithchangenoiseV3(test, PCMweightMat, i, nosieLevel, interation, HighLimit)
            Energy[i] = calcEnergy(test, weightMat)
            if len(updatetracey) < len(updatetrace):
                updatetracey.append(Energy[i])
                updatetraceDeviation.append(DeviceDeviation[int(seletLevel)])
            if Energy[i] < minEnergy:
                mintest = test.copy()
                minEnergy = Energy[i]
                maxCut = calcMaxcut(mintest, weightMat, n)
                minIteration = i
                NeedUpdate = 0
                Type1Count += 1
            elif (Energy[i] == Energy[i-1] and Energy[i-1] == Energy[i-2]):
                NeedUpdate = 1
                Type2Count += 1
            else:
                NeedUpdate = 0
                Type3Count += 1

    elif noiseType == 11:
        currentNoiseLevel = 23
        optimalNoiseLevel = currentNoiseLevel
        NeedUpdate = 1
        Type1Count = 0
        Type2Count = 0
        Type3Count = 0
        '''
        DeviceDeviation = [0.098,0.18016, 0.19228, 0.23034, 0.24954, 0.25356, 0.25412, 0.2641, 0.2651, 0.27679, 0.29299,
                           0.29494, 0.30143, 0.3026, 0.30917,
                           0.32234, 0.3266, 0.3271, 0.33813, 0.33976, 0.33992, 0.34306, 0.35109, 0.39207, 0.39563,
                           0.42292, 0.43095]
        '''
        DeviceDeviation = [0.102, 0.18016, 0.19228, 0.23034, 0.24954, 0.25356, 0.25412, 0.2641, 0.2651, 0.27679,
                           0.29299,
                           0.29494, 0.3026, 0.3026, 0.32709, 0.32709, 0.32709, 0.32709, 0.33202, 0.33366, 0.34306,
                           0.35109, 0.39207, 0.43095]
        DeviceConductance = [27.9769, 10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112,
                             9.02729,
                             9.02729, 3.34815, 3.34815, 2.32458, 2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923,
                             7.76347, 6.68116, 4.76393]  # to modulate the 0 weights
        PCMweightMat = np.zeros((n, n))
        matrixcount = 0
        for i in range(interation):
            print(i, maxCut)
            level = i / interation
            choose = []
            LevelSet = [23, 1, 0]
            Step = 5
            # NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
            NoiseLevel = 23 - 23 * level
            '''
            if(NoiseLevel <= (optimalNoiseLevel-Step)):
                optimalNoiseLevel = optimalNoiseLevel-Step
                Step += 1
            if optimalNoiseLevel <= Step :
                optimalNoiseLevel = 0
            #leveltrace.append(DeviceDeviation[int(optimalNoiseLevel)])
            '''
            if level <= 0.25:
                optimalNoiseLevel = LevelSet[2]
            elif level <= 0.4:
                optimalNoiseLevel = LevelSet[2]
            else:
                optimalNoiseLevel = LevelSet[2]

            seletLevel = optimalNoiseLevel
            leveltrace.append(DeviceDeviation[int(seletLevel)])
            CurrentLeveltrace.append(NoiseLevel)
            # leveltrace.append(int(NoiseLevel))
            # if NoiseLevel <= currentNoiseLevel :
            if NeedUpdate == 1 or Back == 1:
                if NeedUpdate == 1:
                    optimalNoiseLevel = LevelSet[0]
                    updatetrace.append(i-1)
                    updatetracey.append(Energy[i - 1])
                else:
                    optimalNoiseLevel = LevelSet[2]
                    backtrace.append(i-1)
                    backtracey.append(Energy[i - 1])
                for ii in range(n):
                    for jj in range(ii):
                        if (weightMat[ii][jj] == -1):
                            PCMweightMat[ii][jj] = random.normalvariate(weightMat[ii][jj],DeviceDeviation[int(seletLevel)])
                            # PCMweightMat[ii][jj] = weightMat[ii][jj]
                            PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                            # onecount += 1
                            # print(PCMweightMat[i][j])
                        else:
                            # PCMweightMat[ii][jj] = random.normalvariate(1/DeviceConductance[int(seletLevel)], 0.22)
                            PCMweightMat[ii][jj] = random.normalvariate(0, 0.22) / DeviceConductance[int(seletLevel)]
                            PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                            # zerocount += 1

                # updatetracey.append(DeviceDeviation[int(seletLevel)])

            if saveWeightMatrix and (i == 1 or i == 999):
                PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-HNN-Node' + str(
                    currentNoiseLevel) + '-' + '-WeightMatrix.xls'
                saveSample(n, PCMweightMat, PCMweightMatpath)
            # print('one',onecount,'zero',zerocount,'matrixcount',matrixcount)
            # HighLimit = int(len(test) * (1 - level**20) - 1)

            test = calcXiwithchangenoiseV3(test, PCMweightMat, i, nosieLevel, interation, len(test))
            Energy[i] = calcEnergy(test, weightMat)
            if NeedUpdate == 1:
                Back = 1
            else:
                Back = 0
            if Energy[i] < minEnergy:
                mintest = test.copy()
                minEnergy = Energy[i]
                maxCut = calcMaxcut(mintest, weightMat, n)
                minIteration = i
                NeedUpdate = 0
                Type1Count += 1
            elif (Energy[i] == Energy[i - 1]):
                NeedUpdate = 1
                Type2Count += 1
            else:
                NeedUpdate = 0
                Type3Count += 1

    maxCut = calcMaxcut(mintest, weightMat, n)
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(leveltrace[interation-1])
    #print(Type1Count,Type2Count,Type3Count)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, nosieLevel+1, interation)
    if printPlot == 1:
        plt.scatter(minIteration, minEnergy, s=80, alpha=0.8, marker="*", color='Orange', label='Min')
        plt.plot(Energy)
        plt.scatter(updatetrace, updatetracey, s=20, alpha=0.5, marker="*", color='red', label='Update')
        plt.scatter(backtrace, backtracey, s=20, alpha=0.5, marker="*", color='blue', label='Back')
        plt.xlabel('Iteration')
        plt.ylabel('Energy')
        plt.legend(loc=0, ncol=1)
        #plt.scatter(updatetrace, updatetracey, s=20, alpha=0.8, marker="*", color='red', label='Update')
        plt.show()
        plt.plot(leveltrace,label='IdealLevel')
        plt.scatter(updatetrace, updatetraceDeviation, s=20, alpha=0.5, marker="*", color='red', label='Update')
        #plt.plot(CurrentLeveltrace,label='RealLevel')
        #plt.plot(HighLimitTrace, label='HighLimitTrace')
        plt.xlabel('Iteration')
        plt.ylabel('NoiseDeviation')
        plt.legend(loc=0,ncol=1)
        plt.show()
        print(UpdateCount)
    return maxCut

def HNNtestBlockwithPCMEXP(interation, test, weightMat, n , noiseLevel , noiseType ):
    noiseWeighMat = np.zeros((1600, 26))
    noiseWeighMat = readWeightwithNoisefromExcel(pathOfNoiseWeightMat)
    RSTWeightMat = np.zeros((1000, 16))
    RSTWeightMat = readRSTWeightwithNoisefromExcel(pathofRSTConductance)

    conductanceMat = np.zeros((1600, 26))
    conductanceMat = readConductancewithNoisefromExcel(pathOfNoiseWeightMat)
    RSTconductanceMat = np.zeros((1000, 16))
    RSTconductanceMat = readRSTConductancewithNoisefromExcel(pathofRSTConductance)

    Energy = np.zeros(interation)
    currentNoiseLevel = 22
    leveltrace = []
    PCMweightMat = np.zeros((n, n))
    ConductanceweightMat = np.zeros((n, n))
    minEnergy = 0
    mintest = np.ones(n)
    Meanvalue = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393]
    for i in range(interation):
        level = i / interation
        NoiseLevel = 22 - 22 * level ** (0.25)

        leveltrace.append(NoiseLevel)
        if NoiseLevel <= currentNoiseLevel:
            for ii in range(n):
                for jj in range(ii):
                    if (weightMat[ii][jj] == -1):
                        PCMweightMat[ii][jj] = -1 + noiseWeighMat[random.randint(0,1599),int(currentNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        ConductanceweightMat[ii][jj] = conductanceMat[random.randint(0,1599),int(currentNoiseLevel)]
                        ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    else:
                        PCMweightMat[ii][jj] = 1/Meanvalue[int(currentNoiseLevel)] + RSTWeightMat[random.randint(0,999),random.randint(0,15)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        ConductanceweightMat[ii][jj] = RSTconductanceMat[random.randint(0,999),random.randint(0,15)]
                        ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    # print(PCMweightMat[i][j])
            if (currentNoiseLevel <= 1):
                currentNoiseLevel -= 0.1
            else:
                currentNoiseLevel -= 0.1
        if saveWeightMatrix and (i == 10 or i == 999):
            PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-WeightMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            PCMConductanceweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-ConductanceMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            saveSample(n, ConductanceweightMat, PCMConductanceweightMatpath)
        test = calcXiwithexperimentnoiseV2(test, PCMweightMat, i, noiseLevel, interation)
        Energy[i] = calcEnergy(test, weightMat)
        if Energy[i] < minEnergy:
            mintest = test.copy()
            minEnergy = Energy[i]
            maxCut = calcMaxcut(mintest, weightMat, n)
    maxCut = calcMaxcut(mintest, weightMat, n)
    #plt.plot(noisePCM)
    #plt.show()
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, noiseLevel+1, interation)
    if printPlot == 1:
        plt.plot(Energy)
        plt.show()
        plt.plot(leveltrace)
        plt.show()
    return maxCut


def HNNtestBlockwithPCMEXPv2(interation, test, weightMat, n , noiseLevel , noiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconductanceMat ):

    Energy = np.zeros(interation)
    currentNoiseLevel = 23
    leveltrace = []
    PCMweightMat = np.zeros((n, n))
    ConductanceweightMat = np.zeros((n, n))
    NeedUpdate = 1
    Type1Count = 0
    Type2Count = 0
    Type3Count = 0
    UpdateCount = 0
    updatetrace = []
    updatetracey = []
    minEnergy = 0
    minIteration = 0
    mintest = np.ones(n)
    Meanvalue = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393]
    LevelCount = 0
    for i in range(interation):
        level = i / interation
        choose = []
        LevelSet = [23, 1, 0]
        #LevelSet = [23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0,23,0,0,0]
        #LevelSet = [15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0,15, 0, 0, 0]
        #LevelSet = [23,0,0,23,0,0,23,0,0,15,0,0,15,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0,10,0,0]
        Step = 5
        # NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
        NoiseLevel = 23 - 23 * level


        level = i / interation
        NoiseLevel = 22 - 22 * level ** (0.25)
        
        if level <= 0.15:
            optimalNoiseLevel = LevelSet[0]
        elif level <= 0.5:
            optimalNoiseLevel = LevelSet[2]
        else:
            optimalNoiseLevel = LevelSet[2]

        if (NoiseLevel <= currentNoiseLevel):
            for ii in range(n):
                for jj in range(ii):
                    if (weightMat[ii][jj] == -1):
                        PCMweightMat[ii][jj] = -1 + noiseWeighMat[random.randint(0,1599),optimalNoiseLevel] #try * -1
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = conductanceMat[random.randint(0,1599),optimalNoiseLevel]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    else:
                        #PCMweightMat[ii][jj] = 1/Meanvalue[int(optimalNoiseLevel)] + RSTWeightMat[random.randint(0,999),random.randint(0,15)]
                        PCMweightMat[ii][jj] = PCMweightMat[ii][jj] = (RSTWeightMat[random.randint(0,999),random.randint(0,15)]) / Meanvalue[optimalNoiseLevel]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = RSTconductanceMat[random.randint(0,999),random.randint(0,15)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    # print(PCMweightMat[i][j])
            if (level <= 0.25):
                currentNoiseLevel -= 0.6
                UpdateCount += 1
                updatetrace.append(i)
            else:
                currentNoiseLevel -= 0.3
                UpdateCount += 1
                updatetrace.append(i)
            LevelCount += 1
        if saveWeightMatrix and (i == 10 or i == 999):
            PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-WeightMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            PCMConductanceweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-ConductanceMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            saveSample(n, ConductanceweightMat, PCMConductanceweightMatpath)
        test = calcXiwithexperimentnoiseV2(test, PCMweightMat, i, noiseLevel, interation)
        Energy[i] = calcEnergy(test, weightMat)
        if len(updatetracey) < len(updatetrace):
            updatetracey.append(Energy[i])
        if Energy[i] < minEnergy:
            mintest = test.copy()
            minEnergy = Energy[i]
            maxCut = calcMaxcut(mintest, weightMat, n)
            minIteration = i
            NeedUpdate = 0
            Type1Count += 1
        elif (Energy[i] == Energy[i - 1]):
            NeedUpdate = 1
            Type2Count += 1
        else:
            NeedUpdate = 0
            Type3Count += 1

    maxCut = calcMaxcut(mintest, weightMat, n)
    #plt.plot(noisePCM)
    #plt.show()
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, noiseLevel+1, interation)
    if printPlot == 1:
        print(Type2Count,UpdateCount)
        print(UpdateCount)
        plt.plot(Energy)
        plt.scatter(updatetrace, updatetracey, s=20, alpha=0.4, marker="*", color='green', label='Update')
        plt.scatter(minIteration, minEnergy, s=80, alpha=0.8, marker="*", color='orange', label='Min')
        plt.show()
        plt.plot(leveltrace)
        #plt.show()
    return maxCut

def HNNtestBlockwithPCMEXPv3(interation, test, weightMat, n , noiseLevel , noiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconduct,testnum):

    Energy = np.zeros(interation)
    currentNoiseLevel = 23
    leveltrace = []
    PCMweightMat = np.zeros((n, n))
    ConductanceweightMat = np.zeros((n, n))
    NeedUpdate = 1
    Type1Count = 0
    Type2Count = 0
    Type3Count = 0
    UpdateCount = 0
    updatetrace = []
    updatetracey = []
    backtrace = []
    backtracey = []
    minEnergy = 0
    minIteration = 0
    maxCut = 0
    Back = 0
    mintest = np.ones(n)
    wrongRate = []
    Meanvalue = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393]

    for i in range(interation):
        print(i,maxCut)
        level = i / interation
        choose = []
        LevelSet = [23, 1, 0]
        Step = 5
        # NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
        NoiseLevel = 23 - 23 * level
        optimalNoiseLevel = 0
        '''
        level = i / interation
        NoiseLevel = 22 - 22 * level ** (0.25)
        '''

        if NeedUpdate >= 1 or Back == 1 or (i+n)//n == 0:
            if NeedUpdate == 2:
                optimalNoiseLevel = LevelSet[0]
                updatetrace.append(i-1)
                updatetracey.append(Energy[i-1])
                UpdateCount += 1
                print('Update')
            elif NeedUpdate == 1:
                optimalNoiseLevel = LevelSet[0]
                updatetrace.append(i-1)
                updatetracey.append(Energy[i-1])
                UpdateCount += 1
                print('Update')
            else:
                optimalNoiseLevel = LevelSet[2]
                backtrace.append(i-1)
                backtracey.append(Energy[i-1])
                UpdateCount += 1
                print('Back')
            if (i+n)//n == 0:
                print((i+n)//n)
                optimalNoiseLevel = LevelSet[0]
                UpdateCount += 1
                updatetrace.append(i - 1)
                updatetracey.append(Energy[i - 1])


            for ii in range(n):
                for jj in range(ii):
                    if (weightMat[ii][jj] == -1):
                        PCMweightMat[ii][jj] = -1 + noiseWeighMat[random.randint(0,1599),int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = conductanceMat[random.randint(0,1599),int(optimalNoiseLevel)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    else:
                        #PCMweightMat[ii][jj] = RSTWeightMat[random.randint(0,999),random.randint(0,15)] + 1/Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[ii][jj] = (RSTWeightMat[random.randint(0, 999), random.randint(0, 15)]) / \
                                               Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = RSTconductanceMat[random.randint(0,999),random.randint(0,15)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    # print(PCMweightMat[i][j])
            if (level <= 0.5):
                currentNoiseLevel -= 0.4
                #updatetrace.append(i)
            else:
                currentNoiseLevel -= 0.3


            '''
            if (currentNoiseLevel <= 1):
                currentNoiseLevel -= 0.1
            else:
                currentNoiseLevel -= 0.1
            '''
        if saveWeightMatrix and (i == 10 or i == 999):
            PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-WeightMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            PCMConductanceweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-ConductanceMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            saveSample(n, ConductanceweightMat, PCMConductanceweightMatpath)
        test = calcXiwithexperimentnoiseV2(test, PCMweightMat, i, noiseLevel, interation, wrongRate)
        Energy[i] = calcEnergy(test, weightMat)
        maxCut = calcMaxcut(test, weightMat, n)
        if NeedUpdate == 1:
            Back = 1
        else:
            Back = 0
        if NeedUpdate == 2:
            NeedUpdate = 1
        elif Energy[i] < minEnergy:
            mintest = test.copy()
            minEnergy = Energy[i]

            minIteration = i
            NeedUpdate = 0
            Type1Count += 1
        elif (Energy[i] == Energy[i - 1]):
            NeedUpdate = 2
            Type2Count += 1
        else:
            NeedUpdate = 0
            Type3Count += 1


        maxCut = calcMaxcut(mintest, weightMat, n)
    #plt.plot(noisePCM)
    #plt.show()
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, noiseLevel+1, interation)
    if printPlot == 1:
        print(Type2Count,UpdateCount)
        print(UpdateCount)
        plt.plot(Energy)
        plt.scatter(backtrace, backtracey, s=20, alpha=0.8, marker="*", color='blue', label='Back')
        plt.scatter(updatetrace, updatetracey, s=20, alpha=0.5, marker="*", color='red', label='Update')
        plt.scatter(minIteration, minEnergy, s=100, alpha=0.8, marker="*", color='Orange', label='Min')
        plt.legend()
        plt.show()
        plt.plot(leveltrace)
        #plt.show()
    if saveTestValid == 1:
        saveResultPath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + DUT + '-Node' + str(
            n) + '-' + str(testnum) + Note + '-result.xls'
        saveTest_mul(n,mintest,saveResultPath,maxCut,UpdateCount)
        saveWrongRate(i, saveWrongRatePath, wrongRate)
    return maxCut

def HNNtestBlockwithPCMEXPv4(interation, test, weightMat, n , noiseLevel , noiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconduct,testnum):

    Energy = np.zeros(interation)
    currentNoiseLevel = 23
    leveltrace = []
    PCMweightMat = np.zeros((n, n))
    ConductanceweightMat = np.zeros((n, n))
    NeedUpdate = 1
    Type1Count = 0
    Type2Count = 0
    Type3Count = 0
    UpdateCount = 0
    updatetrace = []
    updatetracey = []
    backtrace = []
    backtracey = []
    minEnergy = 0
    minIteration = 0
    maxCut = 0
    Back = 0
    mintest = np.ones(n)
    tabuList = np.empty((0,n))
    HNNState = 0 #0: find ground state; 1: find best minima; 2: High jump; 3: Low jump;
    jump = True

    Meanvalue = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393]

    for i in range(interation):
        print(i,maxCut)
        level = i / interation
        choose = []
        LevelSet = [23, 1, 0]
        Step = 5
        # NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
        NoiseLevel = 23 - 23 * level
        optimalNoiseLevel = 0

        if HNNState == 0:  # find ground states
            if i == 0:  # rst_n
                jump = True
                optimalNoiseLevel = LevelSet[2]
                print('First Jump')
            elif Energy[i-1] == Energy[i - 2]:
                if Energy[i-1] < minEnergy:
                    HNNState = 1
                    mintest = test.copy()
                    minEnergy = Energy[i-1]
                    minIteration = i
                    print("Find new minima")
                elif(test in tabuList):
                    print("Tabu Hit!")
                    if i >= 1500:
                        test = mintest
                    HNNState = 2

                else:
                    print("New Tabu!")
                    test_add= [test]
                    tabuList=np.append(tabuList,test_add,axis=0)
                    HNNState = 1
            else:
                optimalNoiseLevel = LevelSet[2]
                jump = False
                print("Find",Energy[i-1])
        if HNNState == 1:  # find current best or new minima
            optimalNoiseLevel = LevelSet[1]
            updatetrace.append(i - 1)
            updatetracey.append(Energy[i - 1])
            UpdateCount += 1
            Type1Count += 1
            jump = True
            HNNState = 0
            print('State1')
        elif HNNState == 2:  # big jump
            optimalNoiseLevel = LevelSet[0]
            backtrace.append(i - 1)
            backtracey.append(Energy[i - 1])
            UpdateCount += 1
            Type2Count += 1
            HNNState = 3
            jump = True
            print('State2')
        elif HNNState == 3:  # after big jump
            optimalNoiseLevel = LevelSet[1]
            backtrace.append(i - 1)
            backtracey.append(Energy[i - 1])
            UpdateCount += 1
            Type2Count += 1
            HNNState = 0
            jump = True
            print('State3')
        if jump:
            for ii in range(n):
                for jj in range(ii):
                    if (weightMat[ii][jj] == -1):
                        PCMweightMat[ii][jj] = -1 + noiseWeighMat[random.randint(0,1599),int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = conductanceMat[random.randint(0,1599),int(optimalNoiseLevel)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    else:
                        #PCMweightMat[ii][jj] = RSTWeightMat[random.randint(0,999),random.randint(0,15)] + 1/Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[ii][jj] = (RSTWeightMat[random.randint(0,999),random.randint(0,15)])/Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = RSTconductanceMat[random.randint(0,999),random.randint(0,15)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    # print(PCMweightMat[i][j])

        if saveWeightMatrix and (i == 10 or i == 999):
            PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-WeightMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            PCMConductanceweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-ConductanceMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            saveSample(n, ConductanceweightMat, PCMConductanceweightMatpath)
        test = calcXiwithexperimentnoiseV2(test, PCMweightMat, i, noiseLevel, interation)
        Energy[i] = calcEnergy(test, weightMat)
        maxCut = calcMaxcut(mintest, weightMat, n)
    #end iteration

    maxCut = calcMaxcut(mintest, weightMat, n)
    #plt.plot(noisePCM)
    #plt.show()
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, noiseLevel+1, interation)
    if printPlot == 1:
        print(Type2Count,UpdateCount)
        plt.plot(Energy)
        plt.scatter(backtrace, backtracey, s=20, alpha=0.8, marker="*", color='blue', label='Best/New Local minima')
        plt.scatter(updatetrace, updatetracey, s=20, alpha=0.5, marker="*", color='red', label='Local minima')
        plt.scatter(minIteration, minEnergy, s=100, alpha=0.8, marker="*", color='Orange', label='Min')
        plt.legend()
        plt.show()
        plt.plot(leveltrace)
        #plt.show()
    if saveTestValid == 1:
        saveResultPath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + DUT + '-Node' + str(
            n) + '-' + str(testnum) + Note + '-result.xls'
        saveTest_mul(n,mintest,saveResultPath,maxCut,UpdateCount)
    return maxCut

def HNNtestBlockwithPCMEXPforDataCollect(interation, test, weightMat, n , noiseLevel , noiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconduct,testnum):

    Energy = np.zeros(interation)
    currentNoiseLevel = 23
    leveltrace = []
    PCMweightMat = np.zeros((n, n))
    ConductanceweightMat = np.zeros((n, n))
    NeedUpdate = 1
    Type1Count = 0
    Type2Count = 0
    Type3Count = 0
    UpdateCount = 0
    updatetrace = []
    updatetracey = []
    backtrace = []
    backtracey = []
    minEnergy = 0
    minIteration = 0
    maxCut = 0
    Back = 0
    mintest = np.ones(n)
    wrongRate = []
    Meanvalue = [27.9769,10.40821, 10.45894, 9.97954, 2.93905, 2.77724, 2.62579, 2.45966, 3.1165, 2.3112, 9.02729,
                9.02729, 3.34815, 3.34815, 2.32458,  2.32458, 2.32458, 2.32458, 8.36817, 2.10098, 3.62923, 7.76347, 6.68116, 4.76393]

    for i in range(interation):
        #pseudoTest = np.ones(n) * -1
        saveResultPath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + DUT + '-Node' + str(
            n) + '-' + str(testnum) + Note + '-result.xls'
        pseudoTest = readMinTestfromExcel(saveResultPath,n)
        print(i,maxCut)
        level = i / interation
        choose = []
        LevelSet = [23, 1, 0]
        Step = 5
        # NoiseLevel = 22 - 22 * level ** (0.25)  #0.1  0.1 0.82 for 32 and below
        NoiseLevel = 23 - 23 * level
        optimalNoiseLevel = 0
        '''
        level = i / interation
        NoiseLevel = 22 - 22 * level ** (0.25)
        '''

        if True:
            optimalNoiseLevel = LevelSet[0]
            for ii in range(n):
                for jj in range(ii):
                    if (weightMat[ii][jj] == -1):
                        PCMweightMat[ii][jj] = -1 + noiseWeighMat[random.randint(0,1599),int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = conductanceMat[random.randint(0,1599),int(optimalNoiseLevel)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]
                    else:
                        #PCMweightMat[ii][jj] = RSTWeightMat[random.randint(0,999),random.randint(0,15)] + 1/Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[ii][jj] = (RSTWeightMat[random.randint(0,999),random.randint(0,15)])/Meanvalue[int(optimalNoiseLevel)]
                        PCMweightMat[jj][ii] = PCMweightMat[ii][jj]
                        if saveWeightMatrix:
                            ConductanceweightMat[ii][jj] = RSTconductanceMat[random.randint(0,999),random.randint(0,15)]
                            ConductanceweightMat[jj][ii] = ConductanceweightMat[ii][jj]

        if saveWeightMatrix and (i == 10 or i == 999):
            PCMweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-WeightMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            PCMConductanceweightMatpath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + 'PCM-EXP' + str(
                i) + '-ConductanceMatrix.xls'
            saveSample(n, PCMweightMat, PCMweightMatpath)
            saveSample(n, ConductanceweightMat, PCMConductanceweightMatpath)
        test = calcXiwithexperimentnoiseV2(pseudoTest, PCMweightMat, i, noiseLevel, interation, wrongRate)
        Energy[i] = calcEnergy(pseudoTest, weightMat)

        if NeedUpdate == 1:
            Back = 1
        else:
            Back = 0
        if NeedUpdate == 2:
            NeedUpdate = 1
        elif Energy[i] < minEnergy:
            mintest = test.copy()
            minEnergy = Energy[i]
            maxCut = calcMaxcut(mintest, weightMat, n)
            minIteration = i
            NeedUpdate = 0
            Type1Count += 1
        elif (Energy[i] == Energy[i - 1]):
            NeedUpdate = 2
            Type2Count += 1
        else:
            NeedUpdate = 0
            Type3Count += 1

        maxCut = calcMaxcut(pseudoTest, weightMat, n)
    #plt.plot(noisePCM)
    #plt.show()
    #regularout(test,5)
    #arrayCom(test,sample)
    #print(Energy[interation-1])
    #plt.plot(noiseData)
    if saveEnergyValid:
        SaveEnergy(savePath, Energy, noiseLevel+1, interation)
    if printPlot == 1:
        print(Type2Count,UpdateCount)
        print(UpdateCount)
        plt.plot(Energy)
        plt.scatter(backtrace, backtracey, s=20, alpha=0.8, marker="*", color='blue', label='Back')
        plt.scatter(updatetrace, updatetracey, s=20, alpha=0.5, marker="*", color='red', label='Update')
        plt.scatter(minIteration, minEnergy, s=100, alpha=0.8, marker="*", color='Orange', label='Min')
        plt.legend()
        plt.show()
        plt.plot(leveltrace)
        #plt.show()
    saveWrongRate(len(wrongRate), saveWrongRatePath, wrongRate)
    if saveTestValid == 1:
        #saveResultPath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/' + DUT + '-Node' + str(n) + '-' + str(testnum) + Note + '-result.xls'
        saveTest_mul(n,mintest,saveResultPath,maxCut,UpdateCount)
        saveWrongRate(len(wrongRate), saveWrongRatePath, wrongRate)
    return maxCut

n = 2000
#100
if n == 60:
    e =886
elif n == 100:
    e = 2476
elif n == 800:   #e = 19177
    e = 4673
else:
    e = 19991
d = 0.5
beginNoiselevel = 7
maxNoiseLevel = 8
testTimes = 1
interation = 1 #for basic test
iteration = [10,25,50,100,250,500,1000,200]
NoiseType = 10

if n == 60 or n == 100 or n == 800 or n == 2000:
    WeightMatSel = 1 # 1 from rudy; 2 from minefunction; 3 from localexcel
else:
    WeightMatSel = 2 # 1 from rudy; 2 from minefunction; 3 from localexcel
BasicTest = 0
AnnealingTest = 0
PCMTest = 0
PCMEXPTest = 1

#auto name the file
printPlot = 1
SaveResultValid = 0
saveWeightMatrix = 0
saveEnergyValid = 0
saveTestValid = 0
DUT = ''
Date = '20230323'
Note = ''
if(BasicTest == 1):
    DUT = 'Basic'
elif(AnnealingTest == 1):
    DUT = 'Annealing'
elif(PCMTest == 1):
    DUT = 'PCM'
elif(PCMEXPTest == 1):
    DUT = 'PCM-EXP'

if testTimes != 1:
    printPlot = 0
elif printPlot == 1:
    print('       ------PLOT-PRINT------')

if n == 60:
    path = 'd:\Rudy\g05601.xls'
elif n == 100:
    path =  'd:\Rudy\g05_1000.xls'
elif n == 2000:
    path = 'd:\Rudy\g22.xls'
else:
    path = 'd:\Rudy\g16.xls'

pathofMine = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/1108_Node'+str(n)+'.xls'
pathofSaveSample = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/1108_Node'+str(n)+'.xls'
EnergySavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/'+Date+'/'+DUT+'-Node'+str(n)+'-'+str(interation)+Note+'-Energy.xls'
savePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/'+Date+'/'+DUT+'-Node'+str(n)+'-'+str(interation)+Note+'-DATA.xls'
BasicsavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/'+Date+'/Basic-Node'+str(n)+'-'+str(interation)+'-DATA.xls'
pathOfNoiseWeightMat = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/SetPulse.xls'
pathofRSTConductance = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/RSTCONDUCTANCE.xls'
saveWrongRatePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/resultDeviation.xls'
'''get weightMat from Rudy (n should be manifest)

weightMat = readWeightfromExcel(path,n,e)

#print(weightMat)
'''

'''get weightMat from function

weightMat = getSample(n,d)

saveSample(n,weightMat,pathofSave)
'''
'''getsamplefromMyExcel
weightMat = readWeightfromExcelofMine(pathofMine,n)
'''

#Typical Node 8 sample
'''
weightMat = [[ 0, -1 , 0 , 0 , 0, -1,  0,  0],
 [-1,  0,  0, -1, -1, -1,  0.,  0],
 [ 0,  0,  0, -1, -1,  0,  0,  0],
 [ 0, -1, -1,  0,  0, -1,  0,  0],
 [ 0, -1, -1,  0,  0, -1, -1,  0],
 [-1, -1,  0, -1, -1,  0,  0,  0],
 [ 0,  0,  0,  0, -1,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0]]'''
#Typical Node 16 sample

#Typial Node 32 sample

#Typical Node 50 sample

#Typical Node 60 sample

#Typical Node 80 sample

#Typical Node 100 sample

# test for no noise successPossiblity
if(WeightMatSel == 1):
    print('-Get weitghtmat from rudy n should be manifest-')
    weightMat = readWeightfromExcel(path, n, e)
elif (WeightMatSel == 2):
    print('-----weightmat from function of mine-----')
    weightMat = getSample(n, d)
    saveSample(n, weightMat, pathofSaveSample)
elif (WeightMatSel == 3):
    print('-----weigtmat from local excel-----')
    weightMat = readWeightfromExcelofMine(pathofMine, n)

if(BasicTest == 1):
    testdata = np.ones((testTimes, maxNoiseLevel))
    testpos = np.zeros(maxNoiseLevel)
    for j in range(beginNoiselevel,maxNoiseLevel):
        print('-------Iteration is------- ', iteration[j])
        sumA = 0
        successA = 0
        sumAmax = 0
        sumAaver = 0
        testprocess = 0
        for i in range(testTimes):
            if((i/testTimes)/0.1 > testprocess):
             print('test has been run ',testprocess*10, '%')
             testprocess += 1
            test = np.ones(n)
            sumA = HNNtestBlock(iteration[j],test,weightMat,n,savePath)
            testdata[i,j] = sumA
            #print(sumA)
            sumAaver += sumA
            if sumA == sumAmax:
                successA += 1
            if sumA > sumAmax:
               sumAmax = sumA
               successA = 1
            testpos[j] = successA/testTimes
        print ('no noise success possibility:',successA/testTimes,sumAaver/testTimes,sumAmax)
    if(SaveResultValid == 1):
        SaveResultnew(BasicsavePath, testdata, maxNoiseLevel, testTimes,testpos)
'''
#testfor Annealing'''
if(AnnealingTest == 1):
    BmaxSuccP = 0
    BmaxNoiseLevel = 0
    testdata = np.ones((testTimes, maxNoiseLevel))
    testPos = np.zeros(maxNoiseLevel)
    AnnealingsavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/Annealing-Node' + str(
        n) + '-DATA.xls'
    print('-----Anealing Simulation Start！-----')
    for j in range (beginNoiselevel,maxNoiseLevel):
      print('-------Iteration is------- ', iteration[j])
      sumBaver = 0
      successB = 0
      sumBmax = 0
      sumB = 0
      maxSuccP = 0
      testprocess = 0
      for i in range(testTimes):
        if((i/testTimes)/0.1 > testprocess):
            print('test has been run ',testprocess*10, '%')
            testprocess += 1
        testRand = np.ones(n)
        sumB = HNNtestBlockwithAnnealing(iteration[j],testRand,weightMat, n , j+1 , NoiseType)
        testdata[i,j] = sumB
        #print (sumB)
        sumBaver += sumB
        if sumB == sumBmax:
            successB += 1
        if sumB > sumBmax:
         sumBmax = sumB
         successB = 1
      print('NoiseLevel =', j+1, successB / testTimes, sumBaver / testTimes, sumBmax)
      testPos[j] = successB / testTimes
      if successB > BmaxSuccP:
          BmaxSuccP = successB
          BmaxNoiseLevel = j+1
    print ('MaxSuccess NoiseLevel of Annealing=',BmaxNoiseLevel,BmaxSuccP/testTimes,sumBmax)
    if (SaveResultValid == 1):
        SaveResultnew(AnnealingsavePath, testdata, maxNoiseLevel, testTimes, testPos)

#testfor PCM Noise
''''''
if(PCMTest == 1):
  CmaxSuccP = 0
  CmaxNoiseLevel = 0
  testdata = np.ones((testTimes,maxNoiseLevel))
  testPos = np.zeros(maxNoiseLevel)
  if NoiseType == 9:
    PCMsavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/FixedNoise-Node' + str(n) + '-DATA.xls'
  else:
      PCMsavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/PCM-HNN-Node' + str(
          n) + '-' +Note +'-DATA.xls'
  print('-----PCM-HNN Simulation Start！-----')
  print(Note)
  for j in range(beginNoiselevel,maxNoiseLevel):
    print('-------Iteration is------- ',iteration[j])
    sumCaver = 0
    successC = 0
    sumCmax = 0
    sumC = 0
    testprocess = 0
    for i in range(testTimes):
        if((i/testTimes)/0.1 > testprocess):
            print('test has been run ',testprocess*10, '%')
            testprocess += 1
        testRand = np.ones(n)
        sumC = HNNtestBlockwithNoiseDecay(iteration[j],testRand,weightMat, n , j , NoiseType , printPlot,savePath)
        testdata[i,j] = sumC
        #print (sumC)
        sumCaver += sumC
        if sumC == sumCmax:
            successC += 1
        if sumC > sumCmax:
         sumCmax = sumC
         successC = 1
    print('NoiseLevel =', j+1, successC / testTimes, sumCaver / testTimes, sumCmax, sumC)
    testPos[j] = successC / testTimes
    if successC > CmaxSuccP:
        CmaxSuccP = successC
        CmaxNoiseLevel = j+1
  if (SaveResultValid == 1):
    SaveResultnew(PCMsavePath, testdata, maxNoiseLevel, testTimes,testPos)
  print ('MaxSuccess NoiseLevel of this work=',CmaxNoiseLevel,CmaxSuccP/testTimes)


#testfor PCM Noise in experiment
''''''
if(PCMEXPTest == 1):
  DmaxSuccP = 0
  DmaxNoiseLevel = 0
  testdata = np.ones((testTimes,maxNoiseLevel))
  testPos = np.zeros(maxNoiseLevel)
  choose = []
  PCMEXPsavePath = 'D:/1StudyFile/PCRAM/Compute in Memory/HNN-PCM/data/' + Date + '/PCM-EXP-Node' + str(n)+ '-' + Note + '-DATA.xls'
  print('PCM-EXP-HNN Simulation Start！')
  for j in range (beginNoiselevel,maxNoiseLevel):
    print('-------Iteration is------- ', iteration[j])
    sumDaver = 0
    successD = 0
    sumDmax = 0
    sumD = 0
    testprocess = 0
    noiseWeighMat = np.zeros((1600, 26))
    noiseWeighMat = readWeightwithNoisefromExcel(pathOfNoiseWeightMat)
    RSTWeightMat = np.zeros((1000, 16))
    RSTWeightMat = readRSTWeightwithNoisefromExcel(pathofRSTConductance)

    conductanceMat = np.zeros((1600, 26))
    conductanceMat = readConductancewithNoisefromExcel(pathOfNoiseWeightMat)
    RSTconductanceMat = np.zeros((1000, 16))
    RSTconductanceMat = readRSTConductancewithNoisefromExcel(pathofRSTConductance)
    for i in range(testTimes):
        if((i/testTimes)/0.1 > testprocess):
            print('test has been run ',testprocess*10, '%')
            testprocess += 1
        testRand = np.ones(n) * -1
        #sumD = HNNtestBlockwithPCMEXPforDataCollect(iteration[j],testRand,weightMat, n , j , NoiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconductanceMat,i)
        sumD = HNNtestBlockwithPCMEXPv3(iteration[j],testRand,weightMat, n , j , NoiseType, noiseWeighMat, RSTWeightMat, conductanceMat, RSTconductanceMat,i)
        testdata[i,j] = sumD
        #print (sumC)
        sumDaver += sumD
        if sumD == sumDmax:
            successD += 1
        if sumD > sumDmax:
         sumDmax = sumD
         successD = 1
    print('NoiseLevel =', j+1, successD / testTimes, sumDaver / testTimes, sumDmax)
    testPos[j] = successD / testTimes
    if successD > DmaxSuccP:
        DmaxSuccP = successD
        DmaxNoiseLevel = j+1
  if (SaveResultValid == 1):
    SaveResultnew(PCMEXPsavePath, testdata, maxNoiseLevel, testTimes,testPos)
  print ('MaxSuccess NoiseLevel of experiment pcm=',DmaxNoiseLevel,DmaxSuccP/testTimes)



'''
test for getMaxcut
for i in range(testTimes):
    test = np.ones(n)
    sumA = HNNtestBlock(interation,test,weightMat,n)
    if sumA > sumAmax:
        sumAmax = sumA
print (sumAmax)

for i in range(testTimes):
    testRand = np.ones(n)
    sumB = HNNtestBlockwithRand(interation,testRand,weightMat,n)
    if sumB > sumBmax:
        sumBmax = sumB
print (sumBmax)'''