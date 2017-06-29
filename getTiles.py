lib_path = 'C:/Users/user/qgis/qgis_tools'

groundWidth = 1000    # ground width(m)
groundHeight = 1000   # ground height(m)
outputWidth = 500      # image width(px)   (value range between 500 and 3000)
outputHeight = 500     # image height(px)  (value range between 500 and 3000)
image_save_path = "c:/temp/"
image_save_type = "jpg"

startX = 13420000
endX = startX + 3 * groundWidth
startY = 2780000
endY = startY + 3 * groundHeight

import sys
sys.path.append(lib_path)

from qgis_tools import *

inx = 0
pts=[]
xs = []
ys = []
names = []

for y in range(startY, endY, groundHeight):
    for x in range(startX, endX, groundWidth):
        xs += [x]
        ys += [y]
        names += [str(x) + "_" + str(y)]
        inx += 1

pts = [xs,ys]
print pts
print "Prepare completed!\n\n"

curPtInx = 0
def doNext():
    global pts, curPtInx, groundWidth, groundHeight
    
    if curPtInx < len(pts[0]):
        print "Zoom to " + names[curPtInx]
        cx = pts[0][curPtInx]
        cy = pts[1][curPtInx]
        #cx, cy = coordinateTransform( cx, cy, 4326, 3857)
        zoom2area( cx + groundWidth/2, cy + groundHeight/2, groundWidth, groundHeight)
        curPtInx += 1


def onMapLoad():
    global pts, curPtInx, outputWidth, outputHeight, cx, cy, dpi, names
    print "Capture image of " + names[curPtInx-1] + "(" + str(curPtInx-1) + ")"
    captureImage2(  image_save_path + names[curPtInx-1],
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