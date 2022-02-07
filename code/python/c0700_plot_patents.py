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
from clinicalstudies_gov_scanner import ClinicalTrial
from find_color import find_color



def plot_patents():
    """

    """

    # count patents
    count_patents()

    # plot patents
    plot_all_patents()



def plot_all_patents():
    """
    plot patents counts from saved df
    """

    file_name = os.path.join(retrieve_path('df_patents_per_year'))
    df = pd.read_csv(file_name)
    df = clean_dataframe(df)

    xx = list(df['year'])
    yy = list(df['file_year_counts'])
    zz = list(df['file_cdf_counts'])
    yyy = list(df['patent_year_counts'])
    zzz = list(df['patent_cdf_counts'])

    plt.figure(figsize=(16, 6))

    plt.subplot(121)
    plt.scatter(xx, yy, label='year filed')
    plt.scatter(xx, yyy, label='year patented')
    plt.xlabel('Years')
    plt.ylabel('Number of Patents')
    plt.title('Yearly Patent Count')
    plt.legend(loc ="upper left")

    plt.subplot(122)
    plt.scatter(xx,zz, label='year filed')
    plt.scatter(xx,zzz, label='year patented')
    plt.xlabel('Years')
    plt.ylabel('Number of Patents')
    plt.title('Cumulative Patent Count')
    plt.legend(loc ="upper left")

    plt.savefig(retrieve_path('all_patents_vs_year'), dpi = 600, edgecolor = 'w')





def count_patents():
    """
    count patents and save as dataframe
    """

    # retrieve ref_file
    ref_file = find_ref('df_aggregated')
    df = pd.read_csv(ref_file)

    # clean dataframe
    df = clean_dataframe(df)

    years = list(df['file_year'])
    year_list = np.arange(min(years), max(years), 1)

    year_counts, cdf_counts = [], []
    patent_year_counts, patent_cdf_counts = [], []
    for year in year_list:

        df_yearly = df[(df.file_year == year)]
        year_counts.append(len(list(df_yearly['file_year'])))

        df_yearly = df[(df.file_year <= year)]
        cdf_counts.append(len(list(df_yearly['file_year'])))

        df_yearly = df[(df.patent_year == year)]
        patent_year_counts.append(len(list(df_yearly['file_year'])))

        df_yearly = df[(df.patent_year <= year)]
        patent_cdf_counts.append(len(list(df_yearly['file_year'])))


    df = pd.DataFrame()
    df['year'] = year_list
    df['file_year_counts'] = year_counts
    df['file_cdf_counts'] = cdf_counts
    df['patent_year_counts'] = patent_year_counts
    df['patent_cdf_counts'] = patent_cdf_counts

    file_name = os.path.join(retrieve_path('df_patents_per_year'))
    print('file_name for counts saved to = ')
    print(file_name)
    df.to_csv(file_name)




def find_ref(path_name):
    """
    Send
    """
    file_ref = ''
    file_list = os.listdir(retrieve_path(path_name))
    for file in file_list:
        if len(file) > len(file_ref):
            file_ref = file

    file_path = os.path.join(retrieve_path(path_name), file_ref)
    print('file_path = ')
    print(file_path)

    return(file_path)




def clean_dataframe(df):
    """

    """
    col_names = df.columns

    for name in col_names:

        if 'Unnamed' in name:
            del df[name]

    try:
        df = df.drop_duplicates(subset = 'patent_num')
        df = df.sort_values('patent_num', ascending=True)
    except:
        print('did not drop.')

    df = df.reset_index()

    return(df)
