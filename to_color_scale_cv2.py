#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import cv2
import colorscale

def open_image(imagename):
    return cv2.imread(imagename, -1)

def convert(img, cscale):
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    conv = colorscale.GrayToBGR(cscale)
    line, row = img.shape
    from itertools import product
    # http://stackoverflow.com/a/13004147
    for pos in product(range(line), range(row)):
        color[pos] = list(conv(img.item(pos)))
    return color

def save_img_as(img, new_filename):
    cv2.imwrite(new_filename, img)
