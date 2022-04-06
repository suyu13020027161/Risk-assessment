#这个程序用来评估道路风险，并将风险值作为高度存入kml文件（苏雨）
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
from numpy import sqrt



#######################################################################################################################################################################################################
#创建KML头文件（苏雨）
#先写头文件（苏雨） 
f = open("KML.kml", "w")
head1 = '<?xml version="1.0" encoding="UTF-8"?>'
f.write(head1)
f.write('\n')
head2 = '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
f.write(head2)
f.write('\n')
f.write("<Document>\n")
f.write("\t<name>" + 'KML.kml' + "</name>\n")
#######################################################################################################################################################################################################








#######################################################################################################################################################################################################
#在提取道路限速（苏雨） 
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

#print(maxspeedlist)
#print(len(maxspeedlist))     
#######################################################################################################################################################################################################







#######################################################################################################################################################################################################    
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
#print(Ek)

#水平威胁距离，单位m（苏雨）
Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*H)/(2*m)))
#print(Lthreat)

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
#print(Ek)

#水平威胁距离，单位m（苏雨）
#Lthreat = (H*Cy*S)/(CD*A)
Lthreat = GL*H
#print(Lthreat)




#道路风险权重（苏雨）
wroad = 0.3
#道路车辆密度，初步定义为辆每平方米（苏雨）
rowcar = 0.2


#######################################################################################################################################################################################################













#######################################################################################################################################################################################################
#提取道路数据，叠加风险值后存入txt文件（苏雨）
#要读取的kml文件名（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()   
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}   
coord_ex = '(-?\d+\.\d+),'
heig_ex = '(\d+)'
regex = coord_ex + coord_ex + heig_ex   
#创建输出头文件，如果存在就覆盖掉（苏雨）
with open('risk_paths.txt','w') as out_pat: 
    #添加说明头文件（苏雨）
    out_pat.write('Road Name,Latitude,Longitude,Riskvalue,Riskdistance\n')
    #定义列表来存储道路名字（苏雨）
    list = []
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
            list.append(name)
            first = 1
        while num < len(list):
            #如果出现重名，则判断符置1（苏雨）
            if name == list[num]:
                same = 1
                #print('出现重复！')
                break  
            else:
                same = 0
            num = num + 1
        if same == 0:   
            list.append(name)  
        #用来解决列表越界的问题（苏雨）
        if count < len(list) - 1:
            count = count + 1  
#print(list)







    count = 0
    #创建列表存储KML航点坐标（苏雨）

    while count < len(list):
    
        kmllist = []
    
    
        for i in root.findall('.//def:Placemark', ns):
        
            
            
            name = i.find('def:name', ns).text
            coord = i.find('.//def:coordinates', ns)  
            #按照路的名称，将路的航点分别筛选储存（苏雨）     
            if not coord is None:    
                coord = coord.text.strip()
                coord = re.findall(regex, coord)                                
            #print(count)
            if name == list[count]: 
                #print(name)                
                
                
                for (long, lat, heig) in coord:
                    if i.find('.//def:LineString', ns):            
                        out_pat.write(f'{name},{long},{lat},')
                        #print(long, lat, heig)
                        
                        kmllist.append(heig)
                        kmllist.append(long)
                        kmllist.append(lat)
                       
                       
                        
                        
 
                        
                        
                        #下面计算这个道路的风险值，先以旋翼飞行器为例（苏雨）
                        m = 1.4
                        v_cruise = 6.5
                        g = 9.8
                        row = 1.29
                        CD = 0.45
                        A = 0.02
                        H = 50                                               
                        Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))
                        vcar = maxspeedlist[count]
                        Rroad = wroad*rowcar*vcar*vcar*Ek
                        Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*H)/(2*m)))
                        Rroadstr = str(Rroad)
                        Lthreatstr = str(Lthreat)


                        out_pat.write(Rroadstr)
                        out_pat.write(',')
                        out_pat.write(Lthreatstr)                        
                        out_pat.write(f'\n')
                        #print(count)
                        






























        #从这里插入kml道路航点数据（苏雨）
        f.write("\t<Placemark>\n")
        
        
        
        
        
        
        
        #这里需要将列表里的数据提取并转换（苏雨）
        coordnum = 0
        coordinates = ''
        while coordnum < len(kmllist) - 1:
            #print (kmllist[coordnum])
            coordnum = coordnum + 1
            coordinates = coordinates + str(kmllist[coordnum])
            if coordnum < len(kmllist) - 1:
                coordinates = coordinates + ','
            
            
            
            
        print(coordinates)
        print('\n')
        print('\n')        
        
        
        
        
        
        


        f.write("\t\t<LineString>\n")
        f.write('\t\t\t<coordinates>\n')
        f.write('\t\t\t\t'+ coordinates + '\n')
        f.write('\t\t\t</coordinates>\n')
        f.write("\t\t</LineString>\n")
        f.write("\t</Placemark>\n")                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                       
                        
                        
                                                                                                         
        count = count + 1 


f.write("</Document>\n")
f.write("</kml>\n")
f.close()

