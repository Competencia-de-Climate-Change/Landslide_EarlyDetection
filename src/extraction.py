from . import api_gcp
from . import geometry

import geopandas as gpd
import json


def get_landslides():
    return api_gcp.bucket_read_csv(rfpath="nasa/landslides.csv")


def run_FeatureCollection(df=None, polygons=False, poly_fun='v1', save=False):
    if df is None:
        df = get_landslides()

    interest_triggers = ['rain', 'downpour', 'monsoon', 'continuous_rain','snowfall_snowmelt', 'flooding']

    filtered_df = df[df.landslide_trigger.isin(interest_triggers)]

    landslide_features = geometry.create_landslides_nasa_points(filtered_df)


    if polygons and poly_fun =='v1':
        landslide_features = [geometry.create_Polygon_around_Point_v1(feat) for feat in landslide_features]

    elif polygons and poly_fun =='v2':
        landslide_features = [geometry.create_Polygon_around_Point_v2(feat) for feat in landslide_features]

    feature_collection = geometry.create_Collection(landslide_features)

    if save:
        with open("landslides_features.geojson", "w") as outfile:  
            json.dump(feature_collection, outfile) 

    return feature_collection

def gpd_FeatureCollection(dict_=None, geojson_file=None):
    if dict_ is not None:
        data = json.dumps(dict_['features'])
        df = gpd.GeoDataFrame(json.loads(data))

        # process geometry
        from shapely.geometry import Point
        df['geometry'] = df['geometry'].apply(lambda x:  Point(x['coordinates'][0], x['coordinates'][1]))

        # process properties
        new_columns = list(df['properties'][0].keys())
        new_data_list = []
        for idx, row in df[['properties']].iterrows():
            new_data = list(dict(row['properties']).values())
            new_data_list.append(new_data)
        
        df[new_columns] = new_data_list

        return df.drop('properties', axis=1)

    return gpd.read_file(geojson_file)