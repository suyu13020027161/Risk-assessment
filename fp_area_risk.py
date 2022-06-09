#######################################################################################################################################################################################################
#苏雨的飞行计划信息提取程序
import csv
with open('flightplan2.csv',"r") as csvfile:
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
#飞行速度（苏雨）
flspeed = rows[1][7]
#print(flspeed)
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


#提取所有区域信息，按照文件夹分别存入数组（苏雨）
dom=minidom.parse("/home/suyu/riskassessment/area2.kml") 
root = dom.documentElement
Folder = root.getElementsByTagName('Folder')
n = Folder[0].childNodes[3]
na = n.childNodes[1]
nam = na.childNodes[0]
name = nam.data
#注意这里要创建二维列表来存储区域数据（苏雨）
areadata = [[] for i in range(len(Folder))]
j = 0
#第一重循环是循环文件夹（苏雨）
while j < len(Folder):
    #请注意getElementsByTagName这个函数返回的是一个列表，要想用它必须对元素操作而不是列表（苏雨）
    Placemark = Folder[j].getElementsByTagName('Placemark')
    #print(len(Placemark))
    #循环写入每个文件夹里面的区域数据（苏雨）
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
#苏雨的飞行计划风险评估程序
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes
import time
from shapely.geometry import Polygon  # 多边形
import scipy.io as io

#定义出现问题航段高度向量（苏雨）
problemh = []

#下面直接计算行人风险值（苏雨）
Peoplelist = []
num = 0
#以旋翼飞行器为例（苏雨）
#飞行器质量（苏雨）
m = 1.4
#巡航速度（苏雨）
v_cruise = 6.5
g = 9.8
row = 1.29
CD = 0.45
A = 0.02
#巡航高度（苏雨）
H = 50
#人口风险权重（苏雨）
warea = 6
#英国平均人口密度，每平方米人口（苏雨）
rowpeople = 0.000434
#定义遮蔽系数表（苏雨）
shelterlist = [1,0.8,0.75,0.65,0.55,0.45,0.35,0.3,0.25]
#求飞行器坠地动能（苏雨）
Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))
#定义人口分布权重表（苏雨）
peopleweight = [0,0.05,0.05,0.05,0.075,0.075,0.2,0.2,0.3]
#坠落概率（苏雨）
P_crash = 1/10**3
#最终区域风险航段坐标向量（苏雨）
problematicareaplan = []
#最终区域风险航段对应的风险（苏雨）
problematicarearisk = []




























 

#先求出现问题部分重叠区域面积（苏雨）
#定义重叠区域面积向量（苏雨）
problemarea = []
#定义重叠区域名称向量（苏雨）
problemname = []
#定义出问题航段坐标向量（苏雨）
problemfp = []


i = 0
problemnum = 0
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
                    problemfp.append(fpline)
                    #计算出现问题航段的平均高度（苏雨）
                    avgh = (flightalt[i][j]+flightalt[i][j+1])/2
                    Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*float(avgh))/(2*m)))                     
                    
                    #print (fpline)
                    #print(transferdata_2[areanum][polynum])
                    #求飞行计划风险面积和地面区域相交面积（苏雨）
                    #先把航线线段拓展为矩形（苏雨）
                    wpx1 = fpline[0][0]
                    wpy1 = fpline[0][1]
                    wpx2 = fpline[1][0]
                    wpy2 = fpline[1][1]                                      
                    Length1 = Lthreat
                    problemnum = problemnum  + 1
                    H1 = (Length1*(wpx2-wpx1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5) 
                    L1 = (Length1*(wpy2-wpy1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5)
                    #矩形顺时针从左上顶点开始（苏雨）
                    #请注意经纬度和米的换算！！！（苏雨）
                    latlontom = 180/(pi*111000)                                
                    x1 = wpx1 - L1*latlontom
                    y1 = wpy1 + H1*latlontom
                    x2 = wpx2 - L1*latlontom
                    y2 = wpy2 + H1*latlontom
                    x3 = wpx2 + L1*latlontom
                    y3 = wpy2 - H1*latlontom
                    x4 = wpx1 + L1*latlontom
                    y4 = wpy1 - H1*latlontom
                    #带比较的第一个物体的顶点坐标（苏雨）
                    data1 = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]                   
                    data2 = transferdata_2[areanum][polynum]
                    poly1 = Polygon(data1).convex_hull
                    poly2 = Polygon(data2).convex_hull
                    inter_area = poly1.intersection(poly2).area*(latlontom**(-2))
                    problemarea.append(inter_area)                    
                    
                    #print ('\n')
                    #print (j)
                    #print (i)
                    #print ('\n') 
                    #记录问题区域名称（苏雨）
                    problemname.append(namelist[areanum])                
                polynum = polynum + 1            
            areanum = areanum + 1       
        j = j + 1
    i = i + 1







#print(problemarea)
#print(problemname) 
#print(problemfp)




#计算行人风险（苏雨）
i = 0
j = 0
#定义航段比较参数并初始化（苏雨）
compare = problemfp[0]
while i < len(problemfp):
    #如果是第一位直接算风险存入向量第一位（苏雨）
    if i == 0:
        #开始计算风险（苏雨）    
        #先确定遮蔽系数和行人密度系数（苏雨）
        if problemname[i] == 'High Street and Promenades':
            #行人密度权重（苏雨）
            rowweight = 0.05
            #遮蔽系数（苏雨）
            shelter = 0.8
        elif problemname[i] == 'Railway Buzz':
            #行人密度权重（苏雨）
            rowweight = 0.05
            #遮蔽系数（苏雨）
            shelter = 0.75        
        elif problemname[i] == 'Waterside Settings':
            #行人密度权重（苏雨）
            rowweight = 0.05
            #遮蔽系数（苏雨）
            shelter = 0.7        
        elif problemname[i] == 'Countryside Sceneries':
            #行人密度权重（苏雨）
            rowweight = 0.075
            #遮蔽系数（苏雨）
            shelter = 0.5  
        elif problemname[i] == 'Suburban Landscapes':
            #行人密度权重（苏雨）
            rowweight = 0.075
            #遮蔽系数（苏雨）
            shelter = 0.45 
        elif problemname[i] == 'The Old Town':
            #行人密度权重（苏雨）
            rowweight = 0.2
            #遮蔽系数（苏雨）
            shelter = 0.35 
        elif problemname[i] == 'Victorian Terraces':
            #行人密度权重（苏雨）
            rowweight = 0.2
            #遮蔽系数（苏雨）
            shelter = 0.3 
        elif problemname[i] == 'Central Business District':
            #行人密度权重（苏雨）
            rowweight = 0.3
            #遮蔽系数（苏雨）
            shelter = 0.25 
        #P_impact和受影响行人数量线性相关，系数暂定为1（苏雨）
        P_impact = problemarea[i]*rowpeople*rowweight        
        #冲击动能（苏雨）
        Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))         
        P_fatality = 1/(1+100*(100/Ek)**(1/(4*shelter)))        
        #最终航段行人风险（苏雨）
        Rarea = warea*P_crash*P_impact*P_fatality*10**7   
        problematicarearisk.append(Rarea)
        problematicareaplan.append(problemfp[i])        
        
    else:
        #如果是同一条航段（苏雨）
        if compare == problemfp[i]:
            #先确定遮蔽系数和行人密度系数（苏雨）
            if problemname[i] == 'High Street and Promenades':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.8
            elif problemname[i] == 'Railway Buzz':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.75        
            elif problemname[i] == 'Waterside Settings':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.7        
            elif problemname[i] == 'Countryside Sceneries':
                #行人密度权重（苏雨）
                rowweight = 0.075
                #遮蔽系数（苏雨）
                shelter = 0.5  
            elif problemname[i] == 'Suburban Landscapes':
                #行人密度权重（苏雨）
                rowweight = 0.075
                #遮蔽系数（苏雨）
                shelter = 0.45 
            elif problemname[i] == 'The Old Town':
                #行人密度权重（苏雨）
                rowweight = 0.2
                #遮蔽系数（苏雨）
                shelter = 0.35 
            elif problemname[i] == 'Victorian Terraces':
                #行人密度权重（苏雨）
                rowweight = 0.2
                #遮蔽系数（苏雨）
                shelter = 0.3 
            elif problemname[i] == 'Central Business District':
                #行人密度权重（苏雨）
                rowweight = 0.3
                #遮蔽系数（苏雨）
                shelter = 0.25 
            #P_impact和受影响行人数量线性相关，系数暂定为1（苏雨）
            P_impact = problemarea[i]*rowpeople*rowweight        
            #冲击动能（苏雨）
            Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))         
            P_fatality = 1/(1+100*(100/Ek)**(1/(4*shelter)))        
            #最终航段行人风险（苏雨）
            Rarea = warea*P_crash*P_impact*P_fatality*10**7     
            #同航段风险直接往上加（苏雨）
            problematicarearisk[j] = problematicarearisk[j] + Rarea
        #如果不是同一条航段（苏雨）
        else:
            j = j + 1
            #先确定遮蔽系数和行人密度系数（苏雨）
            if problemname[i] == 'High Street and Promenades':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.8
            elif problemname[i] == 'Railway Buzz':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.75        
            elif problemname[i] == 'Waterside Settings':
                #行人密度权重（苏雨）
                rowweight = 0.05
                #遮蔽系数（苏雨）
                shelter = 0.7        
            elif problemname[i] == 'Countryside Sceneries':
                #行人密度权重（苏雨）
                rowweight = 0.075
                #遮蔽系数（苏雨）
                shelter = 0.5  
            elif problemname[i] == 'Suburban Landscapes':
                #行人密度权重（苏雨）
                rowweight = 0.075
                #遮蔽系数（苏雨）
                shelter = 0.45 
            elif problemname[i] == 'The Old Town':
                #行人密度权重（苏雨）
                rowweight = 0.2
                #遮蔽系数（苏雨）
                shelter = 0.35 
            elif problemname[i] == 'Victorian Terraces':
                #行人密度权重（苏雨）
                rowweight = 0.2
                #遮蔽系数（苏雨）
                shelter = 0.3 
            elif problemname[i] == 'Central Business District':
                #行人密度权重（苏雨）
                rowweight = 0.3
                #遮蔽系数（苏雨）
                shelter = 0.25 
            #P_impact和受影响行人数量线性相关，系数暂定为1（苏雨）
            P_impact = problemarea[i]*rowpeople*rowweight        
            #冲击动能（苏雨）
            Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))         
            P_fatality = 1/(1+100*(100/Ek)**(1/(4*shelter)))        
            #最终航段行人风险（苏雨）
            Rarea = warea*P_crash*P_impact*P_fatality*10**7     
            problematicarearisk.append(Rarea)
            problematicareaplan.append(problemfp[i])
            compare = problemfp[i]
    i = i + 1






         


print(problematicareaplan)
print(problematicarearisk)        
#######################################################################################################################################################################################################
