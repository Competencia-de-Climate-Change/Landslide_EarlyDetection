"""
DataLoader Module

Module that give data from Satelite Module

More information about Satelite Module in satelite.py

"""
from satelite import CHIRPS, CFS, GSOD, Aster

import numpy as np
import torch 

class DataLoader():

    def __init__(self):
        """
        Class DataLoader
        Create a Valid DataSet to CNN LSTM Model

        Parameters:

        batch_size: int
            Length of batch

        """
        self.satellites = np.array([ # There is a better way to do this. 
                CHIRPS(),
                CFS(),
                GSOD(),
		Aster(),
        ])

    def get_satellites(self):
        """
        Get an array of available satellites

        returntype: np.array
            Numpy array of Satellites
        """
        
        return self.satellites
       
    def get_data_from_satellites_by_cluster(self, cluster=False):
        data = []
        for satelite in self.get_satellites():
            if cluster:
                data.append(satelite.get_negative_data())
            else:
                data.append(satelite.get_positive_data())
        return data
    
        
    def get_positive_data_from_satellites(self):
        return self.get_data_from_satellites_by_cluster(cluster=True)
    
    def get_negative_data_from_satellites(self):
        return self.get_data_from_satellites_by_cluster()
    
    def create_dataset_by_cluster(self, cluster=False):
        data = self.get_positive_data_from_satellites() if cluster else self.get_negative_data_from_satellites()
        final_data = torch.cat(data, 2)
        
        return final_data
    
    def create_positive_dataset(self):
        return self.create_dataset_by_cluster(cluster=True)
    
    def create_negative_dataset(self):
        return self.create_dataset_by_cluster()
