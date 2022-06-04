from HelperClasses import IDEntry, Queue
from BuildShapeClasses import ArcSVGCircle, ArcSVGLineBurst, ArcSVGPolygon, ArcSVGPolyStar, ArcSVGRotaryDial, ArcSVGRotaryGon, ArcSVGStargram

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
                        "LineBurst": IDEntry("LineBurst"),
                        "RotaryGon": IDEntry("RotaryGon")}

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

        
    def addShape(
                self, 
                Etype,
                Layer= None, 
                center = None, 
                majorRadius= None, 
                minorRadius = None, 
                points = 0, 
                shapeCount = None,
                strokeColor = "purple",
                strokeWidth = 2, 
                Opaque = False,
                rounder = False, 
                fill = "none"):
        
        if Layer is None:
            newLayer = Queue(id = f"Layer{self.newLayerID()}")
            self.Layers.enqueue(newLayer)

        newID = self.ShapeIds[Etype].newIDGen()
        
        match Etype:
            case "Circle":
                newShape = ArcSVGCircle(
                                    id = newID,
                                    center = center,
                                    majorRadius= majorRadius,
                                    strokeColor = strokeColor, 
                                    strokeWidth = strokeWidth, 
                                    Opaque = Opaque,
                                    fill = fill
                                    )
                newLayer.enqueue(newShape)
                return newShape

            case "Polygon":
                newShape = ArcSVGPolygon(
                                    id = newID, 
                                    center = center,
                                    majorRadius = majorRadius,  
                                    points = points,
                                    strokeColor = strokeColor,
                                    strokeWidth = strokeWidth,
                                    Opaque = Opaque,
                                    fill = fill
                                    )
                newLayer.enqueue(newShape)
                return newShape

            case "Stargram":
                newShape = ArcSVGStargram(id = newID, 
                                          center = center,
                                          majorRadius = majorRadius,  
                                          points = points,
                                          strokeColor = strokeColor, 
                                          strokeWidth = strokeWidth,
                                          rounder = rounder,
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

            case "RotaryGon":
                newShape = ArcSVGRotaryGon(id = newID, 
                                            center = center,
                                            majorRadius = majorRadius, 
                                            minorRadius = minorRadius,
                                            points = points, 
                                            shapeCount = shapeCount,
                                            strokeColor = strokeColor, 
                                            strokeWidth = strokeWidth, 
                                            Opaque = Opaque,
                                            fill = fill)
                newLayer.enqueue(newShape)
                return newShape
            case _:
                raise ValueError(f"Etype: {Etype} is not valid")
                