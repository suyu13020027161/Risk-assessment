from xml.dom import minidom
#1.导入模块
dom=minidom.parse("/home/suyu/test/test2.kml") #2.加载xml文件
root = dom.documentElement
data = root.getElementsByTagName('Data')
for i in range(len(data)):
    if data[i].getAttribute("name") == 'maxspeed':
        #请注意用下列语句来选择第几个子节点（苏雨）
        #print(data[i].childNodes[1])
        maxspeed = data[i].childNodes[1]
        value = maxspeed.childNodes[0]
        print(value.data)
        
        
        
        























