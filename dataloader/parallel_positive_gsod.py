import os
import sys
from multiprocessing import Pool

import torch
import torch.nn.functional as F
import numpy as np

from path import get_dirs, DATASET_POSITIVE_CFS_PATH
from satelite import gsod

gsod = GSOD()

dirs = np.array(get_dirs(positive=True))
size = 80 # Ajustar

tensor = torch.zeros((size, gsod.get_days(), gsod.get_channels(), 224, 224))

del cfs

def extract(a_range):
    for i in a_range:
        a_data = np.load(DATASET_POSITIVE_GSOD_PATH + dirs[i] + '/X.npy').astype(np.float32)
        dim = a_data.shape
        a_data = F.interpolate(torch.tensor(a_data), size=[224,224])
        tensor[i]=a_data

if __name__=='__main__':
    # Recomiendo usar size // MAX_CORES de manera que la division entera sea exacta
    # Por ejemplo 80 // 8 

    MAX_CORES = os.cpu_count()
    PATH_TO_BUCKET = '../../tensors/'
    p = Pool(MAX_CORES)
    
    p_args = []
    
    b = size*int(sys.argv[1])
    
    for i in range(MAX_CORES):
        s = b + i*(size//MAX_CORES)
        e = b + (i+1)*(size//MAX_CORES)
        p_args.append(np.arange(s, e))
    
    p_args = np.array(p_args)

    p.imap(extract, p_args)
    p.close()

    torch.save(tensor, PATH_TO_BUCKET + f'positive/gsod{b}.pt')
