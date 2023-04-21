import random
import numpy as np
import matplotlib.pyplot as plt

def calcWeight(savedsample):
    N = len(savedsample[0])
    P = len(savedsample)
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
            for u in range(P):
                sum += savedsample[u][i] * savedsample[u][j]
            returnMat[i][j] = sum/float(N)
    return returnMat

def calcEnergy(inMat , weighMat):
    matEnergy = 0
    for i in range(len(inMat)):
        for j in range(len(inMat)):
            matEnergy += -1/2 * weighMat[i][j] * inMat[i] * inMat[j]
    #print (matEnergy)
    return matEnergy

'''def calcXi(inMat , weighMat,intera):
    returnMat = inMat
    choose = []
    for i in range(len(inMat)//25):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
        if sum>=(random.random()-0.5)/3:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat'''

def calcXi(inMat , weighMat,intera):
    returnMat = inMat
    choose = []
    for i in range(len(inMat)//25):
        #随机改变N/5个神经元的值，该参数可调，也可同时改变所有神经元的值
        choose.append(random.randint(0,len(inMat)-1))
    for i in choose:
        sum = 0
        for j in range(len(inMat)):
            sum += weighMat[i][j] * inMat[j]
        if sum>=(random.random()-0.5)/3:
            returnMat[i] = 1
        else: returnMat[i] = -1
    return returnMat

sample =  [[1,-1,-1,-1,1,
           1,1,-1,-1,1,
           1,-1,1,-1,1,
           1,-1,-1,1,1,
           1,-1,-1,-1,1],
          [1,1,1,1,1,
           1,-1,-1,-1,-1,
           1,1,1,1,1,
           1,-1,-1,-1,-1,
           1,1,1,1,1],
          [1,1,1,1,-1,
           1,-1,-1,-1,1,
           1,1,1,1,-1,
           1,-1,-1,1,-1,
           1,-1,-1,-1,1],
          [-1,1,1,1,-1,
           1,-1,-1,-1,1,
           1,-1,-1,-1,1,
           1,-1,-1,-1,1,
           -1,1,1,1,-1]]

def addnoise(mytest_data,n):
    noise_data = mytest_data[:]
        #[1]*n*n
    for x in range(n):
        for y in range(n):
            if random.randint(0, 10) > 6:
                noise_data[x * n + y] = -mytest_data[x * n + y]
    return noise_data

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

weightMat =  calcWeight(sample)
regularout(sample[1],5)
E = calcEnergy(sample[1],weightMat)
print (E)

test = addnoise(sample[1],5)
regularout(test,5)
calcEnergy(test,weightMat)

#print(sample[1])

interation = 200
Energy = np.zeros(interation)
for i in range(interation):
    test = calcXi(test,weightMat,interation)
    Energy[i] = calcEnergy(test,weightMat)
regularout(test,5)

arrayCom(test,sample[1])
#print(sample[1])
print(Energy[interation-1])
plt.plot(Energy)
plt.show()

