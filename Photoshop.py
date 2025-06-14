from PIL import Image
from colorsys import rgb_to_hls, hls_to_rgb
from os.path import exists
from os import mkdir

isFunction = lambda x: type(x).__name__ == "function"

class Photoshop:

    def __init__(self, img_path, mode):
        "Provide name for image stored within /Input/.\nImage will be edited with target mode and saved to output folder under the same name."
        if mode == "METHODS":
            self.__SetMethodList()
            print(self.methods)
            return
        
        self.path = f"Input/{img_path}"
        self.applied = []

        if not self.__CheckDirs():
            self.status = False
            return

        try:
            self.img = Image.open(self.path).convert("RGB")
        except Exception as e:
            print(f"Image loading failed: {e}")
            self.status = False
            return
        
        self.width, self.height = self.img.size

        if type(mode) == list:
            if len(mode) == 0:
                print("No filters provided.")
                return
            
            if mode[0] == "resize":
                if len(mode) != 3:
                    print("RESIZE USAGE: resize <NEW_WIDTH> <NEW_HEIGHT>")
                    return
                
                wid,hei = mode[1],mode[2]
                wid = int(wid)
                hei = int(hei)

                self.in_path = img_path
                self.Resize(wid,hei)
                return
            
            for fx in mode:
                try:
                    this_fx = fx.lower()
                    if not self.__MatchFX(this_fx):
                        raise Exception()
                
                except Exception as e:
                    print(e)
                    print(f"Invalid filter '{this_fx}'. No changes made.")
                    self.status = False
                    return
        
        elif type(mode) == str:
            try:
                this_fx = mode.lower()
                if not self.__MatchFX(this_fx):
                    raise Exception()
                
            except Exception as e:
                print(e)
                print(f"Invalid filter '{this_fx}'. No changes made.")
                self.status = False
                return
            
        else: # what the fuck?
            print(f"Invalid filter format: {type(mode).__name__}. Expected list or string.")
            return
                

        self.img.save(f"Output/{img_path}")
        self.status = True
        print("Done.")
        print("Filters applied:")
        [print(f"   {i}") for i in self.applied]
        self.img.close()


    def __CheckDirs(self):
        changes_made = False
        if not exists("Input/"):
            mkdir("Input/")
            changes_made = True
        if not exists("Output/"):
            mkdir("Output/")
            changes_made = True

        if changes_made:
            print("New directories have been created, please restart and try again.")
        
        return not changes_made


    def __SetMethodList(self):
        dict = Photoshop.__dict__
        ml = []
        for k, v in dict.items():
            if isFunction(v) and "__" not in k:
                ml.append(k)
        self.methods = ml


    def __MatchFX(self, m):
        match(m):
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
                m = self.__getmul()
                self.Brightness(m)

            case "blur":
                print("Blurring.")
                print("Blurring image may take longer than other filters...")
                self.Blur()

            case "nored":
                self.Remove("red")
            
            case "nogreen":
                self.Remove("green")

            case "noblue":
                self.Remove("blue")

            case _:
                print(f"Unknown filter: {m}")
                self.status = False
                return False
        
        self.applied += [m]
        return True


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
        m = self.width // 2
        m += int(m % 2 == 0)
        for x in range(m):
            for y in range(self.height):

                dx = (m) - x
                new_x = self.width - dx

                current_pixel = self.img.getpixel((x,y))
                new_pixel = self.img.getpixel((new_x, y))

                self.img.putpixel((x, y), new_pixel)
                self.img.putpixel((new_x, y), current_pixel)


    def Flip(self):
        buff = list(self.img.getdata())

        mid = len(buff) // 2

        mid += int(mid % 2 == 0)

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


    def __getmul(self):
        try:
            x = float(input("Enter brightness multiplier: "))
            return x
        except:
            return self.getmul()
    

    def __Clamp(val, a, b):
        if val < a:
            return a
        
        if val > b:
            return b
        
        return val


    def __GetSums(self, ox, oy, rx, ry):
        "'Blur' Util function"
        c = Photoshop.__Clamp

        sx = c(int(ox-(rx/2)), 0, self.width)
        ex = c(sx+rx, 0, self.width)
        sy = c(int(oy-(ry/2)), 0, self.height)
        ey = c(sy+ry, 0, self.height)

        sum_red = 0
        sum_green = 0
        sum_blue = 0

        for iy in range(sy, ey):
            for ix in range(sx, ex):
                if not (ix == ox and iy == oy):
                    r,g,b = self.img.getpixel((ix,iy))
                    sum_red += r
                    sum_green += g
                    sum_blue += b
        
        iters = ((ex - sx) * (ey - sy)) - 1 # minus the center pixel

        avg_red = int(sum_red // iters)
        avg_green = int(sum_green // iters)
        avg_blue = int(sum_blue // iters)

        return (avg_red, avg_green, avg_blue)


    def Blur(self):
        tmp_buffer = []

        x_range = 5
        y_range = 5

        for y in range(self.height):
            for x in range(self.width):
                avg_red, avg_green, avg_blue = self.__GetSums(x,y,x_range,y_range)
                new_pixel = (avg_red, avg_green, avg_blue)
                tmp_buffer.append(new_pixel)
        
        self.img.putdata(tmp_buffer)


    def Remove(self, colour):
        bffr = list(self.img.getdata())

        match (colour):
            case ("red"):
                new_bffr = [(0,g,b) for r,g,b in bffr]
            case ("green"):
                new_bffr = [(r,0,b) for r,g,b in bffr]
            case ("blue"):
                new_bffr = [(r,g,0) for r,g,b in bffr]
        
        self.img.putdata(new_bffr)
    

    def Resize(self, new_wid, new_hei):
        new_img_bffr = []
        
        for iy in range(new_hei):
            for ix in range(new_wid):
                
                tmp_x = int((ix/new_wid)*self.width)
                tmp_y = int((iy/new_hei)*self.height)
               
                pxl = self.img.getpixel((tmp_x,tmp_y))                
                
                new_img_bffr.append(pxl)
        
        new_img = Image.new("RGB", (new_wid,new_hei))
        new_img.putdata(new_img_bffr)
        new_img.save(f"Output/{self.in_path}")

        print("Resize Complete.")
        self.status = True
        self.img.close()