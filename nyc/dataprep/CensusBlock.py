#! /usr/bin/env python3
""" Gets the census block code for a given set of coordinates.

This makes use of the FCC census block lookup API, which takes
a (lat,lon) point at outputs some XML with information 
about that position.

This does not support multithreading to make sure that it does
not overload anything. The lookup process can also be very slow.

"""

from xml.etree import ElementTree
import xml.etree
import requests
import pandas as pd
import numpy as np
import sys

""" Get the location data for a given point.

Args:
    lat: The latitude in degrees 
    lon: The longitude in degrees

"""
def getdata(lat,lon):
  page = requests.get(
           "http://data.fcc.gov/api/block/2010/find?latitude={}&longitude={}"
           .format(lat,lon)
         )  

  root = ElementTree.fromstring(page.content)

  status = root.attrib['status']
  block = root[0].attrib['FIPS']  
  county = root[1].attrib['name']
  state = root[2].attrib['code']

  data= {'lat':lat,'lon':lon,'status':status,'block':block,
         'county':county,'state':state}

  return data

""" Test the script on a given point.

The point is in New Jersey.
"""
def test_write():

  data = getdata(40,-75)

  f = open('test.csv','a')
  f.write('status,block,county,state\n')
  f.write( str(data['status'])+','+str(data['block'])+','
          +str(data['county'])+','+str(data['state'])+'\n')
  f.close()

""" Get all the data in a 200x200 grid of coordinates
    surrounding NYC. This will take a long time.

Args:
    outf: The output file.
"""
def grid_of_data(outf='block_latlon.csv'):

  latmin = 40.48
  lonmin = -74.28
  latmax = 40.93
  lonmax = -73.65
  lats = np.mgrid[latmin:latmax:200j]
  lons = np.mgrid[lonmin:lonmax:200j]

  count = 0
  with open(outf,'a') as f:
    for lat in lats:
      for lon in lons:
        print(count)
        sys.stdout.flush()
        if count < 31678: 
          count += 1
          continue

        data = getdata(lat,lon)
        f.write(str(data['lat'])+','+str(data['lon'])+','
                + str(data['status'])+','+str(data['block'])
                +','+str(data['county'])+','+str(data['state'])+'\n')
        f.flush()
        count += 1

  f.close()


if __name__=='__main__':
  grid_of_data()
