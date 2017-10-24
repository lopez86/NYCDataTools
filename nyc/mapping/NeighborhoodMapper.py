""" BoroughMapper.py

Map positions onto NYC Neighborhood Tabulation Areas.
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

class NeighborhoodMapper:
    """ A class to map positions onto neighborhood tabulation area.

    Attributes:
        regions: The shapefile data.

    """ 

    def __init__(self,path='data/neighborhoods.shp'):
        """ Initialize the object and load data from a 
            given shapefile."""
        self.regions = fiona.open(path)

    def find_neighborhood(self,lat,lon):
        """ Find the NTA code given a latitude and longitude."""
        pt = Point(lon,lat)
        for nta in self.regions:
            if shape(nta['geometry']).contains(pt):
                code = nta['properties']['ntacode']
                return code

        return -1

    def get_region_id(self,region):
        """ Get the NTA of a given region in self.regions."""
        return region['properties']['ntacode']

    def get_metadata(self):
        """ Get a dataframe holding the metadata on the different
            regions.
        """
        area = []
        length = []
        ntacode = []
        county_fip = []
        boro_code = []
        ntaname = []
        boro_name = []
        true_area = []
        for nta in self.regions:
            area.append(nta['properties']['shape_area'])
            length.append(nta['properties']['shape_leng'])
            county_fip.append(nta['properties']['county_fip'])
            ntaname.append(nta['properties']['ntaname'])
            ntacode.append(nta['properties']['ntacode'])
            boro_name.append(nta['properties']['boro_name'])
            boro_code.append(int(nta['properties']['boro_code']))
            shp = shape(nta['geometry'])
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

        df = pd.DataFrame({'name':ntaname,
                  'area':true_area,
                  'shape_area':area,
                  'shape_length':length,
                  'county_fip':county_fip,
                  'boro_code':boro_code,
                  'boro_name':boro_name},
                 index=ntacode)
        df.index.name = 'ntacode'
        return df
