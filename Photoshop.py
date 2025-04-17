from PIL import Image
from colorsys import rgb_to_hls, hls_to_rgb

class Photoshop:
    def __init__(self, img_path, mode):
        "Provide name for image stored within /Input/.\nImage will be edited with target mode and saved to output folder under the same name."
        self.path = f"Input/{img_path}"

        try:
            self.img = Image.open(self.path).convert("RGB")
        except Exception as e:
            print(f"Image loading failed: {e}")
            self.status = False
            return
        
        self.width, self.height = self.img.size
        
        self.buffer = list(self.img.getdata())

        match(mode.lower()):
            case "greyscale":
                self.Greyscale()
            
            case "sepia":
                self.Sepia()

            case "invert":
                self.Inverted()

            case "oppose":
                self.Opposed()

            case "spotlight":
                self.Spotlight()

            case "flip":
                self.Flip()

            case "flipx":
                self.Flip_x()

            case "mirror":
                self.Mirror()

            case "mirrorx":
                self.Mirror_x()

            case "rotate":
                self.Rotate()

            case "rotate2":
                self.Rotate(True)

            case "brightness":
                m = self.getmul()
                self.Brightness(m)

            case _:
                print(f"Unknown filter: {mode}")
                self.status = False
                return

        self.img.save(f"Output/{img_path}")
        self.status = True
        print("Done.")
        self.img.close()
    

    def Greyscale(self):
        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))

                avg = (this_red + this_green + this_blue) // 3

                new_red = avg
                new_green = avg
                new_blue = avg

                new_pixel = (new_red, new_green, new_blue)
                self.img.putpixel((x,y), new_pixel)


    def Sepia(self):
        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))

                new_red = int((0.393 * this_red) + (0.769 * this_green) + (0.189 * this_blue))
                new_green = int((0.349 * this_red) + (0.686 * this_green) + (0.168 * this_blue))
                new_blue = int((0.272 * this_red) + (0.534 * this_green) + (0.131 * this_blue))

                new_pixel = (new_red, new_green, new_blue)
                self.img.putpixel((x, y), new_pixel)


    def Inverted(self):
        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))

                new_red = 255 - this_red
                new_green = 255 - this_green
                new_blue = 255 - this_blue

                new_pixel = (new_red, new_green, new_blue)
                self.img.putpixel((x,y), new_pixel)

    
    def Opposed(self):
        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))
                
                try:
                    hue, light, sat = rgb_to_hls(this_red, this_green, this_blue)
                except ZeroDivisionError:
                    hue = 0
                    light = 0
                    sat = 0

                hue = (hue + 0.42) % 1.0


                new_red, new_green, new_blue = hls_to_rgb(hue, light, sat)

                new_red = int(new_red)
                new_green = int(new_green)
                new_blue = int(new_blue)

                new_pixel = (new_red, new_green, new_blue)
                self.img.putpixel((x,y), new_pixel)


    def Spotlight(self):
        ox = self.width // 2
        oy = self.height // 2

        light_rad = 0.6

        rx = ox * light_rad
        ry = oy * light_rad

        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))

                dx = x - ox
                dy = y - oy

                ratio = (((dx*dx) / (rx*rx)) + ((dy*dy) / (ry*ry))) ** 0.5

                if ratio >= 1:

                    new_red = int(this_red // ratio)
                    new_green = int(this_green // ratio)
                    new_blue = int(this_blue // ratio)

                    new_pixel = (new_red, new_green, new_blue)
                    self.img.putpixel((x,y), new_pixel)

    
    def Mirror_x(self):
        for x in range(self.width // 2):
            for y in range(self.height):

                pixel = self.img.getpixel((x, y))

                opposite_x = self.width - 1 - x
                opposite_pixel = self.img.getpixel((opposite_x, y))

                self.img.putpixel((x, y), opposite_pixel)
                self.img.putpixel((opposite_x, y), pixel)
                

    def Mirror(self):
        for x in range(self.width):
            for y in range(self.height // 2):

                pixel = self.img.getpixel((x, y))

                opposite_y = self.height - 1 - y
                opposite_pixel = self.img.getpixel((x, opposite_y))

                self.img.putpixel((x, y), opposite_pixel)
                self.img.putpixel((x, opposite_y), pixel)


    def Flip_x(self):
        for x in range(self.width // 2):
            for y in range(self.height):

                dx = (self.width // 2) - x
                new_x = self.width - 1 - dx

                current_pixel = self.img.getpixel((x,y))
                new_pixel = self.img.getpixel((new_x, y))

                self.img.putpixel((x, y), new_pixel)
                self.img.putpixel((new_x, y), current_pixel)


    def Flip(self):
        buff = self.buffer

        mid = len(buff) // 2

        a = buff[:mid]
        b = buff[mid:]
        
        buff = b + a

        for x in range(self.width):
            for y in range(self.height):

                idx = x + (self.width * y)
                pixel = buff[idx]
                self.img.putpixel((x,y), pixel)


    def Rotate(self, r=False):
        new_img = self.img.resize((self.height, self.width))
        
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.img.getpixel((x, y))
                new_coord = ((-y - 1 if self.height % 2 == 0 else 0) if r else y, x)
                new_img.putpixel(new_coord, pixel)
        
        self.img = new_img


    def Brightness(self, multiplier):
        for x in range(self.width):
            for y in range(self.height):

                this_red, this_green, this_blue = self.img.getpixel((x, y))
                
                new_red = int((this_red * multiplier) % 256)
                new_green = int((this_green * multiplier) % 256)
                new_blue = int((this_blue * multiplier) % 256)

                new_pixel = (new_red, new_green, new_blue)
                self.img.putpixel((x,y), new_pixel)


    def getmul(self):
        try:
            x = float(input("Enter brightness multiplier: "))
            return x
        except:
            return self.getmul() 