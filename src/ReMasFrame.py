import geopandas as gpd
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point, Polygon


class ReMasFrame(gpd.GeoDataFrame):
    def __init__(self, *args, **kwargs):
        super(ReMasFrame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return ReMasFrame

    def box(self, km, inplace=False):
        proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

        def geodesic_point_buffer(row, km):
            # Azimuthal equidistant projection
            aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
            project = partial(
                pyproj.transform,
                pyproj.Proj(aeqd_proj.format(lat=row.y, lon=row.x)),
                proj_wgs84)
            buf = Point(0, 0).buffer(km * 1000)  # distance in metres
            return Polygon(transform(project, buf).exterior.coords[:]).envelope

        if inplace == True:
            self.loc[:,('box')] = self['geometry'].apply(geodesic_point_buffer, km=km)

        return self['geometry'].apply(geodesic_point_buffer, km=km)
