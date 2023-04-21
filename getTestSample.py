import random
import numpy as np

def getSample ( n , d ):
    # d for edge density 0<d<1
    totalNode = (1+n)*n/2
    edge = d * (1+n)*n/2
    print(totalNode,edge)
    testArray = -np.ones(int(totalNode))
    i = 0
    while i < int(edge):
        x = random.randint(0,totalNode-1)
        if testArray[x] != 1:
            testArray[x] = 1
            i += 1
    print(i)
    return testArray

def verifySample (test,edge):
    sum = 0
    result = 'Same'
    for i in range (len(test)):
        if test[i-1] == 1:
            sum += 1
    if sum != edge:
        result = 'Different'
    print (result)

#testSample = -np.zeros(n,n)
n = 8
d = 0.5
# n for node number
# d for edge density

edge  = d * (1+n)*n/2

testArray = getSample(n,d)
verifySample(testArray,edge)




