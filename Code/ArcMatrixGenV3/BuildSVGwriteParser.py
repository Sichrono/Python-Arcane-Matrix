import svgwrite
from ArcSVGMainBuilder import ArcSVGMainGen
import lxml.etree as etree
from wand.api import library
import wand.color
import wand.image   
import cv2
import numpy as np

class ArcSVGMainProcess_SVGWRITE(ArcSVGMainGen):#take stuff from main and pump it out into a proper svg file with svgwrite
    def __init__(self, filename, dimensions, build , fillrule = "evenodd"):
        self.filename = str(filename)
        self.svgDoc = svgwrite.Drawing(filename=str(self.filename),
                                        size = dimensions,
                                        profile='full',
                                        debug=True)
        self.svgDoc.fill(rule = fillrule)
        self.dimensions = dimensions
        self.center = self.getCenter(dimensions)
        self.build = build 
        self.buildata = None
        
        self.svgDoc.add(self.svgDoc.rect(size = (self.dimensions), fill = "white"))
        
    def makeBuildOrder(self,printed=False):
        order = self.build.makeBuildOrder()
        if printed:
            print(order)
        return order

    def printLayerContent(self):
        self.build.printLayerContent()

    def addShape(self, Etype, center, majorRadius, Layer= None, minorRadius = None, points = 0, shapeCount = None, strokeColor = "purple", strokeWidth = 2, Opaque = False, fill = "none"):
        return self.build.addShape(
                                Etype, 
                                Layer= Layer, 
                                center = center, 
                                majorRadius= majorRadius, 
                                minorRadius = minorRadius, 
                                points = points, 
                                shapeCount = points if shapeCount is None else shapeCount,
                                strokeColor = strokeColor, 
                                strokeWidth = strokeWidth, 
                                Opaque = Opaque, 
                                fill = fill)


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
                    circle = doc.add(doc.circle(id = shape.SId,
                                            center = shape.center,
                                            r = shape.majorRadius,
                                            stroke = shape.strokeColor,
                                            stroke_width = shape.strokeWidth,
                                            fill = shape.fill))
                    
                case "RotaryDial":
                    filler = "white" if shape.Opaque else shape.fill
                    for s in shape.rings:
                        ring = doc.add(doc.circle(id = s.SId,
                                                center = s.center,
                                                r = s.majorRadius,
                                                stroke = s.strokeColor,
                                                stroke_width = s.strokeWidth,
                                                fill = filler))

                case "Polygon":
                    filler = "white" if shape.Opaque else shape.fill
                    polygon = doc.add(doc.polygon(id = shape.SId,
                                                points = shape.pointsList,
                                                stroke = shape.strokeColor,
                                                stroke_width = shape.strokeWidth,
                                                fill = filler))

                case "Stargram":
                    pass
                case "PolyStar":
                    pass
                case "LineBurst":
                    pass
                case "RotaryGon":
                    filler = "white" if shape.Opaque else shape.fill
                    for p in shape.polygons:
                        polygon = doc.add(doc.polygon(id = p.SId,
                                                points = p.pointsList,
                                                stroke = p.strokeColor,
                                                stroke_width = p.strokeWidth,
                                                fill = filler))


    #https://stackoverflow.com/questions/2932408/server-side-svg-to-png-or-some-other-image-format-in-python
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