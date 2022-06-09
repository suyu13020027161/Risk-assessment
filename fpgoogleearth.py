#苏雨的飞行计划csv转kml程序
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

#创建包含风险的kml文件头文件（苏雨）
#先写头文件（苏雨） 
f = open("flightplan.kml", "w")
head1 = '<?xml version="1.0" encoding="UTF-8"?>'
f.write(head1)
f.write('\n')
head2 = '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
f.write(head2)
f.write('\n')
f.write("<Document>\n")
f.write("\t<name>" + 'flightplan.kml' + "</name>\n")


#这里需要将列表里的数据提取并转换（苏雨）
plannum = 0
hg = 0    
while plannum < len(fllon):
    f.write("\t<Placemark>\n")
    f.write("\t\t<name>" + 'flight_'+str(plannum + 1) + "</name>\n")
    f.write("\t\t<LineString>\n")
    f.write("\t\t\t<coordinates>\n")
    coordinates = ''
    coordnum = 0 
    while coordnum < len(fllon[plannum]):
        coordinates = coordinates + str(fllon[plannum][coordnum])
        coordinates = coordinates + ','
        coordinates = coordinates + str(fllat[plannum][coordnum])
        coordinates = coordinates + ','        
        coordinates = coordinates + '0'
        if coordnum < (len(fllon[plannum]) - 1):
            coordinates = coordinates + ','
        coordnum = coordnum + 1   
    f.write('\t\t\t\t'+ coordinates + '\n')
    f.write('\t\t\t</coordinates>\n')
    f.write("\t\t</LineString>\n")            
    plannum = plannum + 1
    f.write("\t</Placemark>\n") 
f.write("</Document>\n")
f.write("</kml>\n")
f.close() 






















