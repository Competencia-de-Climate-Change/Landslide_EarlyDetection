"""
Path Module

Module that deal with all dataset paths
If DEBUG is True, then paths gonna point to local repository path
Else, gonna point to Google Cloud Storage Path
"""
import os

DATASET_POSITIVE_CHIRPS_PATH = '../../data-step/dataset/chirps/'
DATASET_POSITIVE_CFS_PATH = '../../data-step/dataset/cfs/'
DATASET_POSITIVE_GSOD_PATH = '../../data-step/dataset/gsod/'

DATASET_NEGATIVE_CHIRPS_PATH = '../../data-step/dataset/negative/chirps/'
DATASET_NEGATIVE_CFS_PATH = '../../data-step/dataset/negative/cfs/'
DATASET_NEGATIVE_GSOD_PATH = '../../data-step/dataset/negative/gsod/'


def generate_dirs(chirps, cfs, gsod):
    chirps_inter_cfs = list(set(chirps).intersection(cfs))
    dirs = list(set(chirps_inter_cfs).intersection(gsod))
    dirs.sort()
    
    return dirs

def get_dirs(positive=False):
    chirps = os.listdir(DATASET_POSITIVE_CHIRPS_PATH) if positive else os.listdir(DATASET_NEGATIVE_CHIRPS_PATH)
    cfs = os.listdir(DATASET_POSITIVE_CFS_PATH) if positive else os.listdir(DATASET_NEGATIVE_CFS_PATH)
    gsod = os.listdir(DATASET_POSITIVE_GSOD_PATH) if positive else os.listdir(DATASET_NEGATIVE_GSOD_PATH)
     
    return generate_dirs(chirps, cfs, gsod)
        
    
