#苏雨的判断线段和多边形相交的程序
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry
import descartes


clip_poly = shapely.geometry.Polygon([[0, 0], [1, 2], [1, 3], [2, 4], [3, 3], [2, 2], [3, 1], [2, 0]])


line = shapely.geometry.LineString([[1, 0.5], [2, 1]])


print ('Blue line intersects clipped shape:', line.intersects(clip_poly))


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(*np.array(line).T, color='blue', linewidth=0.5, solid_capstyle='round')
ax.add_patch(descartes.PolygonPatch(clip_poly, fc='blue', alpha=0.5))
ax.axis('equal')

plt.show()
