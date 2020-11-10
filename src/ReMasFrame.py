import geopandas as gpd

from .extraction import get_landslides
from .products import *
from .geometry import geodesic_point_buffer

from dateutil.parser import parse

import descarteslabs as dl # pip install descarteslabs==1.5.0 !!

#------------------------------------#

class ReMasFrame(gpd.GeoDataFrame):
    """
    Class to handle landslide data as GeoDataFrame.
    """

    def __init__(self, *args, **kwargs):
        # Dataframe with nasa data
        landslide_nasa = get_landslides()

        interest_triggers = ['rain', 'downpour', 'monsoon', 'continuous_rain','snowfall_snowmelt', 'flooding']

        # filters columns of interest by trigger
        landslide_nasa = landslide_nasa[landslide_nasa.landslide_trigger.isin(interest_triggers)]

        interest_columns = ['location_description', 'landslide_size', 'event_date', 'landslide_category', \
                        'landslide_trigger', 'fatality_count', 'injury_count', 'longitude', 'latitude']

        # filter non-interesting columns
        landslide_nasa = landslide_nasa[interest_columns]
        landslide_nasa['event_date'] = landslide_nasa['event_date'].apply(lambda date : parse(date).strftime('%Y-%m-%d'))

        super(ReMasFrame, self).__init__(
            landslide_nasa, 
            geometry=gpd.points_from_xy(landslide_nasa.longitude, landslide_nasa.latitude),
        )

    def create_box(self, km, inplace=False):
        import pyproj
        
        proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

        if inplace == True:
            self.loc[:,('box')] = self['geometry'].apply(geodesic_point_buffer, km=km, proj=proj_wgs84)

        return self['geometry'].apply(geodesic_point_buffer, km=km, proj=proj_wgs84)

    @staticmethod
    def get_products():
        """
        Creates a dictionary with all products and their information.
        """
        return {
            'weather' : weather_prods,
            'soil_moist' : soil_moist,
            'elevation' : elevation,
            'population' : population
        }

    @staticmethod
    def date_interval(date, delta=1, return_str=False):
        """
        Retorna el intervalo de una fecha (date). 'delta' corresponde al intervalo
        de tiempo y 'return_str' es un argumento para decidir si retorna la fecha 
        en forma de string o no.
        """
        from dateutil.relativedelta import relativedelta
        from dateutil.parser import parse

        if return_str:
            return (parse(date) - relativedelta(days=delta)).strftime('%Y-%m-%d'), (parse(date) + relativedelta(days=delta)).strftime('%Y-%m-%d')

        return parse(date) - relativedelta(days=delta), parse(date) + relativedelta(days=delta)


    @staticmethod
    def search_scenes(polygons, product_ids, mid_date=None, date_range=None, start_date=None, end_date=None, limit=10):
        """
        Search scenes from the dataframe between an interval of dates.

        Arguments:
        ---------
            product_ids : list
                product ids, e.g. ["landsat:LC08:PRE:TOAR"]
            
            mid_date : str
                date to create an interval around. Ignored if start/end_date is given.
            
            date_range : int
                size of one half of the interval. Ignored if start/end_date is given.

            start_date, end_date : int, int. Optional
                start and end date of an interval.
            
            limit : int 
                maximum number of images

        Returns:
        -------
        scenes : ndarray
            Result from Descarteslabs

        ctx : context 
            Result from Descarteslabs
        """
        
        if mid_date is not None and date_range is not None:
            start_date, end_date = date_interval(self.date, delta=date_range)
            
        scenes, ctx = dl.scenes.search(
            polygons,
            products=product_ids,
            start_datetime=start_date,
            end_datetime=end_date,
            limit=limit
        )
        
        return scenes, ctx
