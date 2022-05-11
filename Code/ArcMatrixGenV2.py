from math import cos, sin, floor, radians, pi
import lxml.etree as etree
import random
import svgwrite
from wand.api import library
import wand.color
import wand.image   

class PriorityQueue: #https://youtu.be/wptevk0bshY
    pass


class Queue:
    def __init__(self, id):
        self.id = id
        self._L = []

    def enqueue(self, item):
        self._L.append(item)

    def dequeue(self):
        return self._L.pop(0)

    def swapEntries(self, i1, i2):
        self._L[i1],self._L[i2] = self._L[i2], self._L[i1]

    def peek(self):
        return self._L[0]

    def __len__(self):
        return len(self._L)

    def isempty(self):
        return len(self) == 0
    
    def returnQueue(self):
        return self._L

class ArcSVGShape: #base class with all the functions, such as point generation, rotation, etc
    def __init__(self):
        pass
    
#different classes to handle different shapes that can be added
class ArcSVGCircle(ArcSVGShape):
    def __init__(self, id, center, majorRadius, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"Circle{id}"
        self.center = center
        self.majorRadius = majorRadius
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque

class ArcSVGRotoryDial(ArcSVGShape):
    def __init__(self, id, center, majorRadius, minorRadius, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"RotaryDial{id}"
        self.center = center
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque

class ArcSVGLineBurst(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2):
        self.id = f"LineBurst{id}"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        
class ArcSVGStargram(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2):
        self.id = f"Stargram{id}"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        
class ArcSVGPolyStar(ArcSVGShape):
    def __init__(self, id, center, majorRadius, minorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"PolyStar{id}"
        self.center = center
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque

class ArcSVGPolygon(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"Polygon{id}"
        self.center = center
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque

class IDEntry:
    def __init__(self, Etype):
        self.type = Etype
        self.Ids = set()
        self.LastId = None

    def newIDGen(self):
        if self.LastId is None:
            self.LastId = 0
            self.Ids.add(0)
            return 0

        newID = self.LastId
        while newID in self.Ids:
            newID += 1

        self.Ids.add(newID)
        self.LastId = newID
        return newID
        
class ArcSVGMainGen(ArcSVGShape):#basically keep track of layers 
    def __init__(self):
        self.Layers = Queue(id = "root") # a layer is made of a queue of entries, FIFO ordering for build execution
        self.LayerIDs = set()
        self.lastLayerID = None
        self.ShapeIds = {"Circle": IDEntry("Circle"),
                        "Polygon": IDEntry("Polygon"),
                        "Stargram": IDEntry("Stargram"), 
                        "RotoryDial": IDEntry("RotoryDial"), 
                        "PolyStar": IDEntry("PolyStar"),
                        "LineBurst": IDEntry("LineBurst")}

    def newLayer(self):
        self.Layers.enqueue(Queue()) #add a new queue as a layer
    
    def swapLayers(self, layer1, layer2):
        self.Layers.swapEntries(layer1, layer2)
    
    def newLayerID(self):
        if self.lastLayerID is None:
            self.LayerIDs.add(0)
            self.lastLayerID = 0
            return 0
        
        newID = self.lastLayerID
        while newID in self.LayerIDs:
            newID += 1

        self.LayerIDs.add(newID)
        self.lastLayerID = newID
        return newID

        
    def addShape(self, Etype, Layer= None, center = None, majorRadius= None, minorRadius = None, points = 0, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        if Layer is None:
            newLayer = Queue(id = self.newLayerID)
            self.Layers.enqueue(newLayer)

        newID = self.ShapeIds[Etype].newIDGen()
        
        match Etype:
            case "Circle":
                newLayer.enqueue(ArcSVGCircle(id = newID,
                                              center = center,
                                              majorRadius= majorRadius,
                                              strokeColor = strokeColor, 
                                              strokeWidth = strokeWidth, 
                                              Opaque = Opaque))
            case "Polygon":
                newLayer.enqueue(ArcSVGPolygon(id = newID, 
                                               center = center,
                                               majorRadius = majorRadius,  
                                               points = points,
                                               strokeColor = strokeColor,
                                               strokeWidth = strokeWidth))
            case "Stargram":
                newLayer.enqueue(ArcSVGStargram(id = newID, 
                                                  center = center,
                                                  majorRadius = majorRadius,  points = points,
                                                  strokeColor = strokeColor, 
                                                  strokeWidth = strokeWidth))
            case "RotoryDial":
                newLayer.enqueue(ArcSVGRotoryDial(id = newID, 
                                                  center = center,
                                                  majorRadius = majorRadius, 
                                                  minorRadius = minorRadius, 
                                                  strokeColor = strokeColor, 
                                                  strokeWidth = strokeWidth, 
                                                  Opaque = Opaque))
            case "PolyStar":
                newLayer.enqueue(ArcSVGPolyStar(id = newID, 
                                               center = center,
                                               majorRadius = majorRadius,
                                               minorRadius = minorRadius,  
                                               points = points,
                                               strokeColor = strokeColor,
                                               strokeWidth = strokeWidth))
            case "LineBurst":
                newLayer.enqueue(ArcSVGLineBurst(id = newID, 
                                                 center = center,
                                                 majorRadius = majorRadius,
                                                 points = points,
                                                 strokeColor = strokeColor,
                                                 strokeWidth = strokeWidth))

            

class ArcSVGMainProcess(ArcSVGMainGen):#take stuff from main and pump it out into a proper svg file with svgwrite
    def __init__(self, filename, dimensions, fillrule):
        self.filename = str(filename)
        self.svgDoc = svgwrite.Drawing(filename=str(self.filename) + ".svg",
                                        size = dimensions,
                                        profile='full',
                                        debug=True)
        self.center = self.getCenter(dimensions)
        self.build = ArcSVGMainGen()

    def parseLayerData(self, layerList):
        pass

    def getCenter(self, dimensions):
        width,height = dimensions
        return width/2,height/2

    def exportSVG(self):
        self.svgDoc.save()
        self.makePretty()

    def makePretty(self):
        etree_parse = etree.parse(self.filename)
        outPretty = etree.tostring(etree_parse, pretty_print=True, encoding="unicode")
        with open(self.filename,"w") as svg_file:
            svg_file.write(outPretty)

    def exportTransPNG(self, resolution):
        with wand.image.Image(resolution=300) as image:
            with wand.color.Color('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand,
                                                background_color.resource)
            image.read(filename=str(self.filename) + ".svg", resolution=300)
            png_image = image.make_blob("png32")
            with open(f"wand-{self.filename}.png", "wb") as out:
                out.write(png_image)

    def addShape(self, Etype, center=(0,0), Layer = None):
        return self.build.addShape(Etype, center=(0,0), Layer = None)
    
    


if __name__ == "__main__":
    import unittest
    from ArcMatrixGenTester import testArcMatrixGen
    unittest.main()
    
    