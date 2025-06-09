from PIL import Image
from random import random

class GradientImage:
    output_width, output_height = 200, 100

    def __init__(self, start_colour: tuple, end_colour: tuple, start_name: str = None, end_name: str = None):
        self.start_col = start_colour
        self.end_col = end_colour

        self.start_name = start_name if start_name else "undefined"
        self.end_name = end_name if end_name else "undefined"
        
        self.SetData()


    def SetData(self):
        row = [(self.start_col)]

        r,g,b = self.start_col
        r1,g1,b1 = self.end_col

        for x in range(1,self.output_width):
            right_ratio = x / self.output_width
            left_ratio = 1-right_ratio
            
            this_mix = (int((r*left_ratio)+(r1*right_ratio)), int((g*left_ratio)+(g1*right_ratio)), int((b*left_ratio)+(b1*right_ratio)))
            
            row.append(this_mix)
        
        bffr = []
        for y in range(self.output_height):
            bffr.extend(row)
        
        self.buffer = bffr


    def Save(self):
        output_path = f"Gradients/{self.start_name}_{self.end_name}.png"

        self.img = Image.new("RGB", (self.output_width,self.output_height))
        self.img.putdata(self.buffer)
        self.img.save(output_path)
        self.img.close()

        print(f"Saved to: {output_path}")


RandomColour = lambda: (int(255*random()),int(255*random()),int(255*random()))


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

GradientImage(black, white, "black", "white").Save()
GradientImage(blue, red, "blue", "red").Save()

for i in range(10):
    a = RandomColour()
    b = RandomColour()
    img = GradientImage(a,b,i,i)
    img.Save()