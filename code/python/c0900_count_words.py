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



def count_words():
    """

    """

    # all_words
    count_all_words()

    # count materials
    count_materials()

    # plot materials
    plot_materials()


def plot_materials():
    """
    plot materials
    """

    df_file = os.path.join(retrieve_path('word_count_material'))
    df = pd.read_csv(df_file)

    years = list(df['patent_year'])

    materials = retrieve_materials()

    # figure
    plt.close('all')
    figure, axes = plt.subplots()

    plt.figure(figsize=(16, 6))

    plt.subplot(121)

    for material in materials:

        count_yearly = []
        year_list = np.arange(min(years), max(years), 1)
        for year in year_list:
            df_yearly =  df[(df.patent_year == year)]

            count_yearly.append(sum(list(df_yearly[material])))

        plt.scatter(year_list, count_yearly, label = material)

    plt.xlabel('Years')
    plt.ylabel('Number of Patents')
    plt.title('Yearly Patent Count')
    plt.legend(loc ="upper left")

    plt.subplot(122)

    for material in materials:

        count_yearly = []
        year_list = np.arange(min(years), max(years), 1)
        for year in year_list:
            df_yearly =  df[(df.patent_year <= year)]

            count_yearly.append(sum(list(df_yearly[material])))

        plt.scatter(year_list, count_yearly, label = material)

    plt.xlabel('Years')
    plt.ylabel('Number of Patents')
    plt.title('Cumulative Patent Count')
    plt.legend(loc ="upper left")

    df_file = os.path.join(retrieve_path('material_count_yearly'))
    plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')


def retrieve_materials():

    # list materials
    df_file = os.path.join('user_provided', 'scaffold_design_elements', 'materials' + '.csv')
    df_materials = pd.read_csv(df_file)
    materials = list(df_materials['materials'])

    return(materials)

def count_materials():
    """

    """

    df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop_time' + '.csv')
    df = pd.read_csv(df_file)

    descriptions = list(df['description'])
    claims = list(df['claims'])
    title = list(df['title'])

    # list materials
    df_file = os.path.join('user_provided', 'scaffold_design_elements', 'materials' + '.csv')
    df_materials = pd.read_csv(df_file)
    materials = list(df_materials['materials'])

    df_counts = pd.DataFrame()
    df_counts['patent_num'] = list(df['patent_num'])
    df_counts['file_year'] = list(df['file_year'])
    df_counts['patent_year'] = list(df['patent_year'])

    # loop through materials
    for material in materials:

        print('material = ' + material)

        df_counts[material] = len(list(df['patent_year']))*[0]

        for i in range(len(claims)):

            claim = claims[i]
            claim = str(claim)
            claim = claim.lower()

            if material in claim:

                df_counts.loc[i , material] = 1
                assert( df_counts.loc[i , material] == 1 )
                print(df_counts.loc[i][material])

                print('material found.')
                print('% complete = ' + str(100*i/len(claims)))


        for i in range(len(descriptions)):
            description = descriptions[i]
            description = str(description)
            description = description.lower()

            if material in description:
                df_counts.loc[i , material] = 1
                assert( df_counts.loc[i , material] == 1 )
                print(df_counts.loc[i][material])


        df_file = os.path.join(retrieve_path('word_count_material'))
        df_counts.to_csv(df_file)

    names = df_counts.columns
    for name in names:
        print(name)
        try:
            print(sum(list(df_counts[name])))
        except:
            print('no value to print')


def clean_text(text):
    """

    """
    string = str(text)
    string = string.lower()
    string = string.replace('[', ' ')
    string = string.replace(']', ' ')
    string = string.replace('(', ' ')
    string = string.replace(')', ' ')
    string = string.replace(',', ' ')
    string = string.replace('.', ' ')
    string = string.replace(':', ' ')

    """
    string = string.replace('is', ' ')
    string = string.replace('it', ' ')
    string = string.replace('an', ' ')
    string = string.replace('a', ' ')
    string = string.replace('the', ' ')
    string = string.replace('with', ' ')
    string = string.replace('its', ' ')
    """

    return(string)



def count_all_words():

    df_file = os.path.join(retrieve_path('df_aggregated'), 'agg' + '.csv')
    df = pd.read_csv(df_file)

    names = df.columns

    print('names')
    print(names)

    descriptions = list(df['description'])
    claims = list(df['claims'])
    title = list(df['title'])

    all_words = ''

    for description in descriptions:

        string = clean_text(description)
        all_words += str(string) + ' '

    for claim in claims:
        string = clean_text(claim)
        all_words += str(string) + ' '

    word_list = all_words.split(' ')

    print('claims and description listed as bulk individual words')

    unique_word_list = []
    count_word_list = []

    for word in word_list:

        if word not in unique_word_list:

            print('word found = ' + str(word))

            unique_word_list.append(word)
            count_word_list.append(word_list.count(word))

        df = pd.DataFrame()
        df['word'] = unique_word_list
        df['count'] = count_word_list
        df.sort_values(by=['count'], inplace=False)
        file_name = os.path.join(retrieve_path('word_count_all'))
        df.to_csv(file_name)
