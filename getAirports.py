lib_path = 'C:/Users/user/qgis/CaptureAirportImageWithQgis'
airports_json_url = "https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json"
airports_data_save_path = "c:/temp/airports_data.txt"
groundWidth = 10000    # ground width(m)
groundHeight = 10000   # ground height(m)
outputWidth = 500      # image width(px)   (value range between 500 and 3000)
outputHeight = 500     # image height(px)  (value range between 500 and 3000)
image_save_path = "c:/temp/"
image_save_type = "jpg"
#dpi = 300

import sys
sys.path.append(lib_path)

from qgis_tools import *


import urllib
import json

print "Download airport information..."
urllib.urlretrieve(airports_json_url, airports_data_save_path)
print "Download completed!\n\n"

print "Prepare airport information..."
f = open(airports_data_save_path, 'r')
jdata = f.read()
f.close()
data = json.loads(jdata)

inx = 0
pts=[]
xs = []
ys = []
names = []
for j in data:
    inx += 1
    xs += [float( j["lon"] )]
    ys += [float( j["lat"] )]
    names += [j["name"]]        
    if inx >= 3:
        break

pts = [xs,ys]
print "Prepare completed!\n\n"

curPtInx = 0
def doNext():
    global pts, curPtInx, groundWidth, groundHeight
    
    if curPtInx < len(pts[0]):
        print "Zoom to " + names[curPtInx]
        cx = pts[0][curPtInx]
        cy = pts[1][curPtInx]
        cx, cy = coordinateTransform( cx, cy, 4326, 3857)
        zoom2area( cx, cy, groundWidth, groundHeight)
        curPtInx += 1

    
def onMapLoad():
    global pts, curPtInx, outputWidth, outputHeight, cx, cy, dpi, names
    print "Capture image of " + names[curPtInx-1] + "(" + str(curPtInx-1) + ")"
    captureImage2(  image_save_path + str(curPtInx-1) 
                        + "_"+ names[curPtInx-1],
                    image_save_type,
                    outputWidth,   # px
                    outputHeight)  # px
    print "Capture completed!\n"
    if curPtInx >= len(pts[0]):
        iface.mapCanvas().mapCanvasRefreshed.disconnect(onMapLoad)
        print("All Done!! :)")
    else:
        doNext()

print "Start capture process...\n"
iface.mapCanvas().mapCanvasRefreshed.connect(onMapLoad)
doNext()