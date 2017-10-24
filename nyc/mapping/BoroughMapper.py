""" BoroughMapper.py

Map positions onto NYC boroughs.
"""

__author__    = "Jeremy P. Lopez"
__date__      = "2017"
__copyright__ = "(c) 2017, Jeremy P. Lopez"

import fiona
from shapely.geometry import shape,mapping, Point, Polygon, MultiPolygon
import pandas as pd

import pyproj
import shapely.ops as ops
from functools import partial

m2_to_mi2 = 3.86102e-7

class BoroughMapper:
    """ Class to map positions onto NYC boroughs."""
    def __init__(self,path='data/boroughs.shp'):
        """ Initialize the object using a given shapefile.

        Attributes:
            regions: Data read from the file.

        """
        self.regions = fiona.open(path)
  
    def find_borough(self,lat,lon):
        """ Get the borough code given a position. """
        pt = Point(lon,lat)
        for boro in self.regions:
            if shape(boro['geometry']).contains(pt):
                code = boro['properties']['boro_code']
                return code
  
        return -1
  
    def get_region_id(self,reg):
        """Get the id for a given region in self.regions """
        return int(reg['properties']['boro_code'])
  
    def get_metadata(self):
        """Get the dataframe containing metadata for each borough
        """
        area = []
        length = []
        boro_code = []
        boro_name = []
        true_area = []
        for boro in self.regions:
            area.append(boro['properties']['shape_area'])
            length.append(boro['properties']['shape_leng'])
            boro_name.append(boro['properties']['boro_name'])
            boro_code.append(int(boro['properties']['boro_code']))
            shp = shape(boro['geometry'])
            area_tmp = ops.transform(
                         partial(
                           pyproj.transform,
                           pyproj.Proj(init='EPSG:4326'),
                           pyproj.Proj(
                             proj='aea',
                             lat1=shp.bounds[1],
                             lat2=shp.bounds[3])),
                         shp
                       ).area
      
            true_area.append(area_tmp * m2_to_mi2 )
      
        df = pd.DataFrame({'boro_name':boro_name,
                      'area':true_area,
                      'shape_area':area,
                      'shape_length':length},
                     index=boro_code)
        df.index.name = 'boro_code'
        return df
