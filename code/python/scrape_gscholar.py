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

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_datetime


def scrape_gscholar():
    """
    Reference: https://python.plainenglish.io/scrape-google-scholar-with-python-fc6898419305

    """

    print("running scrape_gscholar")

    search_terms = []
    #search_terms.append('genetic+engineering+mesenchymal')
    #search_terms.append('mesenchymal+mechanosensitivity')
    search_terms.append('RoosterBio')

    tasks = [1]

    for search_term in search_terms:

        if 1 in tasks: scrape_json(search_term)
        if 2 in tasks: json_to_dataframe(search_term)
        if 3 in tasks: url_lookup(search_term)


def url_lookup(search_term):
    """

    """

    path = retrieve_path('df_gscholar')
    df_file = os.path.join(path, search_term + '.csv')
    df = pd.read_csv(df_file)
    print(df)

    df['lead_author'] = len(list(df['title_link']))*['None']
    df['anchor_author'] = len(list(df['title_link']))*['None']
    df['date'] = len(list(df['title_link']))*['None']
    df['description'] = len(list(df['title_link']))*['None']
    df['author'] = len(list(df['title_link']))*['None']
    df['journal'] = len(list(df['title_link']))*['None']
    df['abstract'] = len(list(df['title_link']))*['None']
    #df['author'] = len(list(df['title_link']))*['None']

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

        html = requests.get(url).text
        page = BeautifulSoup(html, "html.parser")


        print('date = ')

        try:
            date = page.findAll(attrs={"name": re.compile(r"citation_date", re.I)})
            date = date[0]['content']
        except:
            date = None
        df.at[row_number, 'date'] = date
        print(date)

        # description
        print('description = ')
        try:
            desc = page.findAll(attrs={"name": re.compile(r"description", re.I)})
            desc = desc[0]['content']
        except:
            desc = None
        df.at[row_number, 'description'] = desc
        print(desc)

        # author
        print('lead_author = ')
        try:
            author = page.findAll(attrs={"name": re.compile(r"citation_author", re.I)})
            author = author[0]['content']
        except:
            author = None
        df.at[row_number, 'lead_author'] = author
        print(author)

        # author
        print('anchor_author =')
        try:
            author = page.findAll(attrs={"name": re.compile(r"citation_author", re.I)})
            author = author[-1]['content']
        except:
            author = None
        df.at[row_number, 'anchor_author'] = author
        print(author)

        """
        # institution
        print('institution = ')
        try:
            institution = page.findAll(attrs={"name": re.compile(r"citation_author_institution", re.I)})
            institution = institution[0]['content']
        except:
            institution = None
        df.at[row_number, 'institution'] = institution
        print(institution)
        """

        # journal
        print('journal = ')
        try:
            journal = page.findAll(attrs={"name": re.compile(r"citation_journal_title", re.I)})
            journal = journal[0]['content']
        except:
            journal = None
        df.at[row_number, 'journal'] = journal
        print(journal)

        # abstract
        print('abstract = ')
        try:
            abstract = page.findAll(attrs={"name": re.compile(r"citation_abstract", re.I)})
            abstract = abstract[0]['content']
        except:
            abstract = None
        df.at[row_number, 'abstract'] = abstract
        print(abstract)

        print('url = ' + str(url))

        path = retrieve_path('df_gscholar')
        df_file = os.path.join(path, search_term + ' v02' +'.csv')
        df.to_csv(df_file)


def json_to_dataframe(search_term):
    """

    """
    path = retrieve_path('json_gscholar_patent')

    df = pd.DataFrame()

    file_list = os.listdir(path)

    print('file_list = ')
    print(file_list)

    for file in file_list:

        if file.endswith('.json'):

            if search_term in str(file):

                jsonfile = os.path.join(path, file)
                df_file = pd.read_json(jsonfile)

                df = pd.DataFrame.append(df, df_file)

    print(df)

    # sort
    df = df.sort_values('citations', ascending=False)
    df = df.drop_duplicates(subset = 'title_link')
    df = df.reset_index()

    del df['index']
    print(df)

    print(df['citations'])

    path = retrieve_path('df_gscholar')
    df_file = os.path.join(path, search_term + '.csv')
    df.to_csv(df_file)


def scrape_json(search_term):
    """

    """

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    num_list = np.arange(0, 2, 1, dtype=int)

    for num in num_list:
        print('num = ' + str(num))

        url = 'https://scholar.google.com/scholar?'
        url = url + 'start=' + str(int(num*10))
        url = url + '&q=' + search_term
        url = url + '&hl=en&as_sdt=0,5'
        print('url = ')
        print(url)

        #url = 'https://scholar.google.com/scholar?'
        #url = url + 'hl=en&as_sdt=0%2C5&q=' + search_term + '&oq='
        #print('url = ')
        #print(url)

        time_string = retrieve_datetime()
        print('Wait: ' + time_string)
        time.sleep(30)

        html = requests.get(url, headers=headers, proxies=proxies).text

        # Delay scraping to circumvent CAPCHA
        time.sleep(30)
        time_string = retrieve_datetime()
        print('Wait: ' + time_string)

        soup = BeautifulSoup(html, 'lxml')

        print('soup = ')
        print(soup)

        error = str('Our systems have detected unusual traffic from your computer network.  This page checks to see if it')

        if error in str(soup):
            print('Automated search detected.')
            # break

        # Scrape just PDF links
        for pdf_link in soup.select('.gs_or_ggsm a'):
            pdf_file_link = pdf_link['href']
            print(pdf_file_link)

        # JSON data will be collected here
        data = []

        # Container where all needed data is located
        for result in soup.select('.gs_top'):

            print('result = ')
            print(result)

            title = result.select_one('.gs_rt').text

            try:
                title_link = result.select_one('.gs_rt a')['href']
            except:
                title_link = None

            publication_info = result.select_one('.gs_a').text
            snippet = result.select_one('.gs_rs').text
            cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
            related_articles = result.select_one('a:nth-child(4)')['href']
            try:
                all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
            except:
                all_article_versions = None

            # get number of citations for each paper
            try:
                txt_cite = result.find("div", class_="gs_fl").find_all("a")[2].string
            except:
                txt_cite = '0 0 0'

            try:
                citations = txt_cite.split(' ')
            except:
                citations = '0 0 0'

            citations = (citations[-1])

            try:
                citations = int(citations)
            except:
                citations = 0

            # get the year of publication of each paper
            txt_year = result.find("div", class_="gs_a").text
            year = re.findall('[0-9]{4}', txt_year)
            if year:
                year = list(map(int,year))[0]
            else:
                year = 0


            data.append({
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet,
                'citations': citations,
                'cited_by': f'https://scholar.google.com{cited_by}',
                'related_articles': f'https://scholar.google.com{related_articles}',
                'all_article_versions': f'https://scholar.google.com{all_article_versions}',
                'year': year,
                })

            json_string = json.dumps(data, indent = 2, ensure_ascii = False)
            print(json_string)

            time_string = retrieve_datetime()


            path = retrieve_path('json_gscholar_patent')
            file = os.path.join(path, search_term + ' ' + time_string + '.json')
            print('json file saved: ')
            print(file)


    print("completed scrape_gscholar")



if __name__ == "__main__":
    main()
