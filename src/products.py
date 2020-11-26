weather_prods = {
    'goes' : {
        'id' : 'goes17:fulldisk:v1',
        'short_name' : 'goes',
        'freq' : '15 min',
        'res' : 'multiple',
        'bands' : [
            'derived:evi',
            'derived:ndvi',
            'derived:ndwi',
            'derived:ndwi1',
            'derived:ndwi2'
        ]
    },

    'gsod' : {
        'name' : 'GSOD Daily Interpolation Weather Product',
        'short_name' : 'gsod',
        'id' : 'daily-weather:gsod-interpolated:v0',
        'res' : '10km',
        'deg_res': 0.10,
        'bands' : ['tavg', 'tmax', 'tmin', 'rh', 'prec'],
        'descrip' : 'interpolated raster from 1980-01-01 for geographical area from -180 deg to 180 deg longitude, and from -60 to 60 deg latitude.'
    },

    'chirps' : {
        'name' : 'CHIRPS Daily Precipitation Weather',
        'short_name' : 'chirps',
        'id' : 'chirps:daily:v1',
        'res' : '5km',
        'deg_res': 0.05,
        'freq': 'daily',
        'bands' : ['daily_precipitation']

    },

    'cfs' : {
        'name' : 'CFS Daily Weather',
        'short_name' : 'cfs',
        'id' : 'ncep:cfsr-v2:daily:v1',
        'res' : '20km',
        'deg_res': 0.20,
        'freq': 'daily',
        'bands' : ['albedo', 'prec', 'snow_cover', 'snow_depth', 'snow_water_equivalent', 
        'soilmoist1', 'soilmoist2', 'soilmoist3', 'tavg', 'tmax', 'tmin', 'water_runoff']
    }
}

soil_moist = {
    'smap' : {
        'id'   : 'smap:SMPL3SM_E',
        'short_name': 'smap',
        'res'  : '9km',
        'deg_res': 0.10,
        'freq' : 'daily',
        'bands':  ['am_soil_moisture', 'pm_soil_moisture']
    }
}

elevation = {
    'aster' : {
        'id' : 'aster:gdem3:v0',
        'short_name': 'aster',
        'res': '30m',
        'deg_res': 0.001,
        'bands': ['alpha', 'height', 'number_images']
    }
}

population = {
    'population' : {
        'id' :  'd15c019579fa0985f7006094bba7c7288f830e1f:GPW_Population_Density_V4_0', 
        'name': 'pop',
        'res' : '1km',
        'deg_res': None,
        'bands': ['population']
        }
}