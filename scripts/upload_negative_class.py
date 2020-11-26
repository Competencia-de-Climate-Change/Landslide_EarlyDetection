"""
Script to upload landslide dataset (positive class) to GCP Storage

Run as:
>>> python upload_dataset.py

Check logs:
>>> cat log_*.txt # where * is the last datetime
"""
import subprocess
from datetime import datetime
import numpy as np
import geopandas as gpd

from .src.uploader import Uploader # pylint: disable=relative-beyond-top-level
from .src.ReMasFrame import ReMasFrame # pylint: disable=relative-beyond-top-level

NOW = datetime.now().strftime("%Y_%m_%d_%H_%M")
LOG_FILE_NAME = f"log_{NOW}.txt"

def get_dem(upload, bands, buffer_size=0.1, axis=0, update=False):
    """
    Retrieves DEM at given location by upload object
    """
    product_id = upload.products[upload.current_cat][upload.current_prod]['id']
    aoi = upload.event_geometry.buffer(buffer_size).envelope

    scenes, ctx = ReMasFrame.search_scenes(
        aoi,
        product_id, 
        start_date='2013-10-01',
        end_date='2013-12-01'
    )
    if not scenes:
        error_str = f"El conjunto de escenas está vacía para {upload.current_prod}, {bands}"
        raise IndexError(error_str)

    new_ctx = ctx.assign(resolution=upload.current_deg_res)
    arr_stack = scenes.stack(bands, new_ctx)

    composite = np.ma.median(arr_stack, axis=axis)

    # reshape to be (bs, channel, w, h)
    old_shape = list(composite.shape)
    new_shape = tuple([1] + old_shape)
    composite = composite.reshape(new_shape)

    if update:
        upload.set_current_stack(composite)
        upload.current_scenes = scenes
        upload.current_ctx = new_ctx

    return (scenes, new_ctx), composite

def get_smap(upload, bands=None, axis=1, update=False):
    """
    Retrieves SMAP at given location by upload object
    """

    (scenes, ctx), _ = upload.get_scenes()

    bands = upload.current_bands if bands is None else bands

    if not scenes:
        error_str = f"El conjunto de escenas está vacía para {upload.current_prod}, {bands}"
        raise IndexError(error_str)

    new_ctx = ctx.assign(resolution=upload.current_deg_res)
    arr_stack = scenes.stack(bands, new_ctx)

    # compisite.shape = (bs, w, h)
    composite = np.ma.median(arr_stack, axis=axis)

    # reshape to be (bs, channel, w, h)
    old_shape = list(composite.shape)
    new_shape = tuple(old_shape[0], 1, old_shape[1], old_shape[2])
    composite = composite.reshape(new_shape)

    if update:
        upload.set_current_stack(composite)
        upload.current_scenes = scenes
        upload.current_ctx = new_ctx

    return (scenes, new_ctx), composite  


def elevation_workflow(upload):
    """
    Runs elevation workflow
    """
    _, _ = get_dem(upload, bands='heigth', update=True)
    return upload

def smap_workflow(upload):
    """
    Runs soil moisture workflow
    """
    _, _ = get_smap(upload, update=True)

    _ = upload.fill_value(method='mean', update=True)
    return upload

def default_workflow(upload):
    """
    Runs default workflow
    """
    # update argument saves data in object
    _, _ = upload.get_scenes(update=True)

    _ = upload.create_stack(update=True)

    _ = upload.fill_value(method='mean', update=True)

    return upload

# THIS CAN BE DONE IN PARALLEL
def upload_landslides(landslide_df, upload):
    """
    Function to upload landslide dataset for current product
    """
    for event_idx, series in landslide_df.iterrows():
        upload.set_current_event(
            event_date=series.event_date,
            event_id=event_idx,
            event_geometry=series.geometry
        )
        # aster need median composite + doesnt need fill_value
        try:
            if upload.current_prod == 'aster':
                upload = elevation_workflow(upload)
            elif upload.current_prod == 'smap':
                upload = smap_workflow(upload)
            else:
                upload = default_workflow(upload)
        except (IndexError) as exception_error:  # pylint: disable=broad-except
            print(
                f"Not succesful workflow for idx: {event_idx} and product:" + \
                f"{upload.current_prod}' -- {str(exception_error)}"
            )
            command = f"echo 'Not succesful workflow for idx: {event_idx} and product:" + \
                      f"{upload.current_prod}' >> {LOG_FILE_NAME}"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            _, _ = process.communicate()
            continue

        # specific manipulation for soil bands cfs
        if upload.current_prod == 'cfs':
            idx_soil_bands = []
            for idx, band in enumerate(upload.current_bands):
                if 'soil' in band:
                    idx_soil_bands.append(idx)

            upload.sum_bands(
                idx_target_bands=idx_soil_bands,
                update=True
            )

        _, _ = upload.create_upload_path(update=True)
        try:
            upload.upload_current_stack()
        except Exception as exception_error:  # pylint: disable=broad-except
            print(
                f"Not succesful upload for idx: {event_idx} and product:" + \
                f"{upload.current_prod}' -- {str(exception_error)}"
            )
            # manage exception by saving a log of non succesful uploads
            command = f"echo 'Not succesful upload for idx: {event_idx} and product:" + \
                      f"{upload.current_prod}' >> {LOG_FILE_NAME}"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            _, _ = process.communicate()
            continue



def main():
    """
    Main Program to upload dataset for all of the products
    """
    upload = Uploader('dataset/negative', token='default')
    df_points__ = gpd.read_file("Landslide_EarlyDetection/data/no_landslide.shp")
    products = ReMasFrame.get_products()

    # THIS CAN BE DONE IN PARALLEL
    for cat_name, products_dict in products.items():
        for product_name, product_config in products_dict.items():
            if product_name in ['goes', 'population']: # undefined deg_res
                continue
            print(product_name)
            bands = product_config['bands']
            deg_res = product_config['deg_res']
            upload.set_current_prod(cat_name, product_name, bands, deg_res)

            upload_landslides(df_points__, upload)



if __name__ == "__main__":
    main()
