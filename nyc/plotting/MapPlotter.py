from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
from shapely.geometry.polygon import Polygon
from shapely.geometry import shape
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy

class MapPlotter:

    def __init__(self,mapper):
        self.mapper = mapper
        self.cmap = 'inferno'
        self.nan_color = [0.7,0.7,0.7]
        self.region_list = None
        self.metadata = None

    def set_cmap(self,c):
        self.cmap = c
   
    def set_nan_color(self,c):
        self.nan_color = c

    def set_region_list(self,rl):
        self.region_list = rl

    def plot(self,values,ax,area_norm=False,color_label=""):
        if area_norm is True: 
            self.metadata = self.mapper.get_metadata()
        self._patches = []
        self._nanpatches = []
        xlimits = numpy.array([200.1,-200.1])
        ylimits = numpy.array([200.1,-200.1])
        self._value_arr = []
        for region in self.mapper.regions:
            sh = shape(region['geometry'])  
            reg_id = self.mapper.get_region_id(region)
            if self.region_list is not None and \
                 reg_id not in self.region_list:
               continue
            bounds = sh.bounds
            
            xlimits = [numpy.min([xlimits[0],bounds[0]]),
                       numpy.max([xlimits[1],bounds[2]])]
            ylimits = [numpy.min([ylimits[0],bounds[1]]),
                       numpy.max([ylimits[1],bounds[3]])]
    
            try:
                value = values[reg_id] 
                if area_norm is True:
                    value /= self.metadata.loc[reg_id,'area']
                self._value_arr.append(value)
                self._patches.append(PolygonPatch(sh))
            except:
                self._nanpatches.append(PolygonPatch(sh))
       
     
        self._p = PatchCollection(self._patches,cmap=self.cmap,alpha=0.8)
      
        self._p.set_array(numpy.array(self._value_arr))
        self._np = PatchCollection(self._nanpatches,color=self.nan_color,alpha=0.5)
        ax.add_collection(self._p)
        ax.add_collection(self._np)
        xlimits = [xlimits[0]-0.01,xlimits[1]+0.01]
        ylimits = [ylimits[0]-0.01,ylimits[1]+0.01]
        ax.set_xlim(xlimits)
        ax.set_ylim(ylimits)
        ax.set_ylabel('Latitude [deg]')
        ax.set_xlabel('Longitude [deg]')
        self.cbar = plt.colorbar(self._p,cmap=self.cmap,ax=ax)
        self.cbar.set_label(color_label,rotation=270)
