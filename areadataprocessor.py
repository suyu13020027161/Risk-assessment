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
print(transferdata_2)    
             

