# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import re

def main():
    #要读取的kml文件名（苏雨）
    tree = ET.parse('test2.kml')
    root = tree.getroot()
    
    namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
    ns = {'def': namespace}
    
    coord_ex = '(-?\d+\.\d+),'
    heig_ex = '(\d+)'
    regex = coord_ex + coord_ex + heig_ex
    
    #创建输出头文件，如果存在就覆盖掉（苏雨）
    with open('output_paths.txt','w') as out_pat:
      
        #添加说明头文件（苏雨）
        out_pat.write('Pin Name,Pin_#,Latitude,Longitude,Height\n')


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
          






 
 
 
 
 
 
 
 
 





            #按照路的名称，将路的航点分别筛选储存（苏雨）
            
            
            
            
            
            
            
            if not coord is None:    
                coord = coord.text.strip()
                coord = re.findall(regex, coord)
            for (long, lat, heig) in coord:
                if i.find('.//def:LineString', ns): 
                    
                    
                    
                    lastname = f'{name}'
                    print(lastname)
                    
                    
                    
                                       
                    if i.find('def:name', ns).text == list[count]:
                        out_pat.write(f'{name},{lat},{long},{heig}\n')
            
            
            #用来解决列表越界的问题（苏雨）
            if count < len(list) - 1:
                count = count + 1
            
            
            
            



 
 
 
 
 
 








 
     
'''
        #按照路的名称，将路的航点分别筛选储存（苏雨）
        num = 0
        if not coord is None:    
            coord = coord.text.strip()
            coord = re.findall(regex, coord)          
        while num < len(list):    
            pin = 0
            for (long, lat, heig) in coord:
                pin = pin + 1
                #这里用来输出道路的信息（苏雨）    
                if i.find('.//def:LineString', ns):              
                    #根据不同道路名称来筛选道路（苏雨）
                    print(num)
                    if i.find('def:name', ns).text == list[num]:
                        out_pat.write(f'{name},{lat},{long},{heig}\n') 
            num = num + 1 
'''


















'''              
          if not coord is None:
              coord = coord.text.strip()
              coord = re.findall(regex, coord)
            # Save data
              pin = 0
              for (long, lat, heig) in coord:
                  pin += 1
                  if i.find('.//def:Point', ns):
                      out_pin.write(f'{name},{lat},{long},{heig}\n')
                  #这里用来输出道路的信息（苏雨）    
                  elif i.find('.//def:LineString', ns):                                   
                      
                      #根据不同道路名称来筛选道路（苏雨）
                      if i.find('def:name', ns).text == 'Kingston Roundabout':
                          out_pat.write(f'{name},{lat},{long},{heig}\n')                         
                                                                                                       
                  elif i.find('.//def:Polygon', ns):   
                      out_pol.write(f'{name},pin_{pin},{lat},{long},{heig}\n')
'''               



    










if __name__ == '__main__':
    main()
