from PIL import Image
import glob

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from c0001_retrieve_meta import retrieve_path

def build_gif():
    """

    """

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
