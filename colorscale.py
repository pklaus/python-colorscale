class Palette(object):
    table = []
    @property
    def stops(self):
        return self.table[0]
    @property
    def red(self):
        return self.table[1]
    @property
    def green(self):
        return self.table[2]
    @property
    def blue(self):
        return self.table[3]

class TillPalette(Palette):
    table = [ [0.0, 0.05, 0.30, 0.70, 1.00], # stops
              [0.0, 0.50, 0.00, 0.99, 0.99], # red
              [0.0, 0.99, 0.00, 0.00, 0.99], # green
              [0.0, 0.99, 0.99, 0.00, 0.00], # blue
            ]

class RGBValue(object):
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue
    def to_grey(self):
        print int((self.red+self.green+self.blue)/3.)
    def __str__(self):
        return "RGB value: (%d, %d, %d)" % (self.red, self.green, self.blue)
    def __iter__(self):
        return (self.red, self.green, self.blue)

def bgr_to_rgb(bgr):
    """ Values in ndarrays are stored as BGR. """
    return (bgr[2], bgr[1], bgr[0])

class GreyToRGB(object):
    def __init__(self, palette, min=0, max=255):
        self.palette = palette
        self.min = min
        self.max = max
        self.lut = dict()
    def __call__(self, grey_value):
        try:
            return self.lut[grey_value]
        except KeyError:
            self.lut[grey_value] = self.convert_grey_to_rgb(grey_value)
            return self.lut[grey_value]
    
    def convert_grey_to_rgb(self, grey_value):
        pal = self.palette
        min, max = self.min, self.max
        if grey_value == max: return RGBValue(max, max, max)
        if grey_value < min or grey_value > max: raise ValueError('grey value must be in the limits of %d to %d.' % (min, max))
        percentage = float(grey_value)/(2**8-1)
        stop = 0
        while stop < len(pal.stops)-1 and percentage >= pal.stops[stop]:
            stop += 1
        x = percentage - pal.stops[stop-1]
        # red
        k = (pal.red[stop] - pal.red[stop - 1]) / (pal.stops[stop] - pal.stops[stop - 1])
        y0 = pal.red[stop - 1]
        red = k * x + y0
        # green
        k = (pal.green[stop] - pal.green[stop - 1]) / (pal.stops[stop] - pal.stops[stop - 1])
        y0 = pal.green[stop - 1]
        green = k * x + y0
        # blue
        k = (pal.blue[stop] - pal.blue[stop - 1]) / (pal.stops[stop] - pal.stops[stop - 1])
        y0 = pal.blue[stop - 1]
        blue = k * x + y0
        # convert to (min, max):
        red = int((max-min)*red+.5)
        green = int((max-min)*green+.5)
        blue = int((max-min)*blue+.5)
        rgbval = RGBValue(red, green, blue)
        return rgbval

#import numpy
class ReverseGreyToRGB(object):
    def __init__(self, palette, min=0, max=255):
        self.palette = palette
        extent = max-min+1
        self.lut = dict()
        #numpy.zeros((extent, extent, extent), dtype=numpy.int)
        conv = GreyToRGB(palette, min=min, max=max)
        for i in range(min, max+1):
            rgb = conv(i)
            rgb = (rgb.red, rgb.green, rgb.blue)
            if rgb in self.lut: raise NameError("Cannot create reverse colour scale: non reversible colour scale / duplicate entries")
            self.lut[rgb] = i
    def __call__(self, rgb):
        return self.lut[rgb]


