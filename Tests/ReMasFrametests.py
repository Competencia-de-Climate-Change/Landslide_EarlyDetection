import fsspec
from src.ReMasFrame import ReMasFrame
from io import StringIO
import pandas as pd
import geopandas as gpd

mapper = fsspec.get_mapper('gcs://data-projectx/')


def read_bytes_string(byte_file, encoding='utf-8'):
    s = str(byte_file,'utf-8')
    return StringIO(s)


nasa_df = pd.read_csv("gs://data-projectx/nasa/landslides.csv")
nasa_df = ReMasFrame(nasa_df, geometry=gpd.points_from_xy(nasa_df.longitude, nasa_df.latitude))
nasa_df.box(2, inplace=True)
