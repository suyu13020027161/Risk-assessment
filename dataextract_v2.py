#这个程序是用来将txt文件里的航路坐标点提取出来按道路名称存入数组（苏雨）
import numpy as np
with open('output_paths.txt') as f:
    line=f.readline()
    #先建个数组把txt文件里面的数据读出来（苏雨）
    data_array=[]
    #再建个数组把同一街道名称的道路航点坐标合并存储（苏雨）
    processed_array=[]            
    #定义临时列表存放一个道路的数据（苏雨）
    temp_list=[]    
    while line:
        num=list(map(str,line.split(',')))
        data_array.append(num)
        line=f.readline()
    data_array=np.array(data_array)
    #下面开始处理数组的数据（苏雨）
    #txt第一行是头文件，不处理（苏雨）
    i = 1
    #逐行判断道路同名，若同名则归纳到一行里面（苏雨）
    samename = ''
    while i < len(data_array):         
        #如果是重名的则归纳到一行里（苏雨）
        if data_array [i][0] == samename:                                                
            #重名的话道路名字不要（苏雨）                        
            j = 1
            while j <= 2:
                temp_list.append(data_array [i][j])
                j = j + 1                
            temp_list.append('0')                                                                                  
            samename = data_array [i][0]              
        #如果没重名，则新建临时列表存储数据（苏雨）
        else:
            temp_list=[]                        
            temp_list.append(data_array [i][0]) 
            j = 1
            while j <= 2:
                temp_list.append(data_array [i][j])
                j = j + 1                
            temp_list.append('0')                                                 
            samename = data_array [i][0]            
            processed_array.append(temp_list)                           
        i = i + 1        
print(processed_array)
