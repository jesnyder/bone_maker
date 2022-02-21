from PIL import Image
import glob

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from a0001_admin import clean_dataframe
from a0001_admin import name_paths
from a0001_admin import retrieve_format
from a0001_admin import retrieve_list
from a0001_admin import retrieve_path
from a0001_admin import write_paths
from find_color import find_color

def build_gif():
    """

    """
    for name_article in retrieve_list('type_article'):



        print('building gif')
        path = os.path.join(retrieve_path('df_map_yearly'))

        frames = []
        print('path = ')
        print(path)
        png_file = os.path.join(path, "*.png")

        save_file = os.path.join(retrieve_path('map_gif'))

        imgs = glob.glob(png_file)
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)

            # Save into a GIF file that loops forever
            frames[0].save(save_file, format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=300, loop=0)
