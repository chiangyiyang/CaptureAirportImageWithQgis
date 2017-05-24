from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.utils import iface


def coordinateTransform(x, y, src_crs_id, tar_crs_id):
    src_crs = QgsCoordinateReferenceSystem()
    src_crs.createFromSrid(src_crs_id)
    tar_crs = QgsCoordinateReferenceSystem()
    tar_crs.createFromSrid(tar_crs_id)
    tf = QgsCoordinateTransform(src_crs, tar_crs)
    pt = QgsGeometry.fromPoint(QgsPoint(x, y))
    pt.transform(tf)
    return pt.asPoint()
    
    
def captureImage2(name, type, w, h):
    ##Output using Map Composer#########
    # set up composition
    mapRenderer = iface.mapCanvas().mapRenderer()
    c = QgsComposition(mapRenderer)
    c.setPlotStyle(QgsComposition.Print)
    dpi = 100
    c.setPrintResolution(dpi)
#    dpi = c.printResolution()
    
    # add a map to the composition
    width = w
    height = h
    w = int(w/dpi*25.4)
    h = int(h/dpi*25.4)
    c.setPaperSize(w, h, False)
    composerMap = QgsComposerMap(c, 0, 0, w, h) 
    c.addItem(composerMap)

    ##Output to a raster image#########
    dpmm = dpi / 25.4
    
    # create output image and initialize it
    image = QImage(QSize(width, height), QImage.Format_ARGB32)
    image.setDotsPerMeterX(dpmm * 1000)
    image.setDotsPerMeterY(dpmm * 1000)
    image.fill(0)

    # render the composition
    imagePainter = QPainter(image)
    sourceArea = QRectF(0, 0, w, h)
    targetArea = QRectF(0, 0, width, height)
    c.render(imagePainter, targetArea, sourceArea)
    imagePainter.end()
    image.save( name +'.' + type, type)


def captureImage(name, type, dpi, w, h):
    ##Output using Map Composer#########
    # set up composition
    mapRenderer = iface.mapCanvas().mapRenderer()
    c = QgsComposition(mapRenderer)
    c.setPlotStyle(QgsComposition.Print)
    c.setPrintResolution(dpi)
    
    # add a map to the composition
    c.setPaperSize(w, h, False)
    composerMap = QgsComposerMap(c, 0, 0, w, h) 
    c.addItem(composerMap)

    ##Output to a raster image#########
    dpi = c.printResolution()
    dpmm = dpi / 25.4
    width = int(dpmm * w)
    height = int(dpmm * h)
    
    # create output image and initialize it
    image = QImage(QSize(width, height), QImage.Format_ARGB32)
    image.setDotsPerMeterX(dpmm * 1000)
    image.setDotsPerMeterY(dpmm * 1000)
    image.fill(0)

    # render the composition
    imagePainter = QPainter(image)
    sourceArea = QRectF(0, 0, w, h)
    targetArea = QRectF(0, 0, width, height)
    c.render(imagePainter, targetArea, sourceArea)
    imagePainter.end()
    image.save( name +'.' + type, type)

#captureImage(
#            "./output/test22",      # file name
#            "png",                  # file type
#            100,                    # image dpi
#            200,                    # image width
#            200)                    # image height


def zoom2area(x, y, imgWidth, imgHeight):
    canvas = iface.mapCanvas()
    canvas.setExtent(
            QgsRectangle(
                x - imgWidth/2, y - imgHeight/2, 
                x + imgWidth/2, y + imgHeight/2
                ))
    canvas.refresh()


#zoom2area( x, y, imgWidth, imgHeight)