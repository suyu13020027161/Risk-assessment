import numpy as np
with open('output_paths.txt') as f:
    line=f.readline()
    #先建个数组把txt文件里面的数据读出来（苏雨）
    data_array=[]
    #再建个数组把同一街道名称的道路航点坐标合并存储（苏雨）
    processed_array=[]
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
                processed_array.append(data_array [i][j])
                j = j + 1
                
            processed_array.append('0') 
                 
                
                
                
                
            samename = data_array [i][0]      
        else:
            processed_array.append(data_array [i][0]) 
            j = 1
            while j <= 2:
                processed_array.append(data_array [i][j])
                j = j + 1
                
            processed_array.append('0')             
            
            
            
            samename = data_array [i][0]            
            
            
               
        i = i + 1









print(processed_array)
