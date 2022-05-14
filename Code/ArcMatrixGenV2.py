
from math import cos, sin, floor, radians, pi
from turtle import width
import lxml.etree as etree
import random
import svgwrite
from wand.api import library
import wand.color
import wand.image   
import cv2
import numpy as np

class PriorityQueue: #https://youtu.be/wptevk0bshY
    pass


class Queue:
    def __init__(self, id):
        self._Qid = id
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

class ArcSVGShapeTools: #base class with all the functions, such as point generation, rotation, etc
    def __init__(self): #Etype
        '''
        match Etype: #determine what type of generation is needed
            case "Circle":
                pass
            case "Polygon":
                pass
            case "Stargram":
                pass
            case "RotaryDial":
                pass
            case "PolyStar":
                pass
            case "LineBurst":
                pass
            '''
        pass

    def ListPointCoordGen(self, center,  majorRadius, points):
        polar_coords = []
        iteration = 0
        x,y = center
        while iteration < points:
            angle = iteration*((radians(360)/points))-pi/2
            polar_coords.append((majorRadius*cos(angle)+x, majorRadius*sin(angle)+y))
            iteration += 1
        return polar_coords
#different classes to handle different shapes that can be added
class ArcSVGCircle:
    def __init__(self, id, center, majorRadius, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        self.SId = f"Circle{id}"
        self.type = "Circle"
        self.center = center
        self.majorRadius = majorRadius
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill

class ArcSVGRotaryDial(ArcSVGShapeTools):
    def __init__(self, id, center, majorRadius, minorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        self.SId = f"RotaryDial{id}"
        self.type = "RotaryDial"
        self.center = center
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill
        self.pointsList = self.makePointsList()
        self.rings = self.makeRings()
        #print(self.pointsList)
    def makePointsList(self):
        return ArcSVGShapeTools.ListPointCoordGen(self, center = self.center, majorRadius = self.majorRadius, points = self.points)
    def makeRings(self):
        rings = []
        id = 0
        for c in self.pointsList:
            rings.append(ArcSVGCircle(id = f"ring{id}",
                                        center = c,
                                        majorRadius= self.minorRadius,
                                        strokeColor = self.strokeColor, 
                                        strokeWidth = self.strokeWidth, 
                                        Opaque = self.Opaque,
                                        fill = self.fill))
        return rings

class ArcSVGLineBurst:
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, fill = "none"):
        self.SId = f"LineBurst{id}"
        self.type = "LineBurst"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.fill = fill
        
class ArcSVGStargram:
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, fill = "none"):
        self.SId = f"Stargram{id}"
        self.type = "Stargram"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.fill = fill
       
class ArcSVGPolyStar:
    def __init__(self, id, center, majorRadius, minorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        self.SId = f"PolyStar{id}"
        self.type = "PolyStar"
        self.center = center
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill

class ArcSVGPolygon:
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        self.SId = f"Polygon{id}"
        self.type = "Polygon"
        self.center = center
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill

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
        
class ArcSVGMainGen:#basically keep track of layers 
    def __init__(self):
        self.Layers = Queue(id = "root") # a layer is made of a queue of entries, FIFO ordering for build execution
        self.LayerIDs = set()
        self.lastLayerID = None
        self.ShapeIds = {"Circle": IDEntry("Circle"),
                        "Polygon": IDEntry("Polygon"),
                        "Stargram": IDEntry("Stargram"), 
                        "RotaryDial": IDEntry("RotaryDial"), 
                        "PolyStar": IDEntry("PolyStar"),
                        "LineBurst": IDEntry("LineBurst")}
    def makeBuildOrder(self):
        orderIDs = []
        order = []
        for layer in self.Layers.returnQueue():
            for shape in layer.returnQueue():
                order.append(shape)
                orderIDs.append((shape,shape.SId))
                
        return order,orderIDs

    def printLayerContent(self):
        
        [print(s) for s in [f"{L._Qid}\n  ->{[i.SId for i in L.returnQueue()]}"  for L in self.Layers.returnQueue()]]

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

        
    def addShape(self, Etype, Layer= None, center = None, majorRadius= None, minorRadius = None, points = 0, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        
        if Layer is None:
            newLayer = Queue(id = f"Layer{self.newLayerID()}")
            self.Layers.enqueue(newLayer)

        newID = self.ShapeIds[Etype].newIDGen()
        
        match Etype:
            case "Circle":
                newShape = ArcSVGCircle(id = newID,
                                        center = center,
                                        majorRadius= majorRadius,
                                        strokeColor = strokeColor, 
                                        strokeWidth = strokeWidth, 
                                        Opaque = Opaque,
                                        fill = fill)
                newLayer.enqueue(newShape)
                return newShape

            case "Polygon":
                newShape = ArcSVGPolygon(id = newID, 
                                         center = center,
                                         majorRadius = majorRadius,  
                                         points = points,
                                         strokeColor = strokeColor,
                                         strokeWidth = strokeWidth,
                                         fill = fill)
                newLayer.enqueue(newShape)
                return newShape

            case "Stargram":
                newShape = ArcSVGStargram(id = newID, 
                                          center = center,
                                          majorRadius = majorRadius,  
                                          points = points,
                                          strokeColor = strokeColor, 
                                          strokeWidth = strokeWidth,
                                          fill = fill)
                newLayer.enqueue(newShape)
                return newShape

            case "RotaryDial":
                newShape = ArcSVGRotaryDial(id = newID, 
                                            center = center,
                                            majorRadius = majorRadius, 
                                            minorRadius = minorRadius,
                                            points = points, 
                                            strokeColor = strokeColor, 
                                            strokeWidth = strokeWidth, 
                                            Opaque = Opaque,
                                            fill = fill)
                newLayer.enqueue(newShape)
                return newShape

            case "PolyStar":
                newShape = ArcSVGPolyStar(id = newID, 
                                          center = center,
                                          majorRadius = majorRadius,
                                          minorRadius = minorRadius,  
                                          points = points,
                                          strokeColor = strokeColor,
                                          strokeWidth = strokeWidth,
                                          fill = fill)
                newLayer.enqueue(newShape)
                return newShape
                                                  
            case "LineBurst":
                newShape = ArcSVGLineBurst(id = newID, 
                                           center = center,
                                           majorRadius = majorRadius,
                                           points = points,
                                           strokeColor = strokeColor,
                                           strokeWidth = strokeWidth,
                                           fill = fill)
                newLayer.enqueue(newShape)
                return newShape

            

class ArcSVGMainProcess(ArcSVGMainGen):#take stuff from main and pump it out into a proper svg file with svgwrite
    def __init__(self, filename, dimensions, fillrule):
        self.filename = str(filename)
        self.svgDoc = svgwrite.Drawing(filename=str(self.filename),
                                        size = dimensions,
                                        profile='full',
                                        debug=True)
        self.dimensions = dimensions
        self.center = self.getCenter(dimensions)
        self.build = ArcSVGMainGen()
        self.buildata = None

    def makeBuildOrder(self,printed=False):
        order = self.build.makeBuildOrder()
        if printed:
            print(order)
        return order
    def printLayerContent(self):
        self.build.printLayerContent()
    def addShape(self, Etype, center, majorRadius, Layer= None, minorRadius = None, points = 0, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        return self.build.addShape(Etype, Layer= Layer, center = center, majorRadius= majorRadius, minorRadius = minorRadius, points = points, strokeColor = strokeColor, strokeWidth = strokeWidth, Opaque = Opaque, fill = fill)

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

    def exportTransPNG(self, resolution=300, whitebg = False):
        with wand.image.Image(resolution=resolution) as image:
            with wand.color.Color('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand,
                                                background_color.resource)
            image.read(filename=str(self.filename), resolution=300)
            png_image = image.make_blob("png32")
            with open(f"wand-{self.filename[:-4]}.png", "wb") as out:
                out.write(png_image)
            if not whitebg:
                self.removebackground(f"wand-{self.filename[:-4]}.png")
        
        

    def generateBuildData(self): #this figures out what needs to be masked
        pass
    def parseBuildData(self):
        buildOrder, OrderIDs = self.makeBuildOrder()
        doc = self.svgDoc
        Etype = None
        for i,shape in enumerate(buildOrder):
            Etype = shape.type

            match Etype: #determine what type of generation is needed
                case "Circle":
                    if shape.Opaque:
                        defs = doc.defs
                        maskID = shape.SId + "-Mask"
                        mask = defs.add(doc.mask(id = maskID, size = (self.dimensions)))
                        #  fill = "white", height="100%", width="100%"
                        mask.add(doc.rect(size = (self.dimensions), fill = "white"))
                        #doc.rect(width = "100%", height = "100%", fill = "white"
                        mask.add(doc.circle(r = shape.majorRadius, center = shape.center, fill = "black"))
                        #mask.add(doc.use(href = f"#{shape.SId}", fill = "black"))
                        circle = doc.add(doc.circle(id = shape.SId,
                                                    center = shape.center,
                                                    r = shape.majorRadius,
                                                    stroke = shape.strokeColor,
                                                    stroke_width = shape.strokeWidth,
                                                    fill = shape.fill))

                    else:
                        circle = doc.add(doc.circle(id = shape.SId,
                                                center = shape.center,
                                                r = shape.majorRadius,
                                                stroke = shape.strokeColor,
                                                stroke_width = shape.strokeWidth,
                                                fill = shape.fill))
                    
                case "RotaryDial":
                    for s in shape.rings:
                        filler = "white" if s.Opaque else s.fill
                        circle = doc.add(doc.circle(id = s.SId,
                                                center = s.center,
                                                r = s.majorRadius,
                                                stroke = s.strokeColor,
                                                stroke_width = s.strokeWidth,
                                                fill = filler))

                case "Polygon":
                    pass
                case "Stargram":
                    pass
        

                case "PolyStar":
                    pass
                case "LineBurst":
                    pass
    
    def removebackground(self, filename, threshhold = 150):
    # load image
        img = cv2.imread(f'{filename}')

        # convert to graky
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold input image as mask
        mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

        # negate mask
        mask = 255 - mask

        # apply morphology to remove isolated extraneous noise
        # use borderconstant of black since foreground touches the edges
        kernel = np.ones((1,1), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # anti-alias the mask -- blur then stretch
        # blur alpha channel
        mask = cv2.GaussianBlur(mask, (3,3), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

        # linear stretch so that 127.5 goes to 0, but 255 stays 255
        mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

        # put mask into alpha channel
        
        #trying to increase contrast
    
        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
        
        result[:, :, 3] = mask
        

        # save resulting masked image
        cv2.imwrite(filename, result)

        # display result, though it won't show transparency
        #cv2.imshow("INPUT", img)
        #cv2.imshow("GRAY", gray)
        #cv2.imshow("MASK", mask)
        #cv2.imshow("RESULT", result)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()


if __name__ == "__main__":
    #from ArcMatrixGenTester import testArcMatrixGen
    #import unittest
    #unittest.main()
    from memory_profiler import profile
    #@profile
    def main():
        arc = ArcSVGMainProcess("ArcMatrixV2.svg", (1024,1024), "evenodd")
        arc.svgDoc.add(arc.svgDoc.rect(size = (arc.dimensions), fill = "white"))
        arc.addShape(Etype="Circle", center = arc.center, majorRadius = 150)
        arc.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 150, minorRadius= 50, points = 5,Opaque= True, strokeWidth=2)
        arc.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 25, minorRadius= 50, points = 5,Opaque= True, strokeWidth=2)
        arc.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 200, minorRadius= 50, points = 6,Opaque= True, strokeWidth=2)

        #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 100)
        #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 240, strokeColor= "red", Opaque= False)
        #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 350)

        arc.parseBuildData()
        arc.exportSVG()
        arc.printLayerContent()
        arc.exportTransPNG()

    main()

    
    