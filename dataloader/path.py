"""
Path Module

Module that deal with all dataset paths
If DEBUG is True, then paths gonna point to local repository path
Else, gonna point to Google Cloud Storage Path
"""
import os

DATASET_POSITIVE_ASTER_PATH = '../../data-step/dataset/aster/'
DATASET_POSITIVE_CHIRPS_PATH = '../../data-step/dataset/chirps/'
DATASET_POSITIVE_CFS_PATH = '../../data-step/dataset/cfs/'
DATASET_POSITIVE_GSOD_PATH = '../../data-step/dataset/gsod/'
DATASET_POSITIVE_SMAP_PATH = '../../data-step/dataset/smap/'

DATASET_NEGATIVE_ASTER_PATH = '../../data-step/dataset/negative/aster/'
DATASET_NEGATIVE_CHIRPS_PATH = '../../data-step/dataset/negative/chirps/'
DATASET_NEGATIVE_CFS_PATH = '../../data-step/dataset/negative/cfs/'
DATASET_NEGATIVE_GSOD_PATH = '../../data-step/dataset/negative/gsod/'
DATASET_NEGATIVE_SMAP_PATH = '../../data-step/dataset/negative/smap/'


def generate_dirs(chirps, cfs, gsod):
    #aster_inter_chirps = list(set(aster).intersection(chirps))
    #cfs_inter_gsod = list(set(cfs).intersection(gsod))
    #dirs = list(set(aster_inter_chirps).intersection(cfs_inter_gsod))
    chirps_inter_cfs = list(set(chirps).intersection(cfs))
    dirs = list(set(chirps_inter_cfs).intersection(gsod))
    dirs.sort()
    
    return dirs

def get_dirs(positive=False):
    #aster = os.listdir(DATASET_POSITIVE_ASTER_PATH) if positive else []
    chirps = os.listdir(DATASET_POSITIVE_CHIRPS_PATH) if positive else os.listdir(DATASET_NEGATIVE_CHIRPS_PATH)
    cfs = os.listdir(DATASET_POSITIVE_CFS_PATH) if positive else os.listdir(DATASET_NEGATIVE_CFS_PATH)
    gsod = os.listdir(DATASET_POSITIVE_GSOD_PATH) if positive else os.listdir(DATASET_NEGATIVE_GSOD_PATH)
     
    return generate_dirs(chirps, cfs, gsod)
        
    
