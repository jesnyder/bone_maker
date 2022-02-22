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



def count_metadata():
    """

    """

    # retrieve ref_file
    ref_file = find_ref('df_aggregated')
    df = pd.read_csv(ref_file)

    # clean dataframe
    df = clean_dataframe(df)

    # count instances for each column name
    for name in df.columns:

        print('name = ' + str(name))

        unique_list = []
        count_list = []

        for item in list(df[name]):

            if item not in unique_list:

                unique_list.append(item)

                df_item = (df[df[name] == item])

                count = len(list(df_item[name]))
                count_list.append(count)

        df_item = pd.DataFrame()
        df_item['count'] = count_list
        df_item[name] = unique_list

        df_item = df_item.sort_values('count', ascending=False)

        file_name = os.path.join(retrieve_path('count_patent'), name + '.csv')
        df_item = df_item.reset_index()
        del df_item['index']
        df_item.to_csv(file_name)


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

    df = df.drop_duplicates(subset = 'patent_num')
    df = df.sort_values('patent_num', ascending=True)
    df = df.reset_index()

    return(df)
