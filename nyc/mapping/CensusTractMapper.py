""" BoroughMapper.py

Map positions onto NYC 2010 census tracts.
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

class CensusTractMapper:
    """ Class to map positions onto census tracts."""
    def __init__(self,path='data/census_tracts.shp'):
        """ Initialize the object given a path to the shapefile.

        Attributes:
            regions: Census tract information read from the file.
            boros: A map from borough name to census tract code.

        """
        self.regions = fiona.open(path)
        self.boros = {'Manhattan':'36061','Brooklyn':'36047',
                      'Bronx':'36005','Queens':'36081',
                      'Staten Island':'36085'}

    def get_region_id(self,region):
        """ Get the ID code for a given region from self.regions."""
        ct = region['properties']['ct2010']
        boro = self.boros[region['properties']['boro_name']]
        tract_num = boro+ct

        return int(tract_num)

    def find_tract(self,lat,lon):
        """ Find the tract code for the given position."""
        pt = Point(lon,lat)
        for tract in self.regions:
            if shape(tract['geometry']).contains(pt):
                ct = tract['properties']['ct2010']
                boro = self.boros[tract['properties']['boro_name']]
                tract_num = boro+ct

                return int(tract_num)

        return -1


    def get_metadata(self):
      """ Get a dataframe holding metadata for the different
          census tracts.
      """
      area = []
      length = []
      ntacode = []
      ntaname = []
      ctlabel = []
      boro_code = []
      boro_name = []
      true_area = []
      cdeligibility = []
      boro_ct2010 = []
      ct2010 = []
      puma = []
      tract_code = []
      for tract in self.regions:
          area.append(tract['properties']['shape_area'])
          length.append(tract['properties']['shape_leng'])
          ntacode.append(tract['properties']['ntaname'])
          ntaname.append(tract['properties']['ntacode'])
          ctlabel.append(tract['properties']['ctlabel'])
          ct2010.append(tract['properties']['ct2010'])
          boro_ct2010.append(tract['properties']['boro_ct201'])
          boro_name.append(tract['properties']['boro_name'])
          boro_code.append(tract['properties']['boro_code'])
          cdeligibility.append(tract['properties']['cdeligibil'])
          puma.append(tract['properties']['puma'])
          #
          ct = tract['properties']['ct2010']
          boro = self.boros[tract['properties']['boro_name']]
          tract_num = boro+ct
          tract_code.append(int(tract_num))
          # Get tract area
          shp = shape(tract['geometry'])
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
  
      df = pd.DataFrame({'ctlabel':ctlabel,
                    'area':true_area,
                    'shape_area':area,
                    'shape_length':length,
                    'ct2010':ct2010,
                    'boro_ct2010':boro_ct2010,
                    'boro_code':boro_code,
                    'boro_name':boro_name,
                    'ntacode':ntacode,
                    'ntaname':ntaname,
                    'cdeligibility':cdeligibility,
                    'puma':puma},
                   index=tract_code)
      df.index.name = 'tract_code'
      return df
