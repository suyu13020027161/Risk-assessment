#苏雨的风险评估地图绘制测试程序
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection



#道路航点数据（苏雨）
college_rd_y=[52.073424,52.073918,52.074418,52.074653,52.074820,52.074874,52.074911,52.075220,52.075251,52.075275,52.075932,52.077582,52.078291,52.079361,52.084624]
college_rd_x=[-0.630392,-0.630169,-0.629850,-0.629625,-0.629241,-0.628610,-0.628123,-0.626163,-0.624704,-0.623595,-0.621726,-0.618613,-0.617856,-0.617205,-0.614204]

folly_ln_y=[52.073424,52.073434,52.073395,52.073410,52.073599,52.073100,52.071785,52.068287,52.067776,52.067384,52.066988,52.066603,52.065775,52.065529]
folly_ln_x=[-0.630392,-0.632736,-0.635036,-0.635620,-0.638084,-0.638309,-0.638412,-0.640945,-0.641284,-0.641779,-0.642491,-0.643500,-0.647808,-0.648387]

university_way_y=[52.073424,52.073164,52.072775,52.072283,52.071949,52.071650,52.071323,52.070582,52.070254,52.067867,52.067607,52.067562,52.067470,52.067355,52.067267,52.067278,52.067353,52.067510,52.067607,52.067562,52.067470,52.067355,52.067267,52.067278,52.067353,52.067364,52.067337,52.067256,52.067161,52.067028,52.066984,52.067089,52.067243,52.067328,52.067256,52.067161,52.067028,52.066718,52.064937]
university_way_x=[-0.630392,-0.630435,-0.630502,-0.630517,-0.630555,-0.630641,-0.630768,-0.631085,-0.631178,-0.631538,-0.631543,-0.631320,-0.631229,-0.631262,-0.631433,-0.631613,-0.631760,-0.631748,-0.631543,-0.631320,-0.631229,-0.631262,-0.631433,-0.631613,-0.631760,-0.632163,-0.634113,-0.634404,-0.634357,-0.634410,-0.634702,-0.634895,-0.634874,-0.634684,-0.634404,-0.634357,-0.634410,-0.634417,-0.634164]

#注意下面两个参数后边将会随着道路不同而变化，是反应风险值的参数（苏雨）
#定义渐变色分辨率（苏雨）
res=100
#定义渐变色宽度（苏雨）
width=10


i=0
while (i < res):
   plt.plot(college_rd_x,college_rd_y,linestyle='-',linewidth=2*width-i/(res/width),color=[i/res, i/res, 1-i/res])
   i=i+1
i=0
while (i < res):
   plt.plot(college_rd_x,college_rd_y,linestyle='-',linewidth=width-i/(res/width),color=[1, 1-i/res, 0])
   i=i+1



i=0
while (i < res):
   plt.plot(university_way_x,university_way_y,linestyle='-',linewidth=2*width-i/(res/width),color=[i/res, i/res, 1-i/res])
   i=i+1
i=0
while (i < res):
   plt.plot(university_way_x,university_way_y,linestyle='-',linewidth=width-i/(res/width),color=[1, 1-i/res, 0])
   i=i+1


plt.plot(folly_ln_x,folly_ln_y,linestyle='-',linewidth=1,color=[1.0, 0.5, 0.25])
plt.plot(university_way_x,university_way_y,linestyle='-',linewidth=1,color=[1.0, 0.5, 0.25])


#绘制连线图并显示（苏雨）
#plt.scatter(college_rd_x,college_rd_y)
#plt.plot(college_rd_x,college_rd_y,linestyle='-',linewidth=10,color=[1, 0, 0])
#plt.plot(college_rd_x,college_rd_y,linestyle='-',linewidth=5,color=[1.0, 0.5, 0.25])





plt.show()

