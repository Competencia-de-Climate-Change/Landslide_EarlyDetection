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
import os

import torch
import torch.nn.functional as F
import numpy as np

from path import *

class Satelite():
    def __init__(self, positive_path, negative_path, name):
        """
        Class Satelite
        
        Inicialize a Satelite Instance
        
        
        Parameters:
        --------
        
        path: string
            Path to Satelite Data 
            
        name: string
            Name of satelite
        """
        
        self.positive_path = positive_path
        self.negative_path = negative_path
        self.name = name
            
    def get_name(self):
        """
        Get name of satelite
        """
        
        return self.name
    
    def get_positive_path(self):
        """
        Getter path to training data
        """
        return self.positive_path
    
    def get_negative_path(self):
        
        return self.negative_path
    
    def get_sample_data(self):
        dirs = get_dirs()
        path_to_sample = self.get_negative_path() + dirs[0] + '/X.npy'
        
        return np.load(path_to_sample).astype(np.float32)
    
    
    def get_days(self):
        return self.get_sample_data().shape[0]
    
    def get_data_by_cluster(self, cluster=False):
        """
        Create a Dataset by Cluster
        
        Parameters:
        
        cluster: boolean
            If True, return Positive Landslide dataset
            If False, return Negative Landslide dataset
            
        returntype: tensor
            Tensor with dataset.
        
        """
        
        dirs = get_dirs(positive=cluster)
        
        path = self.get_positive_path() if cluster else self.get_negative_path()
        size = len(dirs)
        
        data_tensor = torch.zeros((size, self.get_days(), self.get_channels(), 224, 224))
        
        progress = 0
        for i, directory in enumerate(dirs): # O(n)
            path_file = path + directory + '/X.npy'
            a_data = np.load(path_file).astype(np.float32) # X.npy (9, c, w, h)
            dim = a_data.shape
            a_data = F.interpolate(torch.tensor(a_data), size=[224, 224])
            assert(a_data.shape == (dim[0], dim[1], 224, 224))
            data_tensor[i] = a_data
            progress += 1
            percentage = round(progress/size * 100, 2)
            print(f"{self.get_name()}: loading data: {percentage}%", end='\r')
       
        return data_tensor
        
        
    def get_positive_data(self):
        return self.get_data_by_cluster(cluster=True)
    
    def get_negative_data(self):
        return self.get_data_by_cluster()
        
            
    def get_dirs(self):
        return [f.path for f in os.scandir(self.get_path()) if f.is_dir()]
    
    def get_width(self):
        """
        Get Width data

        returntype: int
            Width of the Data Image
        """
        return self.get_sample_data().shape[2] 

    def get_height(self):
        """
        Get Height data

        returntype: int
            Height of the Data Image
        """
        return self.get_sample_data().shape[3] 

    def get_channels(self):
        """
        Get Channel length

        returntype: int
            Length of the Channel
        """
        return self.get_sample_data().shape[1] 

class Aster(Satelite):
    def __init__(self):
        positive_path = DATASET_POSITIVE_ASTER_PATH
        negative_path = DATASET_NEGATIVE_ASTER_PATH
        super(Aster, self).__init__(positive_path, negative_path, 'aster')

class CHIRPS(Satelite):
    def __init__(self):
        positive_path = DATASET_POSITIVE_CHIRPS_PATH
        negative_path = DATASET_NEGATIVE_CHIRPS_PATH
        super(CHIRPS, self).__init__(positive_path, negative_path, 'chirps')

class CFS(Satelite):
    def __init__(self):
        positive_path = DATASET_POSITIVE_CFS_PATH
        negative_path = DATASET_NEGATIVE_CFS_PATH
        super(CFS, self).__init__(positive_path, negative_path, 'cfs')

class GSOD(Satelite):
    def __init__(self):
        positive_path = DATASET_POSITIVE_GSOD_PATH
        negative_path = DATASET_NEGATIVE_GSOD_PATH
        super(GSOD, self).__init__(positive_path, negative_path, 'gsod')

class SMAP(Satelite):
    def __init__(self):
        positive_path = DATASET_POSITIVE_SMAP_PATH
        negative_path = DATASET_NEGATIVE_SMAP_PATH
        super(SMAP, self).__init__(positive_path, negative_path, 'smap')

