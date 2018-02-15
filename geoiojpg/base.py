import os, geoio, osr
from tempfile import NamedTemporaryFile
from shapely.geometry import box
from lxml import etree
from PIL import Image

BANDS = ['', 'Red', 'Green', 'Blue']

def mkVRT(georef, height, width, img_file):
    img_file = os.path.realpath(img_file)

    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    wkt = srs.ExportToWkt()

    root = etree.Element('VRTDataset', rasterXSize=str(width), rasterYSize=str(height))

    etree.SubElement(root, 'SRS').text = wkt

    minlon, minlat, maxlon, maxlat = georef.bounds

    # top left corner and pixel resolution
    geotransform = '%16E, %16E, %16E, %16E, %16E, %16E' % (
        minlon,
        (maxlon - minlon) / width,
        0,
        maxlat,
        0,
        -(maxlat - minlat) / height
    )

    etree.SubElement(root, 'GeoTransform').text = geotransform

    for b in range(1, 4):
        band = etree.SubElement(root, 'VRTRasterBand', dataType="Byte", band=str(b))
        etree.SubElement(band, 'NoDataValue').text = '0'
        etree.SubElement(band, 'ColorInterp').text = BANDS[b]
        source = etree.SubElement(band, 'ComplexSource')
        etree.SubElement(source, 'SourceFilename', relativeToVRT="0").text = img_file
        etree.SubElement(source, 'SourceBand').text = str(b)
        offs = {'xOff' : '0', 'yOff' : '0', 'xSize' : str(width), 'ySize' : str(height)}
        etree.SubElement(source, 'SrcRect', **offs)
        etree.SubElement(source, 'DstRect', **offs)
        etree.SubElement(source, 'NODATA').text = '0'

    return root

def GeoImage(filename, georef):
    img = Image.open(filename)
    vrt = mkVRT(georef, img.height, img.width, filename)
    with NamedTemporaryFile(suffix='.vrt') as f:
        f.write(etree.tostring(vrt))
        f.flush()
        return geoio.GeoImage(f.name)
