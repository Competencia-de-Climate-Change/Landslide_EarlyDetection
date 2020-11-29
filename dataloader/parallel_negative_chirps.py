import os
import sys
from multiprocessing import Pool

import torch
import torch.nn.functional as F
import numpy as np

from path import get_dirs, DATASET_NEGATIVE_CHIRPS_PATH
from satelite import CHIRPS

chirps = CHIRPS()

dirs = np.array(get_dirs())
size = 160

tensor = torch.zeros((size, chirps.get_days(), chirps.get_channels(), 224, 224))

del chirps

def extract(a_range, a_dirs, a_tensor, size):
    for i in a_range:
        a_data = np.load(DATASET_NEGATIVE_CHIRPS_PATH + a_dirs[i] + '/X.npy').astype(np.float32)
        a_data = F.interpolate(torch.tensor(a_data), size=[224,224])
        try:
            a_tensor[i%size]=a_data
        except:
            continue

if __name__=='__main__':
    MAX_CORES = os.cpu_count()
    PATH_TO_BUCKET = '../../data-step/processed_data/'
    p = Pool(MAX_CORES)
    
    p_args= [] 
    
    b = size*int(sys.argv[1])
    
    for i in range(MAX_CORES):
        s = b + i*(size//MAX_CORES)
        e = b + (i+1)*(size//MAX_CORES)
        p_args.append((np.arange(s,e), dirs, tensor, size))

    p.starmap(extract, p_args)
    p.close()
    torch.save(tensor, PATH_TO_BUCKET + f'negative/chirps/chirps{b}.pt')
