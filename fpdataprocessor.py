#苏雨的飞行计划信息提取程序
import csv
with open('flightplan.csv',"r") as csvfile:
    reader = csv.reader(csvfile)
    rows= [row for row in reader]
#print (rows)

#先看一下有几个航班，每个航班几个航点（苏雨）
i = 1
#航班数量（苏雨）
flnum = 1
#对比名称初始化（苏雨）
name = rows[1][1]
#print (name)
while i < len(rows):
    if rows[i][1] != name:
        flnum = flnum + 1
        name = rows[i][1]
    i = i + 1
#print(flnum)    

#定义二维数组，航班序号，经纬高度速度（苏雨）
fllat = [[] for j in range(flnum)]
fllon = [[] for j in range(flnum)]
flalt = [[] for j in range(flnum)]

i = 1
flnum = 1
name = rows[1][1]
while i < len(rows):
    if rows[i][1] != name:
        flnum = flnum + 1
        name = rows[i][1] 
    fllat[flnum-1].append(float(rows[i][3]))
    fllon[flnum-1].append(float(rows[i][4]))
    flalt[flnum-1].append(float(rows[i][5]))        
    i = i + 1
#print(fllat) 
#print(fllon) 
#print(flalt)
