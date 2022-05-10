from math import cos, sin, floor, radians, pi
import lxml.etree as etree
import random
import svgwrite
from wand.api import library
import wand.color
import wand.image   

class PriorityQueue(): #https://youtu.be/wptevk0bshY
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
class ArcSVGShape():
    pass

class ArcSVGCircle(ArcSVGShape):
    def __init__(self, id, center, majorRadius, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"Circle{id}"
        self.center = center

class ArcSVGRotoryDial(ArcSVGShape):
    def __init__(self, id, center, majorRadius, minorRadius, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"RotaryDial{id}"
        self.center = center

class ArcSVGLineBurst(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2):
        self.id = f"LineBurst{id}"
        self.center = center

class ArcSVGStargram(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2):
        self.id = f"Stargram{id}"
        self.center = center

class ArcSVGPolyStar(ArcSVGShape):
    def __init__(self, id, center, majorRadius, minorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"PolyStar{id}"
        self.center = center

class ArcSVGPolygon(ArcSVGShape):
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False):
        self.id = f"Polygon{id}"
        self.center = center

class ArcSVGMain(ArcSVGShape):#basically keep track of layers 
    def __init__(self):
        self.Layers = Queue() # a layer is made of a queue of entries, FIFO ordering for build execution
        self.currentLayer = 0
        
    def newLayer(self):
        self.Layers.enqueue(Queue()) #add a new queue as a layer
    
    def swapLayers(self, layer1, layer2):
        self.Layers.swapEntries(layer1, layer2)
        
    def addEntry(self, Etype, center=(0,0)):
        match Etype:
            case "Circle":
                print("circle")
            case "Polygon":
                pass
            case "Stargram":
                pass
            case "RotoryDial":
                pass
            case "PolyStar":
                pass
            case "LineBurst":
                pass



class ArcSVGProcess(ArcSVGMain):#take stuff from main and pump it out into a proper svg file with svgwrite
    def __init__(self, filename, dimensions, fillrule):
        self.filename = str(filename)
        self.svgDoc = svgwrite.Drawing(filename=str(self.filename) + ".svg",
                                        size = dimensions,
                                        profile='full',
                                        debug=True)
        self.center = self.getCenter(dimensions)

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
        


if __name__ == "__main__":
    g = ArcSVGProcess("ArcMatrixV2", (1024,1024), "evenodd")
    g.addEntry(Etype="Circle")
    