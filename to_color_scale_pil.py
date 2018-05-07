#!/usr/bin/env python
# -*- coding: utf-8 -*-

import colorscale

from PIL import Image
import numpy as np

class ConversionError(NameError):
    pass

def open_image(imagename):
    return Image.open(imagename)

def convert(img, cscale):
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
    return img

def save_img_as(img, new_filename):
    img.save(new_filename)
