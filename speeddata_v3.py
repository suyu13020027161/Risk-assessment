from xml.dom import minidom
#1.导入模块
dom=minidom.parse("/home/suyu/test/test2.kml") #2.加载xml文件
root = dom.documentElement
Placemark = root.getElementsByTagName('Placemark')
#判断道路同名，若同名则归纳到一行里面（苏雨）
samename = []

for i in range(len(Placemark)):
    n = Placemark[i].childNodes[1]
    na = n.firstChild
    name = na.data
    print (name)
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
            print(maxspeedvalue)
        
        
        
        
        
    #print(len(ExtendedData.childNodes))
    
    
    
    
    #第一个名字直接插入samename（苏雨）
    if len(samename) == 0:
        samename.append(name)
        #print(maxspeed.childNodes)
    
    
    
    
    
    
    
    
    
    
    
    
    count = 0
    #找道路名称数组里有没有重复的（苏雨）
    while count < len(samename):
        if samename[count] == name:
            break
        else:
            if count == len(samename) - 1:                
                samename.append(name)
                #print(name)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        count = count + 1
            
#print (samename)    


    













'''
for i in range(len(data)):
    if data[i].getAttribute("name") == 'maxspeed':
        #请注意用下列语句来选择第几个子节点（苏雨）
        #print(data[i].childNodes[1])
        maxspeed = data[i].childNodes[1]
        value = maxspeed.childNodes[0]
        print(value.data)
'''        
        
        
        























