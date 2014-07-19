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
    def to_gray(self):
        return int(round((self.red+self.green+self.blue)/3.))
    def __str__(self):
        return "RGB value: (%d, %d, %d)" % (self.red, self.green, self.blue)
    def __iter__(self):
        for color in (self.red, self.green, self.blue): yield color
    def __getitem__(self, index):
        if index not in [0,1,2]: raise KeyError('Index must be 0, 1 or 2')
        if index == 0: return self.red
        if index == 1: return self.green
        if index == 2: return self.blue
    def __setitem__(self, index, value) :
        if index not in [0,1,2]: raise KeyError('Index must be 0, 1 or 2')
        if index == 0: self.red = value
        if index == 1: self.green = value
        if index == 2: self.blue = value

def bgr_to_rgb(bgr):
    """ Values in ndarrays are stored as BGR. """
    return (bgr[2], bgr[1], bgr[0])

class GrayToRGB(object):
    def __init__(self, palette, min=0, max=255):
        self.palette = palette
        self.min = min
        self.max = max
        self.lut = dict()
    def __call__(self, gray_value):
        try:
            return self.lut[gray_value]
        except KeyError:
            self.lut[gray_value] = self.convert_gray_to_rgb(gray_value)
            return self.lut[gray_value]
    
    def convert_gray_to_rgb(self, gray_value):
        pal = self.palette
        min, max = self.min, self.max
        if gray_value == max: return RGBValue(max, max, max)
        if gray_value < min or gray_value > max: raise ValueError('gray value must be in the limits of %d to %d.' % (min, max))
        percentage = float(gray_value)/(2**8-1)
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

class GrayToBGR(GrayToRGB):
    def __call__(self, gray_value):
        rgb = GrayToRGB.__call__(self, gray_value)
        return (rgb[2], rgb[1], rgb[0])

#import numpy
class ReverseGrayToRGB(object):
    def __init__(self, palette, min=0, max=255):
        self.palette = palette
        extent = max-min+1
        self.lut = dict()
        #numpy.zeros((extent, extent, extent), dtype=numpy.int)
        conv = GrayToRGB(palette, min=min, max=max)
        for i in range(min, max+1):
            rgb = conv(i)
            rgb = (rgb.red, rgb.green, rgb.blue)
            if rgb in self.lut: raise NameError("Cannot create reverse colour scale: non reversible colour scale / duplicate entries")
            self.lut[rgb] = i
    def __call__(self, rgb):
        return self.lut[rgb]


