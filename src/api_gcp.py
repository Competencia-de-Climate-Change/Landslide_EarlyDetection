import gcsfs
import pandas as pd
import os

HOME_ENV = os.environ['HOME']

GLOBAL_PROJECT_ID = 'projectx-uch'
GLOBAL_BUCKET_ID = 'data-projectx'

# Functional API
def create_gcsfs(bucket_id=None, token_loc=None):
    """
    Create a GCSFileSystem (Google Cloud Storage File System), given a 'bucket_id'
    and 'token_loc' parameters. If anyones given, it will set by default configurations.
    """
    if bucket_id is None: bucket_id = GLOBAL_BUCKET_ID

    if token_loc is None:
        return gcsfs.GCSFileSystem(
            bucket_id, 
            token=f'{HOME_ENV}/gcloud/application_default_credentials.json'
            )

    return gcsfs.GCSFileSystem(bucket_id, token=token_loc)

def bucket_ls(gcs, rdir=".", bucket_id=None):
    """
    Prints rdir contents in the given bucket
    """
    if bucket_id is None:  bucket_id = GLOBAL_BUCKET_ID

    return gcs.ls(f"{bucket_id}/{rdir}")

def bucket_get(gcs, rdir, lpath, bucket_id=None):
    """
    Gets rdir file and copies it to lpath
    """
    if bucket_id is None: bucket_id = GLOBAL_BUCKET_ID
    return gcs.get(f"{bucket_id}/{rdir}", lpath)

def bucket_put(gcs, lpath, rdir, bucket_id=None):
    """
    Puts lpath file and copies it to rdir
    """
    if bucket_id is None: bucket_id = GLOBAL_BUCKET_ID

    return gcs.put(lpath, f"{bucket_id}/{rdir}")

def bucket_read_csv(rdir=None, rfile=None, rfpath=None, bucket_id=None):
    """
    Reads csv from rdir/rfile or rfpath and returns it
    """
    if bucket_id is None: bucket_id = GLOBAL_BUCKET_ID

    if rfpath is not None:
        return pd.read_csv(f"gs://{bucket_id}/{rfpath}")

    return pd.read_csv(f"gs://{bucket_id}/{rdir}/{rfile}")

# API

class GCSBucket(object):
    """
    Object based API to interact with Google Cloud Storage Bucket
    """
    def __init__(self, token='default', bucket_id=GLOBAL_BUCKET_ID, project_id=GLOBAL_PROJECT_ID):
        
        # Identifiers
        self._bucket= bucket_id
        self._project= project_id

        if token == 'default':
            home_env = os.environ['HOME']
            self.token= f'{home_env}/.config/gcloud/application_default_credentials.json'
        else:
            self.token= token

        # Connection to GCP Bucket
        self.gcs = create_gcsfs(bucket_id, self.token)

    
    def ls(self, remote_path="."):
        """
        Prints remote_path contentss
        """
        return bucket_ls(self.gcs, remote_path, self._bucket)

    def get(self, remote_path, local_path):
        """
        Gets remote_path file and copies it to local_path
        """
        return bucket_get(self.gcs, remote_path, local_path, self._bucket)

    def put(self, local_path, remote_path):
        """
        Puts local_path file and copies it to remote_path
        """
        return bucket_put(self.gcs, local_path, remote_path, self._bucket)
    
    def read_csv(self, remote_path, rfile):
        """
        Reads csv from remote_path/rfile or rfpath and returns it
        """
        return bucket_read_csv(rdir=remote_path, rfile=rfile, bucket_id=self._bucket)

    