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

def geodesic_point_buffer(row, km, proj):
    from functools import partial
    import pyproj
    from shapely.ops import transform
    from shapely.geometry import Point, Polygon
    
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=row.y, lon=row.x)),
        proj)
    buf = Point(0, 0).buffer(km * 1000)  # distance in metres
    return Polygon(transform(project, buf).exterior.coords[:]).envelope