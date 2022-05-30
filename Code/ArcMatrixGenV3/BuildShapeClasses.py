from math import radians,sin,cos,pi, floor

from numpy import append


def ListPointCoordGen(center,  majorRadius, points, rotation = 0):
        polar_coords = []
        iteration = 0
        x,y = center
        rotation = radians(rotation)
        while iteration < points:
            angle = iteration*((radians(360)/points))-pi/2-rotation
            
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
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2,rounder = False, fill = "none"):
        self.SId = f"Stargram{id}"
        self.type = "Stargram"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.fill = fill
        self.pointsList = self.makePointsList()
        self.shapes = self.makeParaStar()
        self.rounder = rounder
    def makePointsList(self):
        return ListPointCoordGen(
                                center = self.center,
                                majorRadius = self.majorRadius, 
                                points = self.points)
    def determineSteps(self):
        regSteps, degenSteps = [],[]
        half_limit = floor(self.points/2)
        if self.points > 13:
            raise ValueError(f"{self.points} is more than 13")
        if self.points <3:
            raise ValueError(f"{self.points} is less than 3")
        for i in range(1,half_limit+1):
            if self.points % i != 0:
                if i == 6:
                    degenSteps.append(i)
                else:
                    regSteps.append(i)
            elif self.points % i == 0 and i > 1: #if even
                degenSteps.append(i)
        if self.points == 12:
            regSteps.append("12s")
        if self.points == 8:
            degenSteps.append("8s")
        return(regSteps,degenSteps)


    def makeParaStar(self):
        shapes = []
        tid = 0
        #print(self.pointsList)
        regSteps,degenSteps = self.determineSteps()
        print(regSteps,degenSteps)
        stepper = regSteps[0]
        if self.points == 3 or self.points == 4:
                shapes.append(ArcSVGPolygon(id = f"{tid}_{self.SId}",
                                            center = self.center,
                                            majorRadius= self.majorRadius,
                                            points = self.points,
                                            strokeColor = self.strokeColor, 
                                            strokeWidth = self.strokeWidth, 
                                            Opaque = False,
                                            fill = self.fill))
                tid += 1
                return shapes
        elif self.points == 6:
            shapes.append(ArcSVGPolygon(id = f"{tid}.1_{self.SId}",
                                        center = self.center,
                                        majorRadius= self.majorRadius,
                                        points = 3,
                                        strokeColor = self.strokeColor, 
                                        strokeWidth = self.strokeWidth, 
                                        Opaque = False,
                                        fill = self.fill))

            shapes.append(ArcSVGPolygon(id = f"{tid}.2_{self.SId}",
                                        center = self.center,
                                        majorRadius= self.majorRadius,
                                        points = 3,
                                        strokeColor = self.strokeColor, 
                                        strokeWidth = self.strokeWidth, 
                                        Opaque = False,
                                        fill = self.fill,
                                        rotation= 180))
            tid += 1
            return shapes
    
        else:
            curStep = 0
            newPointList = []
            for p in range(self.points):
                newPointList.append((self.pointsList[curStep][0],self.pointsList[curStep][1])) #append x,y
                curStep += stepper
                if curStep >= self.points:
                    curStep -= self.points

            print(newPointList)
            shapes.append(ArcSVGPolygon(id = f"{tid}_{self.SId}",
                                            center = self.center,
                                            majorRadius= self.majorRadius,
                                            points = self.points,
                                            strokeColor = self.strokeColor, 
                                            strokeWidth = self.strokeWidth, 
                                            Opaque = False,
                                            pointsList= newPointList))
            print(shapes)
            return shapes

        '''
        for c in self.pointsList:
            
            if self.points == "8s": 
                shapes.append(ArcSVGPolygon(id = f"{tid}.1_{self.SId}",
                                            center = self.center,
                                            majorRadius= self.majorRadius,
                                            points = 4,
                                            strokeColor = self.strokeColor, 
                                            strokeWidth = self.strokeWidth, 
                                            Opaque = False,
                                            fill = self.fill))

                shapes.append(ArcSVGPolygon(id = f"{tid}.2_{self.SId}",
                                            center = self.center,
                                            majorRadius= self.majorRadius,
                                            points = 4,
                                            strokeColor = self.strokeColor, 
                                            strokeWidth = self.strokeWidth, 
                                            Opaque = False,
                                            fill = self.fill,
                                            rotation= 45))'''
    

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
    def __init__(self, id, center, majorRadius, points, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none", rotation = 0, pointsList = None):
        self.SId = f"Polygon{id}"
        self.type = "Polygon"
        self.center = center
        self.majorRadius = majorRadius
        self.points = points
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.Opaque = Opaque
        self.fill = fill
        self.pointsList = self.makePointsList(rotate= rotation) if pointsList is None else pointsList
        print(self.points)
    def makePointsList(self,rotate):
        return ListPointCoordGen(
                                center = self.center, 
                                majorRadius = self.majorRadius, 
                                points = self.points,
                                rotation = rotate)


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