"""
Path Module

Module that deal with all dataset paths
If DEBUG is True, then paths gonna point to local repository path
Else, gonna point to Google Cloud Storage Path
"""

DEBUG = True

DATASET_ASTER_PATH = '/data-projectx/dataset/aster/'
DATASET_CHIRPS_PATH = '/data-projectx/dataset/chirps/'
DATASET_CFS_PATH = '/data-projectx/dataset/cfs/'
DATASET_GSOD_PATH = '/data-projectx/dataset/gsod/'
DATASET_SMAP_PATH = '/data-projectx/dataset/smap/'

if DEBUG: # There is a better way to do this xd
    DATASET_ASTER_PATH = '../datatest/aster/'
    DATASET_CHIRPS_PATH = '../datatest/chirps/'
    DATASET_CFS_PATH = '../datatest/cfs/'
    DATASET_GSOD_PATH = '../datatest/gsod/'
    DATASET_SMAP_PATH = '../datatest/smap/'

