GeoIOJpg
--------

A wrapper around [GeoIO](https://github.com/DigitalGlobe/geoio) for non-georeferenced jpg files.  Simply give the path to a jpg file and a shapely object describing the geospatial boundary of that image.

# Install

Note that GeoIO only works with python 2, therefore GeoIOJpg also has this same limitation

```
pip install geoiojpg
```

# Usage

```Python
from shapely.geometry import box
from geoiojpg import GeoImage

# Path to some satellite image in jpg format
img_file = './img.jpg'

# bounding box (somewhere in Madagascar)
boundary = box(49.482, -15.908, 49.570, -15.996)

# Create the GeoImage (this returns a regular geoio GeoImage)
geoimg = GeoImage(img_file, boundary)

print(geoimg.raster_to_proj(50, 50))
# > (49.4826462689568, -15.9084275189568)

```

# How it works

GeoIOJpg will build a [VRT](http://www.gdal.org/gdal_vrttut.html) in XML format out of the supplied metadata.  Basically, it will compute the geotransform based on the supplied shapely object and height/width of the image.  It will assume that all jpg files are in RGB format.  This will then call the GeoIO constructor with the temporary VRT file.  After the GeoIO object has been created, the temporary file is deleted.



