#coding=utf-8
import  xml.dom.minidom

#打开xml文档
dom = xml.dom.minidom.parse('test.kml')

#得到文档元素对象
root = dom.documentElement

cc=dom.getElementsByTagName('coordinates')
c1=cc[0]
print (c1.firstChild.data)

c2=cc[1]
print (c2.firstChild.data)


