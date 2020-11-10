weather_prods = {
    'goes' : {
        'id' : 'goes17:fulldisk:v1',
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
        'id' : 'daily-weather:gsod-interpolated:v0',
        'res' : '10km',
        'bands' : ['tavg', 'tmax', 'tmin', 'rh', 'prec'],
        'descrip' : 'interpolated raster from 1980-01-01 for geographical area from -180 deg to 180 deg longitude, and from -60 to 60 deg latitude.'
    },

    'chirps' : {
        'name' : 'CHIRPS Daily Precipitation Weather',
        'id' : 'chirps:daily:v1',
        'res' : '5km',
        'freq': 'daily',
        'bands' : ['daily_precipitation']

    },

    'cfs' : {
        'name' : 'CFS Daily Weather',
        'id' : 'ncep:cfsr-v2:daily:v1',
        'res' : '20km',
        'freq': 'daily',
        'bands' : ['prec', 'snow_cover', 'snow_depth', 'snow_water', 'soilmoisti', 'sublimation', 'tavg', ]
    }
}

soil_moist = {
    'smap' : {
        'id'   : 'smap:SMPL3SM_E',
        'res'  : '9km',
        'freq' : 'daily',
        'bands':  ['am_soil_moisture', 'pm_soil_moisture']
    }
}

elevation = {
    'aster' : {
        'id' : 'aster:gdem3:v0', 
        'res': '30m', 
        'bands': ['alpha', 'height', 'number_images']
    }
}

population = {
    'id' :  'd15c019579fa0985f7006094bba7c7288f830e1f:GPW_Population_Density_V4_0', 
    'res' : '1km',
    'bands': ['population']
}