def create_Point(lat, lon, properties_dict, add_bbox=False):
    aoi_point = \
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [lon, lat]
      }
    }
    
    aoi_point['properties'] = properties_dict
    
    if add_bbox:
        bbox = create_bbox(lat, lon)
        aoi_point['bbox'] = bbox
        
    return aoi_point

def create_Collection(feature_list):
    
    aoi_point_collection = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for feature in feature_list:
        aoi_point_collection["features"].append(feature)
    return aoi_point_collection

def create_landslides_nasa_points(df):

    from dateutil.parser import parse

    point_list = []

    for idx, row in df.iterrows():
        properties_dict = {}

        # properties
        properties_dict['location']  = row['location_description']
        properties_dict['size']      = row['landslide_size']
        properties_dict['date']      = parse(row['event_date']).strftime('%Y-%m-%d')
        properties_dict['category' ] = row['landslide_category']
        properties_dict['trigger']   = row['landslide_trigger']
        properties_dict['fatality']= row['fatality_count']
        properties_dict['injury']  = row['injury_count']

        point_list.append(create_Point(lon=row['longitude'], lat=row['latitude'], properties_dict=properties_dict))
        
    return point_list

def create_Polygon_around_Point_v1(point):
    new_polygon = point
    new_polygon['geometry']['type'] = 'Polygon'
    lon, lat = new_polygon['geometry']['coordinates']
    
    new_coords = [
            [lon - 0.01, lat - 0.01], 
            [lon + 0.1, lat], 
            [lon + 0.1, lat + 0.1],
            [lon, lat + 0.1], 
            [lon - 0.01, lat - 0.01]
      ]
    new_polygon['geometry']['coordinates'] = new_coords
    
    return new_polygon

def create_Polygon_around_Point_v2(point, radius=1, square=False, return_shape=False):
    from shapely.geometry import Point
    
    lon, lat = point['geometry']['coordinates']
            
    polygon = Point(lon, lat).buffer(radius)
    
    if square:
        polygon = polygon.envelope
        
    if return_shape:
        return polygon
    
    point['geometry'] = polygon.__geo_interface__
    
    return point