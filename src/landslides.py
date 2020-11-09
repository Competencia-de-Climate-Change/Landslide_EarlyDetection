from extraction import get_landslides

import geopandas as gpd

import descarteslabs as dl

class Landslides(gpd.GeoDataFrame):
    """
    Class to handle landslide data.
    """

    def __init__(self, mode='default'):
        # Dataframe with nasa data
        self.landslide_nasa = get_landslides()

        interest_triggers = ['rain', 'downpour', 'monsoon', 'continuous_rain','snowfall_snowmelt', 'flooding']


        # Geodataframe in self
        super()__init__(self.landslide_nasa, 
            gpd.points_from_xy(self.landslide_nasa.longitude, self.landslide_nasa.latitude)
            )

        # filters columns of interest
        if mode == 'filtered':
            self = self[self.landslide_trigger.isin(interest_triggers)]

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

        ctx : ctx
            Result from Descarteslabs
        """
        
        
        if mid_date is not None and date_range is not None:
            start_date, end_date = date_interval(self.date, delta=date_range)
            
        scenes, ctx = dl.scenes.search(
            polygons
            products=product_ids,
            start_datetime=start_date,
            end_datetime=end_date,
            limit=limit
        )
        
        return scenes, ctx