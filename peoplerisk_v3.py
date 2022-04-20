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

#print(namelist)
#print(len(namelist))
#######################################################################################################################################################################################################




#######################################################################################################################################################################################################
#下面直接计算风险值和风险距离（苏雨）
Rroadlist = []
num = 0

#以旋翼飞行器为例（苏雨）
m = 1.4
v_cruise = 6.5
g = 9.8
row = 1.29
CD = 0.45
A = 0.02
H = 50

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
#提取所有区域信息，按照文件夹分别存入数组（苏雨）
dom=minidom.parse("/home/suyu/test/area2.kml") 
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
#print(areadata) 
#######################################################################################################################################################################################################




#######################################################################################################################################################################################################
#将风偏插入数组（苏雨）
#print(areadata[0][0][0])
#print(areadata[0][0])
#这里加入风偏（苏雨）
ARC=6371.393*1000
#定义插入风偏后的数组（苏雨）
coordlist = []
arealist = []
windarea = []
foldernum = 0
while foldernum < len(areadata):
    areanum = 0
    arealist = []
    while areanum < len(areadata[foldernum]):
        latnum = 0
        lonnum = 1  
        heignum = 2
        coordlist = []
        while heignum < len(areadata[foldernum][areanum]):
            #print(areadata[foldernum][areanum][latnum])
            #print(areadata[foldernum][areanum][lonnum])
            fllat = float(areadata[foldernum][areanum][latnum])
            fllong = float(areadata[foldernum][areanum][lonnum])
            flheig = float(areadata[foldernum][areanum][heignum])
            #计算旋翼飞行器的风偏量（苏雨）                                 
            fllat2 = fllat + W_distance_rotor * math.sin(wind_direction) / (ARC * math.cos(fllong) * 2 * pi / 360)
            fllong2 = fllong + W_distance_rotor * math.cos(wind_direction) / (ARC * 2 * pi / 360)
            coordlist.append(fllat2)
            coordlist.append(fllong2)
            coordlist.append(flheig)            
            latnum = latnum + 3
            lonnum = lonnum + 3
            heignum = heignum + 3
        arealist.append(coordlist)
        areanum = areanum + 1
    windarea.append(arealist)    
    foldernum = foldernum + 1
#print('\n')
#print(areadata)
#print('\n')
#print(windarea)
#######################################################################################################################################################################################################




#######################################################################################################################################################################################################
#创建包含风险的kml文件头文件（苏雨）
#先写头文件（苏雨） 
f = open("peoplerisk.kml", "w")
head1 = '<?xml version="1.0" encoding="UTF-8"?>'
f.write(head1)
f.write('\n')
head2 = '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
f.write(head2)
f.write('\n')
f.write("<Document>\n")
f.write("\t<name>" + 'peoplerisk.kml' + "</name>\n")

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


    
    f.write('\t'+'<'+Style_id1+'>'+'\n')
    f.write('\t\t'+'<LineStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t'+'</LineStyle>\n')
    f.write('\t\t'+'<PolyStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t'+'</PolyStyle>\n')    
    f.write('\t'+'</Style>'+'\n')
    
    f.write('\t'+'<'+Style_id2+'>'+'\n')
    f.write('\t\t'+'<IconStyle>\n')
    f.write('\t\t\t'+'<scale>'+'1.2'+'</scale>\n')
    f.write('\t\t'+'</IconStyle>\n')
    f.write('\t\t'+'<LineStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t'+'</LineStyle>\n')
    f.write('\t\t'+'<PolyStyle>\n')
    f.write('\t\t\t'+'<color>'+color1+'</color>\n')
    f.write('\t\t'+'</PolyStyle>\n')     
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




foldernum = 0
while foldernum < len(windarea):
    f.write("\t<Folder>\n")
    f.write('\t\t<name>'+ namelist[foldernum] + '</name>' + '\n')   
    areanum = 0
    while areanum < len(windarea[foldernum]):
        f.write("\t\t<Placemark>\n")    
        f.write('\t\t\t<name>'+ namelist[foldernum]+' '+ str(areanum+1) + '</name>' + '\n') 
        f.write('\t\t\t<styleUrl>'+ '#m_ylw-pushpin1' + '</styleUrl>' + '\n')  
        f.write('\t\t\t<Polygon>\n')        
        f.write('\t\t\t\t<tessellate>'+ '1' + '</tessellate>' + '\n') 
        f.write('\t\t\t\t<outerBoundaryIs>\n') 
        f.write('\t\t\t\t\t<LinearRing>\n')
        #这里把列表数据提取为字符串（苏雨）
        coordnum = 0  
        coordinates = ''
        while coordnum < len(windarea[foldernum][areanum]):           
            coordinates = coordinates + str(windarea[foldernum][areanum][coordnum])                    
            if coordnum < len(windarea[foldernum][areanum])-1:
                coordinates = coordinates + ','                 
            coordnum = coordnum + 1         
        f.write('\t\t\t\t\t\t<coordinates>\n')                
        f.write('\t\t\t\t\t\t\t'+ coordinates + '\n')                                      
        f.write('\t\t\t\t\t\t</coordinates>\n')        
        f.write('\t\t\t\t\t</LinearRing>\n')                 
        f.write('\t\t\t\t</outerBoundaryIs>\n')      
        f.write('\t\t\t</Polygon>\n')        
        f.write("\t\t</Placemark>\n")        
        
        
        
        
        
              
        areanum = areanum + 1
    
    
    
    
    f.write("\t</Folder>\n")
    foldernum = foldernum + 1

































   
f.write("</Document>\n")
f.write("</kml>\n")
f.close()    



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
