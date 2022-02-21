from bs4 import BeautifulSoup
import datetime
import json
import lxml
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import random
from serpapi import GoogleSearch
import shutil
import re
import requests
import time

from a0001_admin import retrieve_path
from a0001_admin import clean_dataframe
from a0001_admin import retrieve_datetime


"""
Reference: https://python.plainenglish.io/scrape-google-scholar-with-python-fc6898419305
"""


def article_df(term):
    """

    """
    df = pd.DataFrame()

    name_article = 'gscholar'
    src_path_name = name_article + '_article_json'
    src_path = retrieve_path(src_path_name)
    #print('src_path = ')
    #print(src_path)

    for file in os.listdir(src_path):

        # read in json
        src_file = os.path.join(src_path, file)

        if not file.endswith('.json'): continue
        #if term not in str(file): continue

        #print('src_file = ' + str(src_file))
        df_file = pd.read_json(src_file)

        df = pd.DataFrame.append(df, df_file)
        #df = df.sort_values('citations', ascending=False)
        #df = df.drop_duplicates(subset = 'url')

    #df = df.sort_values('citations', ascending=False)
    #df = df.drop_duplicates(subset = 'url')
    df = df.reset_index()

    del df['index']
    #print(df)

    name_article = 'gscholar'
    dst_path_name = name_article + '_article_df'
    dst_path = retrieve_path(dst_path_name)
    df_file = os.path.join(dst_path, term + '.csv')
    df.to_csv(df_file)


def url_lookup(search_term):
    """

    """
    name_article = 'gscholar'
    src_path_name = name_article + '_article_json'
    src_path = retrieve_path(src_path_name)
    shutil.rmtree(src_path)
    #print('src_path = ')
    #print(src_path)



    for file in os.listdir(src_path):

        # read in json
        src_file = os.path.join(src_path, file)

        if file.endswith('.json'):

            if term in str(file):

                print('src_file = ' + str(src_file))
                df_file = pd.read_json(src_file)

                df = pd.DataFrame.append(df, df_file)
                #df = df.sort_values('citations', ascending=False)
                df = df.drop_duplicates(subset = 'url')
    # sort
    df = df.sort_values('citations', ascending=False)
    df = df.drop_duplicates(subset = 'url')
    df = df.reset_index()

    del df['index']
    print(df)

    # print(df['citations'])


    name_article = 'gscholar'
    dst_path_name = name_article + '_article_df'
    dst_path = retrieve_path(dst_path_name)
    df_file = os.path.join(dst_path, term + '.csv')
    df.to_csv(df_file)


def Ascrape_json(search_term):
    """

    """

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    num_list = np.arange(0, 500, 1, dtype=int)

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


# working programs below line

def article_json(term):
    """
    parse html into json
    """
    name_article = 'gscholar'
    dst_path_name = name_article + '_article_json'
    dst_path = retrieve_path(dst_path_name)
    shutil.rmtree(dst_path)

    name_article = 'gscholar'
    src_path_name = name_article + '_article_html'
    src_path = retrieve_path(src_path_name)


    for file in os.listdir(src_path):

        # read in html
        src_file = os.path.join(src_path, file)
        HtmlFile = open(src_file, 'r', encoding='utf-8')
        contents = HtmlFile.read()
        HtmlFile.close()

        html = contents
        soup = BeautifulSoup(html, 'lxml')

        site = soup.find("meta",  {"property":"og:site_name"})
        site = site["content"] if site else None

        type = soup.find("meta",  {"property":"og:type"})
        type = type["content"] if type else None

        title = soup.find("meta",  {"property":"og:title"})
        title = title["content"] if title else None

        desc = soup.find("meta",  {"property":"og:description"})
        desc = desc["content"] if desc else None

        url = soup.find("meta",  {"property":"og:url"})
        url = url["content"] if url else None

        updated_time = soup.find("meta",  {"property":"og:updated_time"})
        updated_time = updated_time["content"] if updated_time else None

        citation_author = soup.find("meta",  {"property":"citation_author"})
        citation_author = citation_author["content"] if citation_author else None

        citation_author_institution = soup.find("meta",  {"property":"citation_author_institution"})
        citation_author_institution = citation_author_institution["content"] if citation_author_institution else None

        abstract = soup.find("h2", {"class=":"abstract"})
        abstract = abstract["content"] if abstract else None

        data = []
        data.append({
            'site': site,
            'type': type,
            'title': title,
            'url': url,
            'description': desc,
            'citation_author': citation_author,
            'citation_author_institution': citation_author_institution,
            'updated_time': updated_time,
            'abstract': abstract,
            #'title_link': title_link,
            #'publication_info': publication_info,
            #'snippet': snippet,
            #'citations': citations,
            #'cited_by': f'https://scholar.google.com{cited_by}',
            #'related_articles': f'https://scholar.google.com{related_articles}',
            #'all_article_versions': f'https://scholar.google.com{all_article_versions}',
            #'abstract': abstract,
            #'journal': journal,
            #'institution': institution,
            #'date': date,
        })

        #print(json.dumps(data, indent = 2, ensure_ascii = False))

        name_article = 'gscholar'
        dst_path_name = name_article + '_article_json'
        dst_path = retrieve_path(dst_path_name)


        file_strip = file.split('.')
        file_name = file_strip[0]
        file = os.path.join(dst_path, file_name + '.json')

        out_file = open(file , "w")
        json.dump(data, out_file, indent = 2, ensure_ascii = False)
        out_file.close()


def article_html(term):
    """
    save html from article
    """
    name_article = 'gscholar'
    dst_path_name = name_article + '_query_df'
    dst_path = retrieve_path(dst_path_name)
    df_file = os.path.join(dst_path, term + '.csv')
    df = pd.read_csv(df_file)
    df = clean_dataframe(df)
    print(df)

    for url in list(df['title_link']):

        print('url = ')
        print(url)

        url_name = url.replace('/','_')
        url_name = url_name.replace(':','_')
        url_name = url_name.replace('.','_')
        url_name = url_name[:25]

        # was this article already scraped?
        name_article = 'gscholar'
        dst_path_name = name_article + '_article_html'
        dst_path = retrieve_path(dst_path_name)
        if str(url_name + '.html') in os.listdir(dst_path):
            continue

        # set get terms
        headers = {
            'User-agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
            }

        proxies = {
            'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
            }

        # introduce a minimum wait time with a random interval to get request
        wait_timer = random.randint(0, 50)
        print('Wait: ' + str(retrieve_datetime()))
        time.sleep(60 + 0.5*wait_timer)
        html = requests.get(url, headers=headers, proxies=proxies).text
        print('Wait: ' + str(retrieve_datetime()))

        print('html = ')
        print(html)

        soup = html

        # check for errors
        error_found = False
        error = str('Our systems have detected unusual traffic from your computer network.  This page checks to see if it')
        if error in str(soup):
            print('Automated search detected.')
            error_found = True
            return(error_found)

        # compose dst file name
        dst_file = os.path.join(dst_path, url_name + '.html')
        print('html file =  ' + str(dst_file))

        # save html to a file
        out_file = open(dst_file , "w")
        out_file.write(str(soup))
        out_file.close()

        if error_found == True:
            return(error_found)


def json_to_dataframe(term):
    """

    """
    df = pd.DataFrame()

    # retrieve archival json
    src_path = retrieve_path('json_archival')
    for file in os.listdir(src_path):

        src_file = os.path.join(src_path, file)

        if file.endswith('.json'):

            if term not in str(file): continue

            #print('src_file = ' + str(src_file))
            df_file = pd.read_json(src_file)
            df = pd.DataFrame.append(df, df_file)
            df = df.sort_values('citations', ascending=False)
            df = df.drop_duplicates(subset = 'title_link')


    # retrieve scrape json
    name_article = 'gscholar'
    src_path_name = name_article + '_query_json'
    src_path = retrieve_path(name_article + '_query_json')
    #print('src_path = ')
    #print(src_path)

    for file in os.listdir(src_path):

        # read in json
        src_file = os.path.join(src_path, file)

        if file.endswith('.json'):

            if term not in str(file): continue

            #print('src_file = ' + str(src_file))
            df_file = pd.read_json(src_file)
            df = pd.DataFrame.append(df, df_file)
            df = df.sort_values('citations', ascending=False)
            df = df.drop_duplicates(subset = 'title_link')


    # sort
    df = df.sort_values('citations', ascending=False)
    df = df.drop_duplicates(subset = 'title_link')
    df = df.reset_index()
    del df['index']
    #print(df)


    name_article = 'gscholar'
    dst_path_name = name_article + '_query_df'
    dst_path = retrieve_path(dst_path_name)
    df_file = os.path.join(dst_path, term + '.csv')
    df.to_csv(df_file)


def scrape_json(term):
    """
    read in saved html
    convert to json
    """
    name_article = 'gscholar'
    dst_path = retrieve_path(name_article + '_query_json')
    shutil.rmtree(dst_path)

    name_article = 'gscholar'
    src_path_name = name_article + '_query_html'
    src_path = retrieve_path(src_path_name)
    #print('src_path = ')
    #print(src_path)

    for file in os.listdir(src_path):

        # read in html
        src_file = os.path.join(src_path, file)
        HtmlFile = open(src_file, 'r', encoding='utf-8')
        contents = HtmlFile.read()
        HtmlFile.close()

        # contents of html
        html = contents
        soup = BeautifulSoup(html, 'lxml')
        #print('soup = ')
        #print(soup)


        # Scrape just PDF links
        for pdf_link in soup.select('.gs_or_ggsm a'):
            pdf_file_link = pdf_link['href']
            print(pdf_file_link)

            # JSON data will be collected here
            data = []


            # Container where all needed data is located
            for result in soup.select('.gs_ri'):

                title = result.select_one('.gs_rt').text
                title_link = result.select_one('.gs_rt a')['href']
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

                #print('1 txt-cite = ' + str(txt_cite))

                try:
                    citations = txt_cite.split(' ')
                except:
                    citations = '0 0 0'

                #print('2 citations = ' + str(citations))
                citations = (citations[-1])
                #print('3 citations = ' + str(citations))

                try:
                    citations = int(citations)
                except:
                    citations = 0

                    #print('4 citations = ' + str(citations))

                data.append({
                    'title': title,
                    'title_link': title_link,
                    'publication_info': publication_info,
                    'snippet': snippet,
                    'citations': citations,
                    'cited_by': f'https://scholar.google.com{cited_by}',
                    'related_articles': f'https://scholar.google.com{related_articles}',
                    'all_article_versions': f'https://scholar.google.com{all_article_versions}',
                    })

            #print(json.dumps(data, indent = 2, ensure_ascii = False))

            # build the file to save json
            name_article = 'gscholar'
            dst_path = retrieve_path(name_article + '_query_json')
            file_split = file.split(' ')
            file_num = file_split[1]
            f = os.path.join(dst_path, term + '_' + str(file_num) + '_' + retrieve_datetime() + '.json')

            out_file = open(f , "w")
            json.dump(data, out_file, indent = 2, ensure_ascii = False)
            out_file.close()
            #print('json file =  ' + str(file))


def scrape_html(term,num):
    """
    get and save html contents to file
    from google scholar
    """
    # set get terms
    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        }

    proxies = {
        'http': os.getenv('HTTP_PROXY') # or just type proxy here without os.getenv()
        }

    # build url
    print('num = ' + str(num))
    url = 'https://scholar.google.com/scholar?'
    url = url + 'start=' + str(int(num*10))
    url = url + '&q=' + term
    url = url + '&hl=en&as_sdt=0,5'
    print('url = ')
    print(url)

    # introduce a minimum wait time with a random interval to get request
    wait_timer = random.randint(0, 50)
    print('Wait: ' + str(retrieve_datetime()))
    time.sleep(60 + 0.5*wait_timer)
    html = requests.get(url, headers=headers, proxies=proxies).text
    print('Wait: ' + str(retrieve_datetime()))

    print('html = ')
    print(html)

    soup = html

    # check for errors
    error_found = False
    error = str('Our systems have detected unusual traffic from your computer network.  This page checks to see if it')
    error_2 = str( 'sorry but it appears that there has been an internal server error while processing your request. Our engineers have been notified and are working to resolve the issue.')
    if error in str(soup):
        print('Automated search detected.')
        error_found = True
    if error_2 in str(soup):
        print('Internal server error detected.')
        error_found = True

    # save if no error
    if error_found == False:

        # compose dst file name
        name_article = 'gscholar'
        dst_path_name = name_article + '_query_html'
        print(dst_path_name)
        print('dst_path = ')
        dst_path = retrieve_path(dst_path_name)
        print(dst_path)
        dst_file = os.path.join(dst_path, term + ' '  + str(num) + ' ' + str(retrieve_datetime()) + '.html')
        print('html file =  ' + str(dst_file))

        # save html to a file
        out_file = open(dst_file , "w")
        out_file.write(str(soup))
        out_file.close()

    return(error_found)


if __name__ == "__main__":
    main()
