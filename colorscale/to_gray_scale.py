#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import colorscale

import cv2

from itertools import product
from os import path
import argparse

def convert(imagename, cscale):
    img = cv2.imread(imagename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    conv = colorscale.ReverseGrayToRGB(cscale)
    line, row = gray.shape
    # http://stackoverflow.com/a/13004147
    for pos in product(range(line), range(row)):
        rgb = (img.item(pos+(2,)), img.item(pos+(1,)), img.item(pos+(0,)))
        gray[pos] = conv(rgb)
    cv2.imwrite(add_to_file_name(imagename, '_gray'), gray)

def add_to_file_name(old_name, addition):
    fragments = path.splitext(old_name)
    return fragments[0] + addition + fragments[1]

palettes = dict()
palettes['tillscale'] = colorscale.TillPalette()

def main():
    parser = argparse.ArgumentParser(description='Convert an image saved as false color to grayscale')
    parser.add_argument('imagename', metavar='IMAGEFILE', help='The image to convert')
    parser.add_argument('-s', '--colorscale', choices=palettes.keys(), help='Desired color scale', required=True)
    args = parser.parse_args()
    convert(args.imagename, palettes[args.colorscale])

if __name__ == '__main__': main()
