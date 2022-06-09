#苏雨的判断线段是否相交程序

class Point:
    def get(self,text,x,y):
        self.text=text
        self.x = x
        self.y = y       
             

def liesOnSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
  
def checkOrientation(p, q, r):      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0

def checkIntersection(p1,q1,p2,q2):
    global intersectionresult
    global proper
    o1 = checkOrientation(p1, q1, p2)
    o2 = checkOrientation(p1, q1, q2)
    o3 = checkOrientation(p2, q2, p1)
    o4 = checkOrientation(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        if(o1==0 or o2==0 or o3==0 or o4==0):
            intersectionresult=True
            proper=False
        else:
            intersectionresult=True
            proper=True
        return True
    if ((o1 == 0) and liesOnSegment(p1, p2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o2 == 0) and liesOnSegment(p1, q2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o3 == 0) and liesOnSegment(p2, p1, q2)):
        intersectionresult=True
        proper=False
        return True
    if ((o4 == 0) and liesOnSegment(p2, q1, q2)):
        intersectionresult=True
        proper=False
        return True

    intersectionresult=False
    proper=None
    return False


p1=Point()
q1=Point()
p2=Point()
q2=Point()
#请注意，p1,q1是一条线；p2,q2是另一条线（苏雨）
pointlist=[p1,q1,p2,q2]
#请将需要判断的上述四个顶点xy坐标按顺序存在下面的数组里（苏雨）
colist=[0,0,2,2,0,2,2,0]

i = 0
for p in pointlist:
    pointname=[key for key,value in locals().items() if value==p]
    p.get(str(pointname[0]),colist[i],colist[i+1])
    i = i+2

checkIntersection(p1, q1, p2, q2)


if(intersectionresult==True):
    print("YES!")
else:
    print("NO!")

