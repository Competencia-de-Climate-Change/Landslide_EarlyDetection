"""
Satelite Module 

Module that abstract interaction with satellites 

1.- Categories

The data has 4 categories, each category has satellite asociated:
    - Elevation
    - Population
    - Soil Moist
    - Weather
    
1.1.- Elevation:
    Collect Elevation data from a zone
    Satellities asociated:
        - Aster
        
1.2.- Population
    Collect Population data from a zone
    Satellities asociated:
        - Population Density v4
        
1.3.- Soil Moist:
    Collect Soil Moist data from a zone
    Satellities asociated:
        - SMAP

1.4.- Weather:
    Collect Wheater data from a zone
    Satellites asociated:
        - CFS
        - CHIRPS
        - GOES
        - GSOD
        
2.- Satelities:
    Data was collect thanks to differents satellites
    This satellites are from DescartesLab
    
2.1.- Aster Satelite:
    This satelite extract Elevation Data
    Data Channels:
        - Alpha
        - Height
        - Number of Images 
    
2.2.- Population Density v4:
    This satelite extract Population data
    Data Channels:
        - Population
        
2.3.- SMAP:
    This satelite extract Soil Moisture Data
    Data Channels:
        - AM Soil Moisture
        - PM Soil Moisture

2.4.- CFS: *
    This satelite extract Weather Snow Data
    Data Channels:
        - Albedo
        - Precision
        - Snow Depth
        - Snow Water Equivalent
        - Soil Moist 1
        - Soil Moist 2
        - Soil Moist 3 
        - Time Average
        - Time Max
        - Time Min
        - Water Runoff
        
2.5.- CHIRSP:
    This satelite extract Weather Precipitation Data
    Data Channels:
        - Daily Precipitation 

2.6.- GOES:
    This satelite extract Weather Data
    Data Channels:
        - EVI
        - NDVI
        - NDWI
        - NDWI 1
        - NDWI 2
        
2.7.- GSOD:
    This satelite extract Weather Data
    Data Channels:
        - Time Average
        - Time Max
        - Time Min
        . RH
        - Precision
"""
import numpy as np

from path import *

class Satelite():
    def __init__(self, path):
        """
        Class Satelite
        
        Inicialize a Satelite Instance
        
        
        Parameters:
        --------

        batch_size: int
            Size of Batch
            
        path: string
            Path to Satelite Data 
        """
        
        self.path = path
        
    def get_path(self):
        """
        Getter path to training data
        """
        return self.path
    
    def get_data(self):
        """
        Get X Training Data
        
        returntype: np.array
            Numpy array contains X Data
        """
        return np.load(self.get_path() + 'X.npy')
    
    def get_width(self):
        """
        Get Width data

        returntype: int
            Width of the Data Image
        """
        return self.get_x_data().shape[2]

    def get_height(self):
        """
        Get Height data

        returntype: int
            Height of the Data Image
        """
        return self.get_x_data().shape[3]

    def get_channels(self):
        """
        Get Channel length

        returntype: int
            Length of the Channel
        """
        return self.get_x_data().shape[1] 

class Aster(Satelite):
    def __init__(self):
        path = DATASET_ASTER_PATH
        super(Aster, self).__init__(path)

class CHIRPS(Satelite):
    def __init__(self):
        path = DATASET_CHIRPS_PATH
        super(CHIRPS, self).__init__(path)

class CFS(Satelite):
   def __init__(self):
        path = DATASET_CFS_PATH
        super(CFS, self).__init__(path)

class GSOD(Satelite):
   def __init__(self):
        path = DATASET_GSOD_PATH
        super(GSOD, self).__init__(path)

class SMAP(Satelite):
    def __init__(self):
        path = DATASET_SMAP_PATH
        super(SMAP, self).__init__(path)

