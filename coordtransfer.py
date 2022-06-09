#苏雨的航点坐标转换程序
#将两个航点连线叠加风险距离变成矩形，并计算出矩形四个顶点的坐标
# -*- coding: utf-8 -*-

wpx1 = 0
wpy1 = 0
wpx2 = 2
wpy2 = 2
Lthreat = 2
H = (Lthreat*(wpx2-wpx1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5)         
L = (Lthreat*(wpy2-wpy1))/(((wpx2-wpx1)**2+(wpy2-wpy1)**2)** 0.5)    
print(H)    
print(L)
print(2**0.5)
#矩形顺时针从左上顶点开始（苏雨）
x1 = wpx1 - L
y1 = wpy1 + H
x2 = wpx2 - L
y2 = wpy2 + H
x3 = wpx2 + L
y3 = wpy2 - H
x4 = wpx1 + L
y4 = wpy1 - H

print((x1,y1),(x2,y2),(x3,y3),(x4,y4))
