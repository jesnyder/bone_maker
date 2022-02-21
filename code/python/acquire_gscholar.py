from bs4 import BeautifulSoup
import datetime
import json
import lxml
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from serpapi import GoogleSearch
import re
import requests
import time

from a0001_retrieve_meta import retrieve_path
from a0001_retrieve_meta import retrieve_datetime

"""
from c0010_analyze_general import analyze_general
from c0010_analyze_general import name_paths
from c0020_compare_terms import compare_terms
from scrape_gscholar import scrape_gscholar
from find_color import find_color
"""

def acquire_gscholar(term):
    """

    """
    print('beginning acquire_gscholar')

    num_list = np.arange(0, 8000000, 1, dtype=int)
    scrape_lxml(term, num_list)
    scrape_lxml_per_article(term)

    print('completed acquire_gscholar')


def scrape_lxml(term, num_list):
    """
    scrape html from website
    save as lxml
    """

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    for num in num_list:
        print('num = ' + str(num))
        url = 'https://scholar.google.com/scholar?'
        url = url + 'start=' + str(int(num*10))
        url = url + '&q=' + term
        url = url + '&hl=en&as_sdt=0,5'
        print('url = ')
        print(url)

        print('Wait: ' + str(retrieve_datetime()))
        time.sleep(60)
        html = requests.get(url, headers=headers, proxies=proxies).text
        print('Wait: ' + str(retrieve_datetime()))

        soup = BeautifulSoup(html, 'lxml')
        print('soup = ')
        print(soup)

        path = retrieve_path('lxml_gscholar')
        file = os.path.join(path, term + ' '  + str(num) + ' ' + str(retrieve_datetime()) + '.xml')
        print('lxml file =  ' + str(file))

        f = open(file , "w")
        f.write(str(soup))
        f.close()


def scrape_lxml_per_article(term):
    """

    """

    path = retrieve_path('df_gscholar_query')
    df_file = os.path.join(path, search_term + '.csv')
    df = pd.read_csv(df_file)
    print(df)

    title_link = list(df['title_link'])

    for url in title_link:

        row_number = df[df['title_link'] == url].index

        print('row_number = ')
        print(row_number)

        if len(list(row_number)) < 1:
            continue

        row_number = list(row_number)[0]
        print('row_number = ' + str(row_number))
        print('url = ')
        print(url)

        print('Wait: ' + str(retrieve_datetime()))
        time.sleep(60)
        html = requests.get(url).text

        soup = BeautifulSoup(html, "html.parser")

        path = retrieve_path('lxml_gscholar_article')
        file = os.path.join(path, term + ' '  + str(num) + ' ' + str(retrieve_datetime()) + '.xml')
        print('article lxml file =  ' + str(file))

        f = open(file , "w")
        f.write(str(soup))
        f.close()
