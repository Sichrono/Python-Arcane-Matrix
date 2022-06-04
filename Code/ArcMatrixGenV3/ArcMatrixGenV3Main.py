#from HelperClasses import Queue, ArcSVGShapeTools, IDEntry
#from BuildShapeClasses import ArcSVGCircle, ArcSVGLineBurst, ArcSVGPolygon, ArcSVGPolyStar, ArcSVGRotaryDial, ArcSVGRotaryGon, ArcSVGStargram
from ArcSVGMainBuilder import ArcSVGMainGen
from BuildSVGwriteParser import ArcSVGMainProcess_SVGWRITE
from memory_profiler import profile
from math import cos, sin, floor, radians, pi, lcm

if __name__ == "__main__":
    def HypotrochoidPointsGen(R, r, d, center):
        xc, yc = center
        points = "M"
        for i in range(100):
            
            x = (R-r)*cos(i)+d*cos((R-r)/r*i) + xc
            y = (R-r)*sin(i)-d*sin((R-r)/r*i) + yc

            points += (f"{x} {y} ")
        points += "z"
        #print(points)
        return points
    def HypocycloidPointsGen(k, r, center, steps = 20):
        xc, yc = center
        points = "M"
        for i in range(19*k):
            i /= steps
            i -= pi/2

            x = r*(k-1)*cos(i)+r*cos((k-1)*i) + xc
            y = r*(k-1)*sin(i)-r*sin((k-1)*i) + yc

            points += (f"{x} {y} ")
        #points += "z"
        #print(points)
        return points

    #@profile
    def main():
            arcBuild = ArcSVGMainGen()
            arc = ArcSVGMainProcess_SVGWRITE("ArcMatrixV3.svg", (1024,1024), arcBuild, "evenodd")

            #arcBuild.addShape(Etype="Circle", center = arc.center, majorRadius = 150)
            #arcBuild.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 150, minorRadius= 50, points = 7, Opaque= True, strokeWidth=2)
            #e = arcBuild.addShape(Etype="RotaryGon", center = arc.center, majorRadius = 300, minorRadius= 70, points =7, shapeCount = 10, Opaque= True, strokeWidth=2)
            #for c in e.pointsList:
            #    arcBuild.addShape(Etype="RotaryDial", center = c, majorRadius = e.minorRadius, minorRadius= 15, points = 9, Opaque= True, strokeWidth=2)

            #arcBuild.addShape(Etype="Stargram", center = arc.center, majorRadius = 200, points = 7,rounder = True)
            arcBuild.addShape(Etype="PolyStar", center = arc.center, majorRadius = 200, minorRadius= 150, points = 34,rounder = True)
            #arcBuild.addShape(Etype="Stargram", center = arc.center, majorRadius = 300, points = 6)
            #arc.svgDoc.add(arc.svgDoc.path(d = HypocycloidPointsGen(k = 11, r = 40, center = arc.center), fill="none", stroke="#FFC681", stroke_width = 3))
    
            


            #arc.addShape(Etype="Polygon", center = arc.center, majorRadius = 150, points = 5,Opaque= True, strokeWidth=2)
            #arc.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 25, minorRadius= 50, points = 5,Opaque= True, strokeWidth=2)
            #arc.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 200, minorRadius= 50, points = 10,Opaque= False, strokeWidth=2)
            
            #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 100)
            #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 240, strokeColor= "red", Opaque= False)
            #arc.addShape(Etype="Circle", center = arc.center, majorRadius = 350)
        
            arc.parseBuildData()
            arc.exportSVG()
            #arc.printLayerContent()
            #arc.exportTransPNG()

    main()

        
