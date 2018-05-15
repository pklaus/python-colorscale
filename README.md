### Python package colorscale

This package was written to facilitate working with 'false color'. Many scientific fields work with image files to visualize two-dimensional scalar data. The raw data can then be represented as a grayscale image. For different reasons, representing these data in false color can be useful. **This package helps to convert grayscale images to 'false color'.** On the other hand, quite often it is desirable to have access to the original values of a false color plot. If the color scale (or 'color map') is known and it is bijective (a reversible one to one mapping), the original gray scale image can be recovered from the false color image using this tool, too.

### Installation

    pip install colorscale

### Usage

After installing, two command line tools will be available:

* `to_color_scale` and
* `to_gray_scale`.

Start them with the `--help` flag to learn how to use them:

    $ to_color_scale --help
    usage: to_color_scale [-h] -s {tillscale} [-b {pil,cv2}] IMAGEFILE
    
    Convert an image saved as false color to grayscale
    
    positional arguments:
      IMAGEFILE             The image to convert
    
    optional arguments:
      -h, --help            show this help message and exit
      -s {tillscale}, --colorscale {tillscale}
                            Desired color scale
      -b {pil,cv2}, --backend {pil,cv2}

and

    $ to_gray_scale --help
    usage: to_gray_scale [-h] -s COLORSCALE IMAGEFILE
    
    Convert an image saved as false color to grayscale
    
    positional arguments:
      IMAGEFILE             The image to convert
    
    optional arguments:
      -h, --help            show this help message and exit
      -s COLORSCALE, --colorscale COLORSCALE {tillscale}
                            Desired color scale

### ToDo

It is desirable (and on the ToDo list) to make this package work with the colormaps built into matplotlib.
Here's a list of the relevant matplotlib documentation pages:

* [List of matplotlib colormaps](https://matplotlib.org/examples/color/colormaps_reference.html)
* [Builtin colormaps module `matplotlib.cm`](https://matplotlib.org/api/cm_api.html)
* [base class `matplotlib.colors.Colormap`](https://matplotlib.org/api/_as_gen/matplotlib.colors.Colormap.html#matplotlib.colors.Colormap)
* [Colormaps tutorial (in-depth discussion about colormaps, including colorblind-friendliness)](https://matplotlib.org/tutorials/colors/colormaps.html)

### Resources

* Package in Python Package Index (PyPI): <https://pypi.org/project/colorscale/>
* Package on Github: <https://github.com/pklaus/python_colorscale>

### Author

* Philipp Klaus  
  <philipp.l.klaus@web.de>
