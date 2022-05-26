from math import radians,sin,cos,pi

def ListPointCoordGen(center,  majorRadius, points, rotation = 0, pointCenter = False):
        polar_coords = []
        iteration = 0
        x,y = center
        rotation = radians(rotation)
        while iteration < points:
            angle = iteration*((radians(360)/points))-pi/2
            
            x1,y1 = cos(angle), sin(angle)
            '''
            print(x1,y1)
            if pointCenter:
                xp = x1*cos(rotation)-y1*sin(rotation)
                yp = y1*cos(rotation)+x1*sin(rotation)
                polar_coords.append((majorRadius*xp+x,majorRadius*yp+y))
                iteration += 1
            '''
            
            polar_coords.append((majorRadius*x1+x,majorRadius*y1+y))
            iteration += 1
        return polar_coords

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
        
class ArcSVGRotaryDial:
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
        return ListPointCoordGen(
                                center = self.center,
                                majorRadius = self.majorRadius, 
                                points = self.points)
    def makeRings(self):
        rings = []
        tid = 0
        for c in self.pointsList:
            rings.append(ArcSVGCircle(id = f"{tid}_{self.SId}",
                                        center = c,
                                        majorRadius= self.minorRadius,
                                        strokeColor = self.strokeColor, 
                                        strokeWidth = self.strokeWidth, 
                                        Opaque = self.Opaque,
                                        fill = self.fill))
            tid += 1
        return rings

class ArcSVGRotaryGon:
    def __init__(self, id, center, majorRadius, minorRadius, points, shapeCount = None, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        self.SId = f"RotaryGon{id}"
        self.type = "RotaryGon"
        self.center = center
        self.majorRadius = majorRadius
        self.minorRadius = minorRadius
        self.points = points
        self.shapeCount = shapeCount
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill
        self.pointsList = self.makePointsList()
        self.polygons = self.makePolygons()
        #print(self.pointsList)
    def makePointsList(self):
        return ListPointCoordGen(
                                center = self.center,
                                majorRadius = self.majorRadius, 
                                points = self.points)

    def makePolygons(self):
        polygons = []
        tid = 0
        for c in self.pointsList:
            polygons.append(ArcSVGPolygon(id = f"{tid}_{self.SId}",
                                        center = c,
                                        majorRadius= self.minorRadius,
                                        points = self.points,
                                        strokeColor = self.strokeColor, 
                                        strokeWidth = self.strokeWidth, 
                                        Opaque = self.Opaque,
                                        fill = self.fill))
            tid += 1
        return polygons

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
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill
        self.pointsList = self.makePointsList()
        
    def makePointsList(self):
        return ListPointCoordGen(
                                center = self.center, 
                                majorRadius = self.majorRadius, 
                                points = self.points)


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