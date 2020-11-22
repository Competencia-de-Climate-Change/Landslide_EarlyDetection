import fsspec
import gcsfs

import pandas as pd

global_project_id = 'projectx-uch'
global_bucket_id = 'data-projectx'

# Functional API

def create_gcsfs(bucket_id=None, token_loc=None):
    """
    Create a GCSFileSystem (Google Cloud Storage File System), given a 'bucket_id'
    and 'token_loc' parameters. If anyones given, it will set by default configurations.
    """
    if bucket_id is None: bucket_id = global_bucket_id

    if token_loc is None:
        return gcsfs.GCSFileSystem(bucket_id, token='~/.config/gcloud/application_default_credentials.json')

    return gcsfs.GCSFileSystem(bucket_id, token=token_loc)

def bucket_ls(gcs, rdir=".", bucket_id=None):
    if bucket_id is None:  bucket_id = global_bucket_id

    return gcs.ls(f"{bucket_id}/{rdir}")

def bucket_get(gcs, rdir, bucket_id=None):
    if bucket_id is None: bucket_id = global_bucket_id

    return gcs.get(f"{bucket_id}/{rdir}")

def bucket_put(gcs, rdir, bucket_id=None):
    if bucket_id is None: bucket_id = global_bucket_id

    return gcs.put(f"{bucket_id}/{rdir}")

def bucket_read_csv(rdir=None, rfile=None, rfpath=None, bucket_id=None):
    if bucket_id is None: bucket_id = global_bucket_id

    if rfpath is not None:
        return pd.read_csv(f"gs://{bucket_id}/{rfpath}")
    
    return pd.read_csv(f"gs://{bucket_id}/{rdir}/{rfile}")

# API

class GCSBucket(object):

    def __init__(self, token, bucket_id=global_bucket_id, project_id=global_project_id):
        
        # Identifiers
        self._bucket= bucket_id
        self._project= project_id

        if token=='default':
            self.token= '~/.config/gcloud/application_default_credentials.json'
        else:
            self.token= token

        # Connection to GCP Bucket
        self.gcs = create_gcsfs(bucket_id, token)

    
    def ls(rdir="."):
        return bucket_ls(self.gcs, rdir, self._bucket)

    def get(rdir="."):
        return bucket_get(self.gcs, rdir, self._bucket)

    def put(rdir="."):
        return bucket_put(self.gcs, rdir, self._bucket)
    
    def read_csv(rdir, rfile):
        return bucket_read_csv(rdir, rfile, rdir, self._bucket)

    