# -*- coding: utf-8 -*-
from xml.dom import minidom
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re
import math
from numpy import sqrt
pi = math.pi



#######################################################################################################################################################################################################
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

#print(namelist)
#print(len(namelist))
#######################################################################################################################################################################################################




#######################################################################################################################################################################################################
#创建列表存储最大速度（苏雨）
maxspeedlist = []
#提取道路限速（苏雨）
dom=minidom.parse("/home/suyu/test/test2.kml") 
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

#print(maxspeedlist)
#print(len(maxspeedlist))    
#######################################################################################################################################################################################################






#######################################################################################################################################################################################################
#下面直接计算风险值和风险距离（苏雨）
Rroadlist = []
num = 0
while num < len(maxspeedlist):
    #以旋翼飞行器为例（苏雨）
    m = 1.4
    v_cruise = 6.5
    g = 9.8
    row = 1.29
    CD = 0.45
    A = 0.02
    H = 50
    #道路风险权重（苏雨）
    wroad = 0.3
    #道路车辆密度，初步定义为辆每平方米（苏雨）
    rowcar = 0.2    
    vcar = maxspeedlist[num]                                                       
    Ek = (m*v_cruise**2)/2 + ((m**2*g)/(row*CD*A))*(1-math.exp(-(row*CD*A*H)/m))
    vcar = maxspeedlist[num]
    Rroad = wroad*rowcar*vcar*vcar*Ek
    Rroadlist.append(Rroad)
    Lthreat = v_cruise*sqrt((2*m)/(row*CD*A*g))*math.acosh(math.exp((row*CD*A*H)/(2*m)))
    Rroadstr = str(Rroad)
    Lthreatstr = str(Lthreat)    
    num = num + 1
    

#print(Rroadlist)
#print(Lthreat)
#######################################################################################################################################################################################################





#######################################################################################################################################################################################################
#下面计算风偏，单位是弧度（苏雨）
#定义风向角，正北是0°，正东是90°，正南是180°，正西是270°
wind_direction = 3*pi/4
#定义风速，单位km/h（苏雨）
wind_speed = 100
#转换为m/s（苏雨）
wind_speed_ms = wind_speed/3.6
#定义飞行器水平迎风面积（苏雨）
A_horizontal = 0.15


#计算旋翼飞行器的风偏（苏雨）
W_distance_rotor = ((wind_speed_ms**2*A_horizontal)/(2*A*g))*(math.acosh(math.exp((row*CD*A*H)/(2*m))))**2
#print(W_distance_rotor)




#######################################################################################################################################################################################################


















#######################################################################################################################################################################################################
#提取道路数据存入二维列表（苏雨）
tree = ET.parse('test2.kml')
root = tree.getroot()   
namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
ns = {'def': namespace}



#注意这里要创建二维列表来存储道路数据（苏雨）
kmllist_v2 = [[] for i in range(len(Rroadlist))]
road_number = 0
with open('path_coordinates.txt','w') as out_pat:
    shu = 0
          
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
                out_pat.write(f'{name},{lat},{long},{heig}\n')
                
                
                
                #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!这里加入风偏（苏雨）
                ARC=6371.393*1000
                fllong = float(long)
                fllat = float(lat)
                #计算旋翼飞行器的风偏量（苏雨）
                fllong2 = fllong + W_distance_rotor * math.sin(wind_direction) / (ARC * math.cos(fllat) * 2 * pi / 360)
                fllat2 = fllat + W_distance_rotor * math.cos(wind_direction) / (ARC * 2 * pi / 360)
                long2 = str(fllong2)
                lat2 = str(fllat2)                
                kmllist_v2[road_number].append(long2)
                kmllist_v2[road_number].append(lat2) 
        #print(kmllist)              
        #print('\n')
        #print('\n') 
        #kmllist_v2[road_number].append(kmllist)
        #print(road_number)
        road_number = road_number + 1
#print(kmllist_v2)
#######################################################################################################################################################################################################






#######################################################################################################################################################################################################
#创建包含风险的kml文件头文件（苏雨）
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

#创建颜色列表（苏雨）
color_list = ['ff2a2ab3','ff2a4db3','ff2a61b3','ff2a6ab3','ff2a73b3','f2a86b3','ff2a98b3','ff2aaab3','ff2ab3ac','ff2ab396','ff2ab383','ff2ab368','ff2ab356','ff2ab33f','ff2ab32a']

color_count = 0
while color_count < len(color_list):
    #print(color_count)
    color_countstr = str(color_count)
    Style_id1 = 'Style id="default' + color_countstr + '"'
    Style_id2 = 'Style id="hl' + color_countstr + '"'
    Style_id3 = 'StyleMap id="type' + color_countstr + '"'
    styleUrl1 = '#default' + color_countstr
    styleUrl2 = '#hl' + color_countstr
    styleUrl3 = '#type' + color_countstr
    color1 = color_list[color_count]
    #！！！这里有待斟酌（苏雨）
    width1 = str(Lthreat+color_count*10+10)

    
    f.write('\t'+'<'+Style_id1+'>'+'\n')
    f.write('\t\t'+'<LineStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t\t'+'<gx:physicalWidth>'+width1+'</gx:physicalWidth>\n')
    f.write('\t\t'+'</LineStyle>\n')
    f.write('\t'+'</Style>'+'\n')
    
    f.write('\t'+'<'+Style_id2+'>'+'\n')
    f.write('\t\t'+'<IconStyle>\n')
    f.write('\t\t\t'+'<scale>'+'1.2'+'</scale>\n')
    f.write('\t\t'+'</IconStyle>\n')
    f.write('\t\t'+'<LineStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t\t'+'<width>'+width1+'</width>\n')
    f.write('\t\t'+'</LineStyle>\n')
    f.write('\t'+'</Style>'+'\n')    

    f.write('\t'+'<'+Style_id3+'>'+'\n')
    f.write('\t\t'+'<Pair>\n')
    f.write('\t\t\t'+'<key>'+'normal'+'</key>\n')
    f.write('\t\t\t'+'<styleUrl>'+styleUrl1+'</styleUrl>\n')
    f.write('\t\t'+'</Pair>\n')
    f.write('\t\t'+'<Pair>\n')
    f.write('\t\t\t'+'<key>'+'highlight'+'</key>\n')
    f.write('\t\t\t'+'<styleUrl>'+styleUrl2+'</styleUrl>\n')
    f.write('\t\t'+'</Pair>\n')
    f.write('\t'+'</StyleMap>'+'\n')
    
    '''
    print(Style_id1)
    print(Style_id2)
    print(Style_id3)
    print(styleUrl1)
    print(styleUrl2)
    print(styleUrl3)
    '''    
            
    color_count = color_count + 1

#######################################################################################################################################################################################################








#######################################################################################################################################################################################################
#开始绘制道路风险分布图（苏雨）
'''
风险值：
70    173792.2097411448
60    127684.07246288186
40    56748.47665016972
30    31921.018115720464
20    14187.11916254243
'''


#print(Rroadlist)
roadnum = 0
#print(kmllist_v2[0])
while roadnum < (len(kmllist_v2)):
    #按照不同道路风险绘制风险分布图（苏雨）
    if Rroadlist[roadnum] > 170000:
        color_count = len(color_list) - 1
    elif Rroadlist[roadnum] > 100000:
        color_count = len(color_list) - 5 
    elif Rroadlist[roadnum] > 50000:
        color_count = len(color_list) - 7               
    elif Rroadlist[roadnum] > 30000:
        color_count = len(color_list) - 9 
    elif Rroadlist[roadnum] > 10000:
        color_count = len(color_list) - 11 



     
    while color_count >= 0:
        color_countstr = str(color_count)
        orderstr = str(14 - color_count)
        typenum = '#type' +  orderstr
        #print(typenum)    
        #这里需要将列表里的数据提取并转换（苏雨）
        coordnum = 0
        hg = 0    
        coordinates = ''
        while coordnum < len(kmllist_v2[roadnum]):             
            if hg == 2:
                coordinates = coordinates + str(14-color_count)
                hg = 0   
            else:
                coordinates = coordinates + str(kmllist_v2[roadnum][coordnum])
                hg = hg + 1
                coordnum = coordnum + 1    
                    
            if coordnum < len(kmllist_v2):
                coordinates = coordinates + ','                 
        coordinates = coordinates + str(14-color_count)                                   
        #print(coordinates)
        f.write("\t<Placemark>\n")
        f.write('\t\t<name>'+ namelist[roadnum] + '</name>' + '\n')
        f.write('\t\t<styleUrl>'+ typenum + '</styleUrl>' + '\n')
        f.write("\t\t<LineString>\n")             
        #高度参数设置（苏雨）
        f.write('\t\t\t<altitudeMode>'+'relativeToGround'+'</altitudeMode>\n')             
        #请注意，这里设置道路上下优先级（苏雨）
        f.write('\t\t\t'+'<gx:drawOrder>'+color_countstr+'</gx:drawOrder>\n')
        f.write('\t\t\t<coordinates>\n')                
        f.write('\t\t\t\t'+ coordinates + '\n')                                      
        f.write('\t\t\t</coordinates>\n')
        f.write("\t\t</LineString>\n")
        f.write("\t</Placemark>\n")                      
        color_count = color_count - 1                    
    roadnum = roadnum + 1
   
f.write("</Document>\n")
f.write("</kml>\n")
f.close()    
#######################################################################################################################################################################################################







  

        

#######################################################################################################################################################################################################
'''
#道路风险颜色代码对照表，风险从高到低（苏雨）
#b32a2a    ff2a2ab3      
#b3362a    ff2a36b3
#b34d2a    ff2a4db3
#b3612a    ff2a61b3
#b36a2a    ff2a6ab3
#b3732a    ff2a73b3
#b3862a    ff2a86b3
#b3982a    ff2a98b3
#b3aa2a    ff2aaab3
#acb32a    ff2ab3ac
#96b32a    ff2ab396
#83b32a    ff2ab383
#68b32a    ff2ab368
#56b32a    ff2ab356
#3fb32a    ff2ab33f
#2ab32a    ff2ab32a
'''
