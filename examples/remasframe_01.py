import fsspec

from src.ReMasFrame import ReMasFrame

mapper = fsspec.get_mapper('gcs://data-projectx/')

nasa_df = ReMasFrame()

# changes Point to Polygon
nasa_df.box(2, inplace=True)

# Returns products that we use as a dict
products = nasa_df.get_products()

# Choose CHIRPS Daily Precip
chirps = products['weather']['chirps']

# Choose an idx --> a landslide (or filter the geodataframe :D)
idx_test = 0

# Returns start and end date of a 4 day interval
start_date, end_date = nasa_df.date_interval(nasa_df.event_date[idx_test], delta=2)

# Searches scenes between start and end date
scenes, ctx = search_scenes(nasa_df.geometry[idx_test], chirps[id], start_date=start_date, end_date=end_date, limit=10)