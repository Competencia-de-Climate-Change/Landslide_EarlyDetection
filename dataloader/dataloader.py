"""
DataLoader Module

Module that give data from Satelite Module

More information about Satelite Module in satelite.py

"""
from satelite import Aster, CHIRPS, CFS, GSOD, SMAP

import numpy as np

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
                Aster(), 
                CHIRPS(), 
                CFS(), 
                GSOD(), 
                SMAP()
        ])

    def get_satellites(self):
        """
        Get an array of available satellites

        returntype: np.array
            Numpy array of Satellites
        """
        
        return self.satellites
       
    def create_dataset(self):
        """
        Create and return a dataset

        returntype: np.array
            Dataset
        """
        pass
