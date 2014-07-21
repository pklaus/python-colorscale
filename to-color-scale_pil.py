#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import colorscale
from os import path
import argparse
from PIL import Image
import numpy as np
from itertools import product

class ConversionError(NameError):
    pass

def convert(imagename, cscale):
    img = Image.open(imagename)
    if 1 in img.size: raise NotImplementedError()
    data = np.asarray( img, dtype="uint8" )
    if data.ndim != 2: raise ConversionError("Are you sure, this is a grayscale image? - 'cause I don't think so.")
    conv = colorscale.GrayToRGB(cscale)
    cred   = np.frompyfunc(conv.get_red, 1, 1)
    cgreen = np.frompyfunc(conv.get_green, 1, 1)
    cblue  = np.frompyfunc(conv.get_blue, 1, 1)
    # http://www.socouldanyone.com/2013/03/converting-grayscale-to-rgb-with-numpy.html
    #w, h = data.shape
    #color = np.empty((w, h, 3), dtype=np.uint8)
    #color[:, :, 0] = cred(data)
    #color[:, :, 1] = cgreen(data)
    #color[:, :, 2] = cblue(data)
    color = np.dstack((cred(data).astype(data.dtype), cgreen(data).astype(data.dtype), cblue(data).astype(data.dtype)))
    img = Image.fromarray(color)
    img.save(add_to_file_name(imagename, '_color'))

def add_to_file_name(old_name, addition):
    fragments = path.splitext(old_name)
    return fragments[0] + addition + fragments[1]

palettes = dict()
palettes['tillscale'] = colorscale.TillPalette()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an image saved as false color to grayscale')
    parser.add_argument('imagename', metavar='IMAGEFILE', help='The image to convert')
    parser.add_argument('-s', '--colorscale', help='Choose from: %s'%palettes.keys(), required=True)
    args = parser.parse_args()
    convert(args.imagename, palettes[args.colorscale])
