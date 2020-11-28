import os
import sys
from multiprocessing import Pool

import torch
import torch.nn.functional as F
import numpy as np

from path import get_dirs, DATASET_POSITIVE_CHIRPS_PATH
from satelite import CHIRPS

chirps = CHIRPS()

dirs = np.array(get_dirs(positive=True))
size = dirs.shape[0]

tensor = torch.zeros((size, chirps.get_days(), chirps.get_channels(), 224, 224))

del chirps

def extract(i):
    a_data = np.load(DATASET_POSITIVE_CHIRPS_PATH + dirs[i] + '/X.npy').astype(np.float32)
    dim = a_data.shape
    a_data = F.interpolate(torch.tensor(a_data), size=[224,224])
    tensor[i]=a_data

if __name__=='__main__':
    MAX_CORES = os.cpu_count()
    PATH_TO_BUCKET = '../../data-step/clean_dataset/'
    p = Pool(MAX_CORES)

    for i, _ in enumerate(p.imap(extract, range(size)), 1):
        sys.stderr.write('\rdone {0:%}'.format(i/size))
    p.close()

    torch.save(tensor, PATH_TO_BUCKET + 'positive/chirps.pt')
