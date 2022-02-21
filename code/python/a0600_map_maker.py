from bs4 import BeautifulSoup
import datetime
import glob
import json
import lxml
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import exists
import pandas as pd
from PIL import Image
from serpapi import GoogleSearch
import re
import requests
import time
import urllib.parse


from a0001_admin import clean_dataframe
from a0001_admin import name_paths
from a0001_admin import retreive_categories
from a0001_admin import retrieve_format
from a0001_admin import retrieve_list
from a0001_admin import retrieve_path
from a0001_admin import write_paths
from find_color import find_color
from gif_maker import build_gif


def map_maker():
    """

    """
    print('began map_maker')

    # List task numbers to complete
    tasks = [0]
    write_paths()
    if  0 in tasks: tasks = np.arange(1, 101, 1)
    if  1 in tasks: yearly_map()
    if  2 in tasks: build_gif()

    print('completed map_maker')


def scale_sizes(sizes):
    """
    provide list of numbers
    scale
    """

    scatter_size_min = int(retrieve_format('scatter_size_min'))
    scatter_size_max = int(retrieve_format('scatter_size_min'))

    sizes_scaled = []
    for size in sizes:

        try:
            size_min = size + 2
            size_scaled = math.log(size_min)
            size_scaled = float(size_scaled)
        except:
            size_scaled = scatter_size_min
            size_scaled = float(size_scaled)

        size_scaled = scatter_size_max*size_scaled/max(sizes) + scatter_size_min
        sizes_scaled.append(size_scaled)

    assert len(sizes) == len(sizes_scaled)
    return(sizes_scaled)


### completed programs ###

def build_gif():
    """

    """
    print('building gif')

    # list articles
    for name_article in retrieve_list('type_article'):

        file_dst_name = str(name_article + '_map_png')
        df_src = os.path.join(retrieve_path(file_dst_name))

        # list compare term files
        compare_terms = os.path.join(retrieve_path('term_compare'))
        for category in retreive_categories():

            png_list = []
            for file in os.listdir(df_src):

                if category not in str(file): continue
                df_src = os.path.join(retrieve_path(file_dst_name), file)
                png_list.append(df_src)

            #print('png_list = ')
            #print(png_list)
            #assert len(png_list) > 1

            frames = []
            #png_file = os.path.join(path, "*.png")
            gif_dst = str(name_article + '_map_gif')
            save_file = os.path.join(retrieve_path(gif_dst) , category + '.gif')
            print('save_file = ' + str(save_file))

            #imgs = glob.glob(png_file)
            for i in png_list:

                try:
                    per_complete = round(100*png_list.index(i)/len(png_list),2)
                    print(name_article + ' ' + category + ' % complete = ' + str(per_complete) )
                    new_frame = Image.open(i)
                    frames.append(new_frame)

                    # Save into a GIF file that loops forever
                    frames[0].save(save_file, format='GIF',
                               append_images=frames[1:],
                               save_all=True,
                               duration=300, loop=0)
                except:
                    print('exception found.')


def yearly_map():
    """
    from df map each year
    """

    # list articles
    for name_article in retrieve_list('type_article'):

        # list compare term files
        compare_terms = os.path.join(retrieve_path('term_compare'))
        for category in retreive_categories():

            # retrieve search terms
            f = os.path.join(retrieve_path('term_compare'), category + '.csv')
            search_terms = retrieve_list(f)

            # retrieve list of al articles
            file_src = str(name_article + '_compare_terms_df')
            f = os.path.join(retrieve_path(file_src), category  + '.csv')
            print('f = ' + str(f))
            df = clean_dataframe(pd.read_csv(f))

            print('df.columns = ')
            print(df.columns)
            print('name_article = ' + name_article)


            years = np.arange(int(min(list(df['ref_year']))), int(max(list(df['ref_year']))), 1)

            for year in years:

                print('year = ' + str(year))

                df_temp =  df[(df['ref_year'] <= year)]
                lats = list(df_temp['ref_lat'])
                lons = list(df_temp['ref_lon'])

                plt.close('all')
                figure, axes = plt.subplots()

                # add background of the globe
                map_path = os.path.join(retrieve_path('blank_map'))
                img = plt.imread(map_path)
                extent = [-170, 190, -58, 108]
                axes.imshow(img, extent=extent)

                label_str = str(len(list(df_temp['ref_year']))) + ' ' + 'all '
                num = 8
                colorMarker, colorEdge, colorTransparency = find_color(num)
                plt.scatter(lons, lats, color=colorMarker, edgecolors=colorEdge, alpha=float(colorTransparency),label=label_str)

                for term in search_terms:
                    #if '|' in term: term = (term.split('|'))[0]
                    df_term =  df_temp[(df_temp[term] > 0)]
                    lats = list(df_term['ref_lat'])
                    lons = list(df_term['ref_lon'])
                    label_str = str(len(list(df_term['ref_year']))) + ' ' + term
                    num = search_terms.index(term) +1
                    colorMarker, colorEdge, colorTransparency = find_color(num)

                    # set sizes based on the reference value
                    try:
                        sizes = []
                        for  size in list(df_term['ref_value']):
                            sizes.append(size+10)
                        sizes = scale_sizes(sizes)
                    except:
                        sizes = [40]*len(lons)

                    plt.scatter(lons, lats, s=sizes, color=colorMarker, edgecolors=colorEdge, alpha=float(colorTransparency),label=label_str)

                axes.axis('off')
                plt.title(name_article + ' ' + str(int(min(list(df['ref_year'])))) + '-' + str(year))
                plt.legend(bbox_to_anchor=(0.2, -0.2), loc ="upper left")

                file_dst_name = str(name_article + '_map_png')
                df_file = os.path.join(retrieve_path(file_dst_name), category + '_' + str(year) + '.png')
                plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')
                plt.close('all')


if __name__ == "__main__":
    main()
