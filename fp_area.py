#######################################################################################################################################################################################################
#苏雨的飞行计划信息提取程序
import csv
with open('flightplan.csv',"r") as csvfile:
    reader = csv.reader(csvfile)
    rows= [row for row in reader]
#print (rows)

#先看一下有几个航班，每个航班几个航点（苏雨）
i = 1
#航班数量（苏雨）
flightnum = 1
#对比名称初始化（苏雨）
name = rows[1][1]
#print (name)
while i < len(rows):
    if rows[i][1] != name:
        flightnum = flightnum + 1
        name = rows[i][1]
    i = i + 1
#print(flightnum)    

#定义二维数组，航班序号，经纬高度速度（苏雨）
flightlat = [[] for j in range(flightnum)]
flightlon = [[] for j in range(flightnum)]
flightalt = [[] for j in range(flightnum)]

i = 1
flightnum = 1
name = rows[1][1]
while i < len(rows):
    if rows[i][1] != name:
        flightnum = flightnum + 1
        name = rows[i][1] 
    flightlat[flightnum-1].append(float(rows[i][3]))
    flightlon[flightnum-1].append(float(rows[i][4]))
    flightalt[flightnum-1].append(float(rows[i][5]))        
    i = i + 1
#print(flightlat) 
#print(flightlon) 
#print(flightalt)
#######################################################################################################################################################################################################














#######################################################################################################################################################################################################
#苏雨的区域信息提取程序
# -*- coding: utf-8 -*-
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
import numpy
from numpy import sqrt
pi = math.pi

#要读取的kml文件名（苏雨）
tree = ET.parse('area2.kml')
root = tree.getroot()
    
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}
    
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex

namelist = []
for i in root.findall('.//def:Folder', ns):
    name = i.find('def:name', ns).text
    #print(name)
    namelist.append(name)

#print(len(namelist))
#print(len(namelist))

#提取所有区域信息，按照文件夹分别存入数组（苏雨）
dom=minidom.parse("/home/suyu/riskassessment/area2.kml") 
root = dom.documentElement
Folder = root.getElementsByTagName('Folder')
n = Folder[0].childNodes[3]
na = n.childNodes[1]
nam = na.childNodes[0]
name = nam.data
#注意这里要创建二维列表来存储道路数据（苏雨）
areadata = [[] for i in range(len(Folder))]
j = 0
#第一重循环是循环文件夹（苏雨）
while j < len(Folder):
    #请注意getElementsByTagName这个函数返回的是一个列表，要想用它必须对元素操作而不是列表（苏雨）
    Placemark = Folder[j].getElementsByTagName('Placemark')
    #print(len(Placemark))
    #循环写入每个文件夹里面的道路数据（苏雨）
    k = 0
    #第二重循环是循环每个文件夹里的区域（苏雨）
    while k < len(Placemark):
        Polygon = Placemark[k].childNodes[5]
        outerBoundaryIs = Polygon.childNodes[3]
        LinearRing = outerBoundaryIs.childNodes[1]
        coordinates = LinearRing.childNodes[1]
        co = coordinates.childNodes[0]
        coo = co.data
        #提取这个坐标字符串中的浮点数（苏雨）
        number = re.findall(r'-?\d+\.?\d*e?-?\d*?', coo)
        #print(number)
        areadata[j].append(number)
        k = k + 1
    j = j + 1
     
#print(areadata[0][0])
#print(areadata[0][0])
#按照判断程序格式存储数据（苏雨）
transferdata_0 = []
transferdata_1 = []
transferdata_2 = []
transferdata_coord = []
i = 0
while i < len(areadata):
    j = 0
    transferdata_1 = []
    while j < len(areadata[i]):
        k = 0
        transferdata_0 = []
        while k < (len(areadata[i][j]) - 2):
            transferdata_coord = []
            transferdata_coord.append(float(areadata[i][j][k]))
            transferdata_coord.append(float(areadata[i][j][k+1]))
            transferdata_0.append(transferdata_coord)
            k = k + 3
        transferdata_1.append(transferdata_0)
        j = j + 1
    transferdata_2.append(transferdata_1)      
    i = i + 1
#print(areadata)    
#print(transferdata_2)    
#######################################################################################################################################################################################################


 


































#######################################################################################################################################################################################################
#苏雨的飞行计划和区域相交评估程序
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes




i = 0
while i < (flightnum):
    j = 0
    while j < (len(flightlat[i]) - 1):
        #这里就对每个航线段开始循环判断是否与区域冲突了（苏雨）
        areanum = 0
        while areanum < len(transferdata_2):
            polynum = 0
            while polynum < (len(transferdata_2[areanum])):
                clip_poly = shapely.geometry.Polygon(transferdata_2[areanum][polynum])
                #航点坐标，注意经纬度（苏雨）
                fpp_1 = []
                fpp_1.append(flightlon[i][j])
                fpp_1.append(flightlat[i][j])
                fpp_2 = []
                fpp_2.append(flightlon[i][j+1])
                fpp_2.append(flightlat[i][j+1])                
                fpline = []
                fpline.append(fpp_1)
                fpline.append(fpp_2)                                
                line = shapely.geometry.LineString(fpline)
                if(line.intersects(clip_poly)==True):                
                    print (fpline)
                    #print (j)
                    #print (i)
                    #print ('\n')                        
                polynum = polynum + 1
            areanum = areanum + 1       
        j = j + 1
    i = i + 1
   
#######################################################################################################################################################################################################
