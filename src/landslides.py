import api_gcp as gcp
from extraction import run_FeatureCollection


class Landslides():
    """
    Class to handle landslide data.
    """

    def __init__(self, mode='default'):
        # Dataframe with nasa data
        self.landslide_nasa = get_landslides()

        # FeatureCollection, geojson
        self.feature_collection = run_FeatureCollection(
            df=self.landslide_nasa
            polygons=True,
            poly_fun='v2'
        )

        # GeoDataframe
        self.gdf = gpd_FeatureCollection(
            dict_= self.feature_collection
        )


    def query(self, query_col, op, conditions):
        """
        From a given column, operation and list of conditions
        returns a filtered dataframe.

        Arguments:
        ---------
            query_col : str
                the column involved

            op : str
                operation to perform
                Not taken into account when len(condition) > 1
            
            conditions : list
                list of possible conditions

        Returns:
        --------
            df : filtered dataframe

        Example:

        >>> query('trigger', '==', ['rain', 'downpour'])
        ...filtered_df with landslides triggered from rain or downpour...


        >>> query('fatality', '>=', ['100'])
        ...filtered_df with more than a 100 deaths... 

        """
        df = self.gdf 
        
        if len(conditions) > 1: ## isin operation
            return df[df[query_col].isin(conditions)]

        else: ## boolean operation
            if op == '>':
                cond = df[query_col] > conditions[0]
            if op == '>=':
                cond = df[query_col] >= conditions[0]
            if op == '==':
                cond = df[query_col] == conditions[0]
            if op == '<=':
                cond = df[query_col] <= conditions[0]
            if op == '<':
                cond = df[query_col] < conditions[0]

            return df[cond]


        def queries(self, list_queries):
        """
        From a list of self.query arguments, 
        returns a filtered dataframe that 
        correspond to the join of the results
        of each query.
        """
        df = self.gdf 
        

        dataframes = []

        for query_args in list_queries:
            if len(query_args) < 2:
                raise ValueError("Not enough arguments for self.query")

            filtered_df = self.query(query_args[0], query_args[1], query_args[2])  

            dataframes.append(filtered_df)
        
