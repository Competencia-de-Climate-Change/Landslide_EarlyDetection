import numpy as np
from pathlib import Path

# import torch
from .ReMasFrame import ReMasFrame
from .api_gcp import GCSBucket


class Uploader():
    r"""
    Class to automate upload of data to GCP
    """
    def __init__(self, root_dir):
        self.gstorage = GCSBucket(token='default')
        self.root_dir = root_dir
        self.products = ReMasFrame.get_products()
        self.upload_path = None
        self.file_name = None

        self.event_date_str = None
        self.event_id = None
        self.event_geometry = None

        self.current_prod = None     # name of product in self.products
        self.current_cat = None      # name of category must be one of [weather, elevation, ...]
        self.current_bands = None    # list of band names for current prod
        self.current_deg_res = None  # resolution in degrees for current prod


        self.current_scenes = None   # current scene collection
        self.current_ctx = None      # current geocontext of current scene
        self.current_stack = None    # current stack

    def set_current_prod(self, cat_str: str, prod_str: str, bands: list, deg_res: float):
        """
        Sets current product.
        """
        self.current_prod = prod_str
        self.current_cat = cat_str
        self.current_bands = bands
        self.current_deg_res = deg_res

    def set_current_event(self, event_date : str, event_id : str, event_geometry):
        """
        Sets current event.
        """
        self.event_date_str = event_date
        self.event_id = event_id
        self.event_geometry = event_geometry

    def set_current_stack(self, stack):
        """
        Set current stack of images
        """
        self.current_stack = stack

    def create_upload_path(self, update=False):
        """
        Creates path dir for current event and prod
        """
        path = f"{self.root_dir}/{self.current_prod}"
        file_name = f"{self.event_date_str}_{self.event_id}.npy"

        if update:
            self.upload_path = path
            self.file_name = file_name

        return path, file_name

    def upload_current_stack(self):
        """
        Uploads current stack to current upload_path.

        Separates X and y into different files.
        """
        dir_path = self.upload_path
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        # Last image in current stack is target (y), the others are features (X)
        X = self.current_stack[:-1]
        y = self.current_stack[-1]
        base_file_name, extension = self.file_name.split('.')

        file_name_x = f"{base_file_name}/X.{extension}"
        file_name_y = f"{base_file_name}/y.{extension}"

        # Create directory
        Path(f"{dir_path}/{base_file_name}").mkdir(parents=True, exist_ok=True)
        
        for array, file_name in zip([X,y], [file_name_x, file_name_y]):
            full_file_path = f"{dir_path}/{file_name}"

            # Save X and y
            np.save(
                full_file_path,
                array.data
                )
        
            self.gstorage.put(
                local_path=full_file_path,
                remote_path=full_file_path
                )

            Path(full_file_path).unlink()
    
    #----Image manipulation-------#

    def create_stack(self, update=False):
        """
        Creates a stack of images from current Scene Collection
        """

        stack = self.current_scenes.stack(
            self.products[self.current_cat][self.current_prod]['bands'], 
            self.current_ctx
        )

        if update:
            self.set_current_stack(stack)

        return stack

    def fill_value(self, array_masked=None, method='mean', update=False):
        """
        Fills masked value with mean of each image in a 4d array

        e.g:
        x is (bs, channels, w, h)
        for each image:
          for each channel:
                image.fill_value = image.mean()
                image.filled()
        """
        if method != 'mean':
            raise NotImplementedError
        
        masked_array = self.current_stack

        if array_masked is not None:
            masked_array = array_masked

        image_channel_mean = np.ma.mean(masked_array, axis=(2,3))

        for i, image in enumerate(masked_array):
            for j, channel in enumerate(image):
                filled_channel = channel.filled(image_channel_mean[i,j])
                masked_array[i,j] = filled_channel

        if update:
            self.set_current_stack(masked_array)

        return masked_array

    def sum_bands(self, idx_target_bands, stack=None, update=False):
        """
        Sums given bands (as ndarray) and replaces them in the scene_stack.
        """
        # Retrieve bands
        current_stack = self.current_stack
        if stack is not None: # use instead a given stack
            current_stack = stack
        to_replace_bands = current_stack[:, idx_target_bands, ...]
        
        # Update shape
        old_shape = list(to_replace_bands.shape)
        old_shape[1] = 1 # sum of bands equals to one
        new_shape = tuple(old_shape)

        # Sum and reshape bands
        summed_bands = np.sum(to_replace_bands, axis=1).reshape(new_shape)

        # Concatenate new summed band and delete old ones
        scene_stack = np.concatenate((current_stack, summed_bands), axis=1)
        new_scene_stack = np.delete(scene_stack, idx_target_bands, axis=1)

        if update:
            self.set_current_stack(new_scene_stack)

        return new_scene_stack

    #-----DESCARTES SPECIFIC------#

    def get_scenes(self, buffer_size=0.1, update=False):
        """
        Retrieves images from descarteslabs for the current prod
        """
        # Returns start and end date of a 10 day interval, last day is the date of event
        start_date, end_date = ReMasFrame.date_interval(self.event_date_str, delta_minus=10)
        
        # Obtain info for scene collection
        product_id = self.products[self.current_cat][self.current_prod]['id']
        aoi = self.event_geometry.buffer(buffer_size).envelope

        scenes, ctx = ReMasFrame.search_scenes(
            aoi,
            product_id,
            start_date=start_date,
            end_date=end_date
        )
        if not scenes:
            error_str = f"El conjunto de escenas está vacía para {product_id}, {self.event_id}"
            raise IndexError(error_str)

        new_ctx = ctx.assign(resolution=self.current_deg_res)
        if update:
            self.current_scenes = scenes
            self.current_ctx = new_ctx

        return (scenes, new_ctx), (start_date, end_date)



