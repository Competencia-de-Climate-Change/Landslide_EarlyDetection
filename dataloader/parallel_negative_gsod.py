import os
import sys
from multiprocessing import Pool

import torch
import torch.nn.functional as F
import numpy as np

from path import get_dirs, DATASET_NEGATIVE_GSOD_PATH
from satelite import GSOD

gsod = GSOD()

dirs = np.array(get_dirs())
size = 80

tensor = torch.zeros((size, gsod.get_days(), gsod.get_channels(), 224, 224))

del gsod

def extract(a_range):
    for i in a_range:
        a_data = np.load(DATASET_NEGATIVE_GSOD_PATH + dirs[i] + '/X.npy').astype(np.float32)
        dim = a_data.shape
        a_data = F.interpolate(torch.tensor(a_data), size=[224,224])
        tensor[i]=a_data

if __name__=='__main__':
    MAX_CORES = os.cpu_count()
    PATH_TO_BUCKET = '../../tensors/'
    p = Pool(MAX_CORES)
    
    p_args = []
    
    b = 75*int(sys.argv[1])

    for i in range(MAX_CORES):
        s = b + i*(size//MAX_CORES)
        e = b + (i+1)*(size//MAX_CORES)
        p_args.append(np.arange(s, e))
    
    p_args = np.array(p_args)

    p.imap(extract, p_args)
    p.close()

    torch.save(tensor, PATH_TO_BUCKET + f'negative/gsod/gsod{b}.pt')
