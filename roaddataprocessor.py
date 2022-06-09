#苏雨的道路信息提取程序
# -*- coding: utf-8 -*-
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
from numpy import sqrt
pi = math.pi


#要读取的kml文件名（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()
    
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}
    
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex

namelist = []
for i in root.findall('.//def:Placemark', ns):
    name = i.find('def:name', ns).text
    #print(name)
    namelist.append(name)

print(namelist)
print(len(namelist))


#创建列表存储最大速度（苏雨）
maxspeedlist = []
#提取道路限速（苏雨）
dom=minidom.parse("/home/suyu/FPriskassessment/test2.kml") 
root = dom.documentElement
Placemark = root.getElementsByTagName('Placemark')
listnum = 0
while listnum < len(namelist):
    for i in range(len(Placemark)):
        n = Placemark[i].childNodes[1]
        na = n.firstChild
        name = na.data
        
        #当查到对应的道路名字（苏雨）
        if name == namelist[listnum]:
            #print (name)
            ExtendedData = Placemark[i].childNodes[3] 
           
            #下面请注意，每一条路参数里面限速所在位置都不一样，所以需要动用循环来找（苏雨）
            num = 1    
            while num < len(ExtendedData.childNodes):
                data = ExtendedData.childNodes[num]
                dataname = data.getAttribute("name")
                #print(dataname)
                num = num + 2
                if dataname == 'maxspeed':
                    maxspeed = data.childNodes[1]
                    maxspeedvalue = maxspeed.childNodes[0]
                    maxspeedvalue = maxspeedvalue.data
                    #print(maxspeedvalue)
                    #将限速转换为数值（苏雨）
                    if maxspeedvalue == '70 mph':
                        maxspeedvalue = 70
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '60 mph':
                        maxspeedvalue = 60
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)                    
                    elif maxspeedvalue == '40 mph':
                        maxspeedvalue = 40
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '30 mph':
                        maxspeedvalue = 30
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)
                    elif maxspeedvalue == '20 mph':
                        maxspeedvalue = 20
                        #print(maxspeedvalue)
                        maxspeedlist.append(maxspeedvalue)                                                                      
            break
    listnum = listnum + 1

print(maxspeedlist)
print(len(maxspeedlist))   



#提取道路数据存入二维列表（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()   
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}

#注意这里要创建二维列表来存储道路数据（苏雨）
kmllist = [[] for i in range(len(maxspeedlist))]
road_number = 0

          
for i in root.findall('.//def:Placemark', ns):
    name = i.find('def:name', ns).text
    coord = i.find('.//def:coordinates', ns)  
    #按照路的名称，将路的航点分别筛选储存（苏雨）     
    if not coord is None:    
        coord = coord.text.strip()
        coord = re.findall(regex, coord)                                
    #print(count)

    #print(name)
        
    #kmllist = []
    for (long, lat, heig) in coord:
        if i.find('.//def:LineString', ns):                         
            fllong = float(long)
            fllat = float(lat)              
            kmllist[road_number].append(fllong)
            kmllist[road_number].append(fllat) 
    road_number = road_number + 1
print(kmllist)
print(len(kmllist))



 
