#这个程序是用来将xml文件的道路限速信息提取出来（苏雨）
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
from numpy import sqrt

#要读取的kml文件名（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()   
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}   
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex 

#创建列表存储最大速度（苏雨）
maxspeedlist = []
  
#创建输出头文件，如果存在就覆盖掉（苏雨）
with open('output_paths.txt','w') as out_pat: 
    #添加说明头文件（苏雨）
    out_pat.write('Pin Name,Pin_#,Latitude,Longitude,Height\n')
    #定义列表来存储道路名字（苏雨）
    namelist = []
    #定义是否重名判断符，若1则出现重名（苏雨）
    same = 0
    #定义第一次判断符（苏雨）
    first = 0        
    #寻找坐标点（苏雨）
    count = 0
    for i in root.findall('.//def:Placemark', ns):
        name = i.find('def:name', ns).text
        coord = i.find('.//def:coordinates', ns)      
        #把道路名字打出来以便检查（苏雨）                   
        #print(i.find('def:name', ns).text) 
        #下面步骤是将不同道路名称读取出来，存入列表（苏雨）
        num=0
        #遍历列表，防止重名（苏雨）
        #第一次先直接添加列表（苏雨）
        if first == 0:
            namelist.append(name)
            first = 1
        while num < len(namelist):
            #如果出现重名，则判断符置1（苏雨）
            if name == namelist[num]:
                same = 1
                #print('出现重复！')
                break  
            else:
                same = 0
            num = num + 1
        if same == 0:   
            namelist.append(name)  
        #用来解决列表越界的问题（苏雨）
        if count < len(namelist) - 1:
            count = count + 1  
#print(namelist)
#1.导入模块
dom=minidom.parse("/home/suyu/test/test2.kml") #2.加载xml文件
root = dom.documentElement
Placemark = root.getElementsByTagName('Placemark')
#判断道路同名，若同名则归纳到一行里面（苏雨）
samename = []
#直接开循环，按照list里的名单逐个查找道路限速（苏雨）
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
        
#在提取到道路限速后，开始计算道路风险值（苏雨）        
#对于旋翼飞行器，我们先用大疆精灵4作为例子（苏雨）
#参考文献：Ground impact probability distribution for small unmanned aircraft in ballistic desent（苏雨）       

#飞行器质量，单位kg（苏雨）
m = 1.4
#飞行器巡航速度，单位m/s（苏雨）
v_cruise = 6.5
#重力加速度，单位m/s^2（苏雨）
g = 9.8
#空气密度，单位kg/m^3（苏雨）
row = 1.29
#空气阻力系数（苏雨）
CD = 0.45
#迎风面积，单位m^2（苏雨）
A = 0.02
#飞行高度，单位m（苏雨）
H = 50

#撞击地面造成的冲击动能（苏雨）
Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))
print(Ek)

#水平威胁距离，单位m（苏雨）
Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*H)/(2*m)))
print(Lthreat)












#对于固定翼飞行器，参考文献 Quantifying Risk of Ground Impact Fatalities for Small Unmanned Aircraft 中的参数（苏雨）
#飞行器质量，单位kg（苏雨）
m = 16
#飞行器滑翔速度，单位m/s（苏雨）
v_glide = 16
#重力加速度，单位m/s^2（苏雨）
g = 9.8
#滑翔比（苏雨）
GL = 12
#空气密度，单位kg/m^3（苏雨）
row = 1.29 
#机翼面积，单位m^2（苏雨）
S = 2
#迎风面积，单位m^2（苏雨）
A = 0.3
#飞行高度，单位m（苏雨）
H = 100



#撞击地面造成的冲击动能（苏雨）
#Ek = (m*v_cruise**2)/2 + (m**2)*(g-(Cy*row*v_cruise**2*S)/(2*m))/(row*CD*A)*(1-math.exp(-(row*CD*A*H)/m))
Ek = 0.5*m*v_cruise**2     
print(Ek)

#水平威胁距离，单位m（苏雨）
#Lthreat = (H*Cy*S)/(CD*A)
Lthreat = GL*H
print(Lthreat)



