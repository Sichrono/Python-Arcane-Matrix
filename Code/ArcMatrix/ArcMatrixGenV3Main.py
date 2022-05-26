#from HelperClasses import Queue, ArcSVGShapeTools, IDEntry
#from BuildShapeClasses import ArcSVGCircle, ArcSVGLineBurst, ArcSVGPolygon, ArcSVGPolyStar, ArcSVGRotaryDial, ArcSVGRotaryGon, ArcSVGStargram
from ArcSVGMainBuilder import ArcSVGMainGen
from BuildSVGwriteParser import ArcSVGMainProcess_SVGWRITE
from memory_profiler import profile
if __name__ == "__main__":

    #@profile
    def main():
            arcBuild = ArcSVGMainGen()
            arc = ArcSVGMainProcess_SVGWRITE("ArcMatrixV3.svg", (1024,1024), arcBuild, "evenodd")

            arcBuild.addShape(Etype="Circle", center = arc.center, majorRadius = 150)
            arcBuild.addShape(Etype="RotaryDial", center = arc.center, majorRadius = 150, minorRadius= 50, points = 7, Opaque= True, strokeWidth=2)
            arcBuild.addShape(Etype="RotaryGon", center = arc.center, majorRadius = 150, minorRadius= 50, points =5, shapeCount = 10, Opaque= True, strokeWidth=2)
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