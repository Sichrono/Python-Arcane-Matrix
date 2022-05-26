
import svgwrite
from math import cos, sin, floor, radians, pi
import random
import lxml.etree as etree
from wand.api import library
import wand.color
import wand.image   

'''
svg_doc = svgwrite.Drawing(filename = "test-svgwrite.svg",
                                size = ("1000px", "1000px"))
    svg_doc.fill(rule = "evenodd")

    svg_doc.add(svg_doc.rect(insert = (10, 0),
                                    size = ("200px", "100px"),
                                    stroke_width = "1",
                                    stroke = "black",
                                    fill = "rgb(255,255,0)",))
    svg_doc.add(svg_doc.circle(center = (75 ,50),
                                        r = 45,
                                        stroke_width = "1",
                                        stroke = "black",
                                        fill = "rgb(255,255,0)"))

'''

def polar_Coord_Gen(total, radius, iteration, rotation_pi = 0): 
    angle = iteration*((radians(360)/total))-pi/2-rotation_pi
    polar_coords = radius * cos(angle), radius * sin(angle)
    return polar_coords
def num_points_gen(ring_level = 0):
    upper = 7
    return random.randint(3, upper)
def get_draw_center(width, height):
    return width/2,height/2
def determine_Steps(points):
    reg_Steps, degen_Steps = [],[]
    half_limit = floor(points/2)
    if points > 13:
        points = 13
    if points <= 2:
        points = 3
    for i in range(1,half_limit+1):
        if points % i != 0:
            if i == 6:
                degen_Steps.append(i)
            else:
                reg_Steps.append(i)
        elif points % i == 0 and i > 1:
            degen_Steps.append(i)
    return(reg_Steps,degen_Steps)

def points_To_Center_Lines_add(base, center = (0,0), point_count = 5, poly_coords = []):
    output_Coords = []
    for c in poly_coords:
        output_Coords.append(c)
        output_Coords.append(center)
    return output_Coords
    
def regular_Polygons_Points_add(base, 
                                center = (0,0), 
                                radius = 100, 
                                point_count = 5,
                                stroke_color = "green", 
                                stroke_width = 2,
                                fill = "none",
                                center_lines = False):
    poly_coords = []
    center_lines_coords = []
    for p in range(point_count):
        x,y = polar_Coord_Gen(total = point_count, radius = radius, iteration = p)
        poly_coords.append((round(x + center[0]),round(y + center[1])))
    if center_lines == True:
        center_lines_coords = points_To_Center_Lines_add(base = base,
                                    center = center,
                                    point_count = point_count,
                                    poly_coords= poly_coords)

        base.add(base.polyline(points = center_lines_coords,
                                fill = fill,
                                stroke = stroke_color,
                                stroke_width = stroke_width))

    base.add(base.polygon(points = poly_coords,
                            stroke = stroke_color, 
                            stroke_width = stroke_width,
                            fill = fill, 
                            stroke_linejoin = "bevel"))

def parametric_Star_Points_add(base,
                                center = (0,0), 
                                radius = 100, 
                                point_count = 5,
                                stroke_color = "red", 
                                stroke_width = 2,
                                fill = "none", 
                                stroke_linejoin = "bevel"):
    if point_count <= 4:
        return
    if point_count == 6:
        new_count = 3
        loops = point_count/3
        for i in range(int(loops)):
            poly_coords = []
            for p in range(new_count):
                x,y = polar_Coord_Gen(total = new_count, radius = radius, iteration = p, rotation_pi = i * pi)
                poly_coords.append((round(x + center[0]),round(y + center[1])))
        
            base.add(base.polygon(points = poly_coords,
                                stroke = stroke_color, 
                                stroke_width = stroke_width,
                                fill = fill,
                                stroke_linejoin = stroke_linejoin))
        return
    poly_coords = []
    star_coords = []
    
    for p in range(point_count):
        x,y = polar_Coord_Gen(total = point_count, radius = radius, iteration = p)
        poly_coords.append((round(x + center[0]),round(y + center[1])))
    
    reg_Steps,degen_Steps = determine_Steps(point_count)
    if point_count == 12:
        reg_Steps.append("twelve")
    if point_count == 8:
        reg_Steps.append("eight")
    step_size = random.choice(reg_Steps)

    if step_size == "twelve" or step_size == "eight":
        new_count = 3
        loops = point_count/3
        rotate = 2
        if step_size == "eight":
            new_count = 4
            loops = 2
            rotate = 4

        for i in range(int(loops)):
            poly_coords = []
            for p in range(new_count):
                x,y = polar_Coord_Gen(total = new_count, radius = radius, iteration = p, rotation_pi = i/rotate * pi)
                poly_coords.append((round(x + center[0]),round(y + center[1])))
        
            base.add(base.polygon(points = poly_coords,
                                stroke = stroke_color, 
                                stroke_width = stroke_width,
                                fill = fill,
                                stroke_linejoin = stroke_linejoin))
        return
    step_num = 0
    for p in range(point_count):
        x,y = poly_coords[step_num][0],poly_coords[step_num][1]
        star_coords.append((x,y))
        step_num += step_size
        if step_num >= point_count:
            step_num -= point_count

    base.add(base.polygon(points = star_coords,
                            stroke = stroke_color, 
                            stroke_width = stroke_width,
                            fill = fill,
                            stroke_linejoin = stroke_linejoin), transform="rotate(180)")

def circle_ring_add(base,
                    center = (0,0),
                    radius = 100,
                    stroke_color = "purple", 
                    stroke_width = 2,
                    fill = "none"):
    base.add(base.circle(center = center,
                        r = radius,
                        stroke = stroke_color,
                        stroke_width = stroke_width,
                        fill = fill))
    
def rotory_phone_ring_add():
    pass

def main_Matrix(base,
                matrix_center = (0,0), 
                max_detail = 1, 
                start_radius = 200, 
                current_detail = 0, 
                current_ring = 0, 
                point_centers = [],
                current_radius = 0):
                
    num_points = int(num_points_gen(ring_level = current_ring))
    num_points = 5

    print("num_points = ",num_points)
    if current_detail == max_detail:
        pass
    
    current_radius = start_radius/(current_ring*2+1)
    if current_ring == 0:
        point_centers.append(matrix_center)
        current_radius = start_radius

    
    print("current_radius = ",current_radius)
    print("point_centers = ",point_centers)
    print("current_detail = ",current_detail)
    poly_random = random.random() < 0.8
    polyline_random = random.random() < 0.8
    for centers in point_centers:
        '''if random.random() < 0.8:
            parametric_Star_Points_add(base = svg_doc, 
                                        center = centers, 
                                    i    radius = current_radius, 
                                        point_count = num_points,
                                        stroke_color = "red", 
                                        stroke_width = 1,
                                        fill = "none", 
                                        stroke_linejoin = "bevel")'''
        if poly_random == True:
            state = False
            if polyline_random == True:
                state = True
            regular_Polygons_Points_add(base = svg_doc, 
                                        center = centers, 
                                        radius = current_radius, 
                                        point_count = num_points,
                                        stroke_color = "green", 
                                        stroke_width = 2,
                                        center_lines = state)
        
        circle_ring_add(base = svg_doc, 
                        center = centers, 
                        radius = current_radius, 
                        stroke_color = "purple", 
                        stroke_width = 2)

    if current_detail < max_detail:
        new_centers = []
        print("new_center_base = ",point_centers)
        for center in point_centers:
            for point in range(num_points):
                x,y = polar_Coord_Gen(total = num_points, radius = current_radius, iteration = point)
                new_centers.append((round(x + center[0]) ,round(y + center[1])))
                
        main_Matrix(base,
                matrix_center = matrix_center, 
                max_detail = max_detail, 
                start_radius = start_radius, 
                current_detail = current_detail + 1, 
                current_ring = current_ring + 1, 
                point_centers = new_centers)


        
                

if __name__ == '__main__':
    import time
    start_time = time.time()

    draw_width,draw_height = 1024, 1024
    draw_center = get_draw_center(draw_width, draw_height)
    max_detail = 1
    svg_doc = svgwrite.Drawing(filename = "ArcMatrix.svg",
                                size = (draw_width, draw_height),
                                profile='full',
                                debug=True)#insert= (50,100)
    svg_doc.fill(rule = "evenodd")

    main_Matrix(base = svg_doc,max_detail = max_detail, matrix_center = draw_center, start_radius = 200) 
    
    svg_doc.save()

    etree_parse = etree.parse(svg_doc.filename)
    outPretty = etree.tostring(etree_parse, pretty_print=True, encoding="unicode")
    with open(svg_doc.filename,"w") as svg_file:
        svg_file.write(outPretty)
    
    print(f"[Finished in {(time.time() - start_time):.4f}]")


    def svg_to_png(infile, outfile, dpi=300):
        with wand.image.Image(resolution=dpi) as image:
            with wand.color.Color('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand,
                                                background_color.resource)
            image.read(filename=infile, resolution=dpi)
            png_image = image.make_blob("png32")
            with open(outfile, "wb") as out:
                out.write(png_image)

    svg_to_png(svg_doc.filename, f"wand-{svg_doc.filename[:-4]}.png", dpi=100)

    #f"{svg_doc.filename[:-4]}-Masked.svg"
    

'''
    from wand.api import library
    import wand.color
    import wand.image

    with wand.image.Image() as image:
        with wand.color.Color('transparent') as background_color:
            library.MagickSetBackgroundColor(image.wand, 
                                            background_color.resource) 
        image.read(blob=svg_file.read(), format="svg")
        png_image = image.make_blob("png32")

    with open(output_filename, "wb") as out:
        out.write(png_image)

    
    
    #doesnt support alpha channel sadly
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from pdf2image import convert_from_path
    import os

    svgDrawing = svg2rlg(svg_doc.filename)
    renderPDF.drawToFile(svgDrawing, svg_doc.filename[:-4]+".pdf")

    pages = convert_from_path(svg_doc.filename[:-4]+".pdf", 150)
    pages[0].save(svg_doc.filename[:-4]+".png", fmt='PNG')

    #make image transparent
    
    #os.remove(svg_doc.filename[:-4]+".pdf")
    #os.remove(svg_doc.filename[:-4]+".svg")

    from PIL import Image
    
    img = Image.open(svg_doc.filename[:-4]+".png")
    rgba = img.convert("RGBA")
    datas = rgba.getdata()
    
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # finding black colour by its RGB value
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged
    
    rgba.putdata(newData)
    rgba.save("transparent_image.png", "PNG")

    
  




svg_String = svg_String.split(" ")
    for string in svg_String:
        print(string)


def points_To_Center_Lines(base, center = (0,0), point_count = 5, poly_coords = []):
    output_Coords = []
    for c in poly_coords:
        output_Coords.append(c)
        output_Coords.append(center)
    return output_Coords
def regular_Polygons_Points(base, center = (0,0), radius = 100, point_count = 5):
    poly_coords = []
    for p in range(point_count):
        x,y = polar_Coord_Gen(total = point_count, radius = 100, iteration = p)
        poly_coords.append((round(x + center[0]),round(y + center[1])))
    return poly_coords
def parametric_Star_Points(base, center = (0,0), radius = 100, point_count = 5):
    if point_count <= 4:
        return
    poly_coords = []
    star_coords = []
    for p in range(point_count):
        x,y = polar_Coord_Gen(total = point_count, radius = 100, iteration = p)
        poly_coords.append((round(x + center[0]),round(y + center[1])))
    
    reg_Steps,degen_Steps = determine_Steps(point_count)
    step_size = random.choice(reg_Steps)
    step_num = 0
    for p in range(point_count):
        x,y = poly_coords[step_num][0],poly_coords[step_num][1]
        star_coords.append((x,y))
        step_num += step_size
        if step_num >= point_count:
            step_num -= point_count

    return star_coords
s

    svg_doc.add(svg_doc.rect(size =(draw_width,draw_height),
                            fill="none",
                            stroke ="blue",
                            stroke_width = 4
                                        
    svg_doc.add(svg_doc.polyline(points = points_To_Center_Lines(
                                        base = svg_doc, 
                                        center = get_Center(draw_width, draw_height), 
                                        point_count = 7, 
                                        poly_coords =(regular_Polygons_Points(
                                                    base = svg_doc, 
                                                    center = get_Center(draw_width, draw_height),
                                                    radius = 100,
                                                    point_count= 7))),
                                fill = "none",
                                stroke = "purple",
                                stroke_width = 2,
                                stroke_linejoin = "bevel"))
'''

    
