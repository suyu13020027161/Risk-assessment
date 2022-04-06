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
    #print (name)
    
    
    
    #第一个名字直接插入samename（苏雨）
    if len(samename) == 0:
        samename.append(name)
        print(name)
    
    
    
    
    
    
    
    
    
    
    
    
    count = 0
    #找道路名称数组里有没有重复的（苏雨）
    while count < len(samename):
        if samename[count] == name:
            break
        else:
            if count == len(samename) - 1:                
                samename.append(name)
                print(name)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
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
        
        
        























