import os
from multiprocessing import Pool

import torch
import torch.nn.functional as F
import numpy as np

from path import *
from satelite import Aster, CHIRPS, CFS, GSOD 

aster = Aster()
chirps = CHIRPS()
cfs = CFS()
gsod = GSOD()

positive_dirs = get_dirs(positive=True) # Get dir paths to find data
#negative_dirs = get_dirs() 

positive_size = len(positive_dirs)
#negative_size = len(negative_dirs)

#pdaster_tensor = torch.zeros((positive_size, aster.get_days(), aster.get_channels(), 224, 224))
pdchirps_tensor = torch.zeros((positive_size, chirps.get_days(), chirps.get_channels(), 224, 224))
pdcgs_tensor = torch.zeros((positive_size, cfs.get_days(), cfs.get_channels(), 224, 224))
pdgsod_tensor = torch.zeros((positive_size, gsod.get_days(), gsod.get_channels(), 224, 224))

def extract_data(range_data, directory, path, tensor):
    for i in range_data:
        file_path = path + directory[i] + '/X.npy'
        a_data = np.load(file_path).astype(np.float16)
        dim = a_data.shape
        a_data = F.interpolate(torch.tensor(a_data), size =[224,224])
        tensor[i] = a_data

positive_iter = list(range(len(positive_dirs))) 
#negative_iter = list(range(len(negative_dirs)))

if __name__=='__main__':
    MAX_CORES = os.cpu_count() 
    PATH_TO_BUCKET = '../../data-step/clean_dataset/'

    pool = Pool(MAX_CORES)

    pool_args = []
    
    for i in range(MAX_CORES):
        init = i - MAX_CORES*(i//MAX_CORES)
        s = init*(positive_size//MAX_CORES)
        e = (init+1)*(positive_size//MAX_CORES)
        #if i//10  == 0: # aster
        #    continue
        #    path = DATASET_POSITIVE_ASTER_PATH
        #    args = (positive_iter[s:e], positive_dirs, path, pdaster_tensor)
        if i//MAX_CORES  == 0: # chirps
            path = DATASET_POSITIVE_CHIRPS_PATH
            args = (positive_iter[s:e], positive_dirs, path, pdchirps_tensor)
            pool_args.append(args)
        elif i//MAX_CORES == 1: # cfs
            path = DATASET_POSITIVE_CFS_PATH
            args = (positive_iter[s:e], positive_dirs, path, pdcgs_tensor)
            pool_args.append(args)
        else: # gsod
            path = DATASET_POSITIVE_GSOD_PATH
            args = (positive_iter[s:e], positive_dirs, path, pdgsod_tensor)
            pool_args.append(args)

    pool.starmap(extract_data, pool_args)
    
    #torch.save(pdaster_tensor, 'positive_aster.pt')
    torch.save(pdchirps_tensor, PATH_TO_BUCKET + 'positive/chirps.pt')
    torch.save(pdcgs_tensor, PATH_TO_BUCKET + 'positive/cgs.pt')
    torch.save(pdgsod_tensor, PATH_TO_BUCKET +'positive/gsod.pt')

