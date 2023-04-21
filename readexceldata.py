import xlrd
import xlwt
import os
import numpy as np


readbook = xlrd.open_workbook(r'd:\Rudy\g05600.xls')
table = readbook.sheets()[0]
array = -1 * np.ones((60,60))

for i in range(60):
    for j in range(60):
        if i == j:
            array[i][j] = 0

for i in range(2,886):
    array_x = table.cell(i,0).value
    array_y = table.cell(i,1).value

    array[int(array_x)-1][int(array_y)-1] = 1 # table.cell(i,2).value
    array[int(array_y)-1][int(array_x)-1] = array[int(array_x)-1][int(array_y)-1]
