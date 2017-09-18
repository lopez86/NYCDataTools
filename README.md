# NYCDataTools
This package is intended to provide some useful tools for analyzing data
about New York City. I include here some data files and Python code
to use the data.

Current features are:

  -Mapping latitude and longitude to borough, neighborhood, and census tract.

  -Making plots of data arranged by these three geographic types.

The current features allow one to compare geospatial data from NYC to demographic features at the census tract (typical population of several thousand residents) level.

## Data used here

So far, the data files included here are:

  -A selection of ACS (US Census) estimates

Census data is from the federal government and thus is public open source data not subject to copyright within the US.

The copyright status of the NYC geospatial data for the different geographic regions is less clear, so I have not included it here. You can find that at the NYC Open Data site at:

2010 Census Tracts:
https://data.cityofnewyork.us/api/geospatial/fxpq-c8ku?method=export&format=Shapefile

NTAs:
https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=Shapefile

Boroughs:
https://data.cityofnewyork.us/api/geospatial/tqmj-j8zm?method=export&format=Shapefile

If you remove the part after the ?, you can download these in other formats (KML, KMZ, GeoJSON, etc).  There are also additional maps including water areas.
