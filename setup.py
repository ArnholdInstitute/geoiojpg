from setuptools import setup

version = "0.5"

setup(
    name='geoiojpg',
    packages=['geoiojpg'],
    version=version,
    description='A wrapper around GeoIO for non-georeferenced jpg files',
    author='Matt Le',
    author_email='lematt1991@gmail.com',
    url='https://github.com/ArnholdInstitute/geoiojpg',
    download_url='https://github.com/ArnholdInstitute/geoiojpg/archive/{0}.tar.gz'.format(version),
    keywords=['jpg', 'jpeg', 'geoio', 'geospatial'],
    classifiers=[],
    install_requires=['geoio', 'shapely']
)