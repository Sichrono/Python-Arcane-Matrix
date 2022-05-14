from ArcMatrixGenV2 import ArcSVGMainProcess
import unittest
from memory_profiler import profile

class testArcMatrixGen(unittest.TestCase):
    def setUp(self):
        self.arc = ArcSVGMainProcess("ArcMatrixV2", (1024,1024), "evenodd")
    def testArcSVGMainGen__init__(self):
        self.assertEqual(len(self.arc.build.Layers),0)
        self.assertEqual(self.arc.filename, "ArcMatrixV2")

    def testArcSVGMainaddShape(self):
        self.arc.addShape("Circle")
        self.arc.addShape("Stargram")
        self.arc.addShape("LineBurst")
        self.arc.addShape("Polygon")
        self.arc.addShape("PolyStar")
        self.arc.addShape("Polygon")
        self.arc.addShape("Polygon")
        self.arc.addShape("Polygon")
        self.arc.addShape("Polygon")

        #print([[x.id for x in i._L] for i in self.arc.build.Layers.returnQueue()])
        #self.arc.build.returnLayerContent()
        #self.assertEqual(e,0)


if __name__ == "__main__":
    #testArcSVGMainaddShape()
    unittest.main()
    #g.addEntry(Etype="Circle")