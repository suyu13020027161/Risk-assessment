#这个程序是用来创建包含风险的kml文件（苏雨）




#先写头文件（苏雨） 
f = open("KML.kml", "w")
head1 = '<?xml version="1.0" encoding="UTF-8"?>'
f.write(head1)
f.write('\n')
head2 = '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
f.write(head2)
f.write('\n')
f.write("<Document>\n")
f.write("\t<name>" + 'KML.kml' + "</name>\n")








dataname = '<Data name="maxspeed">'
name = 'Kingston Roundabout'
maxspeed = '60 mph'
coordinates = '-0.6034068,52.0257166,0 -0.6033807,52.02565739999999,0 -0.6033751000000001,52.0255961,0 -0.6033981,52.02551920000001,0 -0.6034533,52.02544869999999,0 -0.6035367,52.0253897,0 -0.6036424,52.0253463,0 -0.6037842,52.0253194,0 -0.6039325,52.0253205,0 -0.6040731,52.0253495,0 -0.6041413,52.025376,0 -0.6042012,52.02540920000001,0 -0.6042816,52.0254807,0 -0.6043245,52.0255635,0 -0.6043262,52.0256504,0 -0.6042864999999999,52.0257338,0 -0.6042433,52.02578,0 -0.6041714,52.02582960000001,0 -0.6040833,52.0258681,0 -0.6039833999999999,52.0258934,0 -0.6038333,52.0259044,0 -0.6036852,52.02588599999999,0 -0.6035539,52.0258401,0 -0.6034523000000001,52.0257713,0 -0.6034068,52.0257166,0'

f.write("\t<Placemark>\n")
f.write("\t\t<name>" + name + "</name>\n")
f.write("\t\t<ExtendedData>\n")
f.write('\t\t\t'+ dataname + '\n')
f.write('\t\t\t\t<value>'+ maxspeed + '</value>\n')
f.write('\t\t\t</Data>\n')
f.write("\t\t</ExtendedData>\n")
f.write("\t\t<LineString>\n")
f.write('\t\t\t<coordinates>\n')
f.write('\t\t\t\t'+ coordinates + '\n')
f.write('\t\t\t</coordinates>\n')
f.write("\t\t</LineString>\n")
f.write("\t</Placemark>\n")







f.write("</Document>\n")
f.write("</kml>\n")
f.close()
