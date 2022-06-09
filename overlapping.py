#苏雨的飞多边形相交判断程序
import numpy as np
import time
from shapely.geometry import Polygon  # 多边形
import scipy.io as io

def Cal_area_2poly(data1,data2):
    poly1 = Polygon(data1).convex_hull      # Polygon：多边形对象
    poly2 = Polygon(data2).convex_hull

    if not poly1.intersects(poly2):
        inter_area = 0  # 如果两四边形不相交
    else:
        inter_area = poly1.intersection(poly2).area  # 相交面积
    return inter_area
    
data1 = [[0,0],[0,2],[2,0],[2,2],[1,4]]  # 带比较的第一个物体的顶点坐标
data2 = [[0,0],[1,2],[2,0]]   #待比较的第二个物体的顶点坐标
area = Cal_area_2poly(data1,data2)
print(area)
