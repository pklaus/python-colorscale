#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import colorscale

from os import path
import argparse

def convert_and_save(imagename, cscale, backend=None):
    """ convenience function """
    if backend == 'pil':
        from .to_color_scale_pil import open_image, convert, save_img_as
    elif backend == 'cv2':
        from .to_color_scale_cv2 import open_image, convert, save_img_as
    else:
        raise NotImplementedError('No such backend: ' + backend)
    img = open_image(imagename)
    img = convert(img, cscale)
    save_img_as(img, add_to_file_name(imagename, '_color'))

def add_to_file_name(old_name, addition):
    fragments = path.splitext(old_name)
    return fragments[0] + addition + fragments[1]

palettes = {
  'tillscale': colorscale.TillPalette(),
}

def main():
    parser = argparse.ArgumentParser(description='Convert an image saved as false color to grayscale')
    parser.add_argument('imagename', metavar='IMAGEFILE', help='The image to convert')
    parser.add_argument('-s', '--colorscale', choices=palettes.keys(), help='Desired color scale', required=True)
    parser.add_argument('-b', '--backend', choices=('pil', 'cv2'), default='pil')
    args = parser.parse_args()
    convert_and_save(args.imagename, palettes[args.colorscale], backend=args.backend)

if __name__ == '__main__': main()
