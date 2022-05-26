from math import radians,sin,cos,pi

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

#dead class
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

    def ListPointCoordGen(self, center,  majorRadius, points, rotation = 0, pointCenter = False):
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