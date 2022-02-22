from bs4 import BeautifulSoup
import json
import lxml
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import re
import requests
import shutil
import pandas as pd
import pandas_read_xml as pdx
import time

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_ref
from c0001_retrieve_meta import retrieve_datetime
from c0001_retrieve_meta import clean_dataframe

from gif_maker import build_gif
from clinicalstudies_gov_scanner import ClinicalTrial
from find_color import find_color



def map_patents():
    """

    """
    build_gif()

    df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop_time' + '.csv')
    df = pd.read_csv(df_file)
    df = clean_dataframe(df)

    yearly_map(df)

    lats = list(df['gpsLat'])
    lons = list(df['gpsLong'])
    urls = list(df['url'])

    # figure
    plt.close('all')
    figure, axes = plt.subplots()

    # add background of the globe
    map_path = os.path.join(retrieve_path('blank_map'))
    img = plt.imread(map_path )
    extent = [-170, 190, -58, 108]
    axes.imshow(img, extent=extent)

    count = 0
    for i in range(len(lats)):

        print('% complete = ' + str(100*i/len(lats)))

        try:
            num = len(urls[i])
            colorMarker, colorEdge, colorTransparency = find_color(num)
            plt.scatter(float(lons[i]) , float(lats[i]), color=colorMarker, edgecolors=colorEdge, alpha=float(colorTransparency))
            count = count + 1
        except:
            print('skipped')

    axes.axis('off')

    plt.rcParams.update({'font.size': 10})
    plt.title('Maps of Patents from ' + str(min(list(df['patent_year']))) + '-' + str(max(list(df['patent_year'])))+ '-' + str(year) + ' (' + str(count) + ' patents )')
    df_file = os.path.join(retrieve_path('map_patent'))
    plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')



def yearly_map(df):
    """
    from df map each year
    """

    lats = list(df['gpsLat'])
    lons = list(df['gpsLong'])
    urls = list(df['url'])
    years = list(df['patent_year'])

    year_list = np.arange(min(years), max(years), 1)

    for year in year_list:

        df_short =  df[(df.patent_year <= year)]

        lats = list(df_short['gpsLat'])
        lons = list(df_short['gpsLong'])
        urls = list(df_short['url'])
        years = list(df_short['patent_year'])

        # figure
        plt.close('all')
        figure, axes = plt.subplots()

        # add background of the globe
        map_path = os.path.join(retrieve_path('blank_map'))
        img = plt.imread(map_path )
        extent = [-170, 190, -58, 108]
        axes.imshow(img, extent=extent)

        count = 0
        for i in range(len(lats)):

            print('% complete = ' + str(100*i/len(lats)))

            try:
                num = len(urls[i])
                colorMarker, colorEdge, colorTransparency = find_color(num)
                plt.scatter(float(lons[i]) , float(lats[i]), color=colorMarker, edgecolors=colorEdge, alpha=float(colorTransparency))
                count = count + 1
            except:
                print('skipped')

        axes.axis('off')

        plt.rcParams.update({'font.size': 10})
        plt.title('Maps of Patents from ' + str(min(list(df['patent_year']))) + '-' + str(year) + ' (' + str(count) + ' patents)')
        df_file = os.path.join(retrieve_path('df_map_yearly'), str(year) + '.png')
        plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')

    build_gif()
