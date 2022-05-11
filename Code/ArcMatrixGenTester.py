from ArcMatrixGenV2 import ArcSVGMainProcess
import unittest

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
        print(self.arc.build.Layers.returnQueue())
        
        #self.assertEqual(e,0)

if __name__ == "__main__":
    unittest.main()
    #g.addEntry(Etype="Circle")