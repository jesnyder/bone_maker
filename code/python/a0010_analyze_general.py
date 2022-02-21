import csv
import codecs
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import statistics

from a0001_retrieve_meta import retrieve_path
from a0001_retrieve_meta import clean_dataframe
from find_color import find_color

def analyze_general(name_article):
    """
    Objective: compare cell sources in the database

    Tasks:
        1. Aggregate
        2. Add a standardized column for year
        3. Count the unique values
        4. Plot the unique values
        5. Count the articles per year
    """

    print('begin analyze_general')

    tasks = [0]

    # name paths to files using article name
    # name_article = 'nih_awards'
    name_src, name_dst, name_summary, name_unique, plot_unique = name_paths(name_article)

    # tasks to complete for program
    if 0 in tasks: tasks = np.arange(1, 100, 1)
    if 1 in tasks: aggregate_articles(name_src, name_dst, name_summary)
    if 2 in tasks: add_year(name_dst, name_summary)
    if 3 in tasks: unique_values(name_dst, name_unique)
    if 4 in tasks: unique_plot(name_unique, plot_unique)
    if 5 in tasks: articles_per_year(name_article, name_dst)
    if 6 in tasks: articles_per_year(name_article, name_dst)
    if 7 in tasks: plot_articles_per_year(name_article)
    print('completed analyze_general')

def articles_per_year(name_article, name_src):
    """
    count number of articles per year
    save as dataframe
    """
    # retrieve list of all articles with metadata
    df = pd.read_csv(os.path.join(retrieve_path(name_src), 'agg_with_year' + '.csv'))
    df = clean_dataframe(df)
    print(df.columns)

    df_annual = pd.DataFrame()
    df_annual['years'] = np.arange(min(list(df['ref_year'])) , max(list(df['ref_year']))+1, 1)
    df_annual['pdf'] = [0]*len(list(df_annual['years']))
    df_annual['cdf'] = [0]*len(list(df_annual['years']))
    #df_annual = df_annual.sort_values('years', ascending=True)
    print(df_annual)

    for i in range(len(list(df_annual['years']))):

        year = float(df_annual.loc[i, 'years'])
        df_yearly = df[(df.ref_year == year)]
        df_annual.loc[i,'pdf'] = len(list(df_yearly.loc[:,'ref_year']))
        df_yearly = df[(df.ref_year <= year)]
        df_annual.loc[i,'cdf'] = len(list(df_yearly.loc[:,'ref_year']))

    print(df_annual)

    total_articles_annual = str('df_' + name_article + '_total_annual_counts')
    df_annual = clean_dataframe(df_annual)
    df_annual.to_csv(os.path.join(retrieve_path(total_articles_annual), total_articles_annual + '.csv'))
    print(df.columns)


def plot_articles_per_year(name_article):
    """
    plot annual counts
    """
    total_articles_annual = str('df_' + name_article + '_total_annual_counts')
    file = os.path.join(retrieve_path(total_articles_annual), total_articles_annual + '.csv')
    df = clean_dataframe(pd.read_csv(file))
    print(df.columns)
    print('file = ' + str(file))

    plt.close('all')
    plt.figure(figsize=(10, 10))
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    yy_lists = [list(df['pdf']) , list(df['cdf'])]
    for yy in yy_lists:

        plt.subplot(2, 1, yy_lists.index(yy)+1)

        xx = list(df['years'])
        colorMarker, colorEdge, colorTransparency = find_color(6)
        plt.scatter(xx, yy, s=40, color=colorMarker, edgecolor=colorEdge, alpha=colorTransparency)

        plt.xlabel('Year')
        plt.yscale('log')
        # plt.legend(loc ="upper left")

        if yy_lists.index(yy) == 0:
            plt.ylabel('Annual Number of Articles (mean = ' + str(round(statistics.mean(yy),2)) + ')')
            plt.title(str(sum(yy)) + ' ' + name_article + ' included in plot.')

        elif yy_lists.index(yy) == 1:
            plt.ylabel('Cumulative Number of Articles (mean = ' + str(round(statistics.mean(yy),2)) + ')')
            plt.title(str(yy[-1]) + ' ' + name_article + ' included in plot.')



    # save plot
    plot_total_articles_annual = str('plot_' + name_article + '_total_annual_counts')
    plot_dst = os.path.join(retrieve_path(plot_total_articles_annual), plot_total_articles_annual + '.png')
    plt.savefig(plot_dst, dpi = 600, edgecolor = 'w')
    plt.close('all')


def unique_plot(name_src, name_dst):
    """
    """

    for file in os.listdir(retrieve_path(name_src)):
        file_split = file.split('.')
        file_name = file_split[0]

        df_src = os.path.join(retrieve_path(name_src), file)
        df = pd.read_csv(df_src)

        xx = list(df['terms'])
        yy = list(df['counts'])

        print('file_name = ' + file_name)
        if str(xx[0]).isnumeric() and str(xx[1]).isnumeric():

            print('xx[0:2]')
            print(xx[0:2])
            print('yy[0:2]')
            print(yy[0:2])

            plt.close('all')
            plt.figure(figsize=(16, 6))

            for i in range(len(xx)):

                if str(xx[i]).isnumeric() and str(yy[i]).isnumeric():

                    x = [float(xx[i])]
                    y = [float(yy[i])]
                    colorMarker, colorEdge, colorTransparency = find_color(6)
                    plt.scatter(x, y, s=40, color=colorMarker, edgecolor=colorEdge, alpha=colorTransparency)

            # save the plot
            # print('name_dst: ' + str(name_dst))
            # print('file_name: ' + str(file_name))
            plot_dst = os.path.join(retrieve_path(name_dst), file_name + '.png')
            # print('plt save: ' + str(plot_dst))
            plt.xlabel(file_name)
            plt.ylabel('counts')
            name_src_split = name_src.split('_')
            name_article = str(name_src_split[0] + ' ' + name_src_split[1])
            plt.title(str(sum(yy)) + ' ' + name_article + ' included in plot.')

            # change to log scale
            if file_name == 'Support Year':
                plt.yscale('log')
                plt.grid()

            plt.savefig(plot_dst, dpi = 600, edgecolor = 'w')
            print('saved plot: ' + plot_dst)
            plt.close('all')


def unique_values(name_src, name_unique):
    """

    """

    # read dataframe with ref years
    df = pd.read_csv(os.path.join(retrieve_path(name_src), 'agg_with_year' + '.csv'))

    for name in df.columns:

        if 'Unnamed:' in name or 'index' == name:
            continue

        terms, counts, percentages = [], [], []

        term_list = list(df[name])

        # remove leading zeros from numbers
        for i in range(len(term_list)):
            term = term_list[i]
            if '0' in str(term):
                term_string = str(term)
                if str(term_string[0]) == '0':
                    try:
                        term = term.lstrip('0')
                        term_list[i] = term
                    except:
                        term_list[i] = term

        for i in range(len(term_list)):

            term = term_list[i]

            if term not in terms:
                count = term_list.count(term)
                terms.append(term)
                counts.append(count)

        for count in counts:
            percentages.append(round(100*count/sum(counts),4))

        df_counts = pd.DataFrame()
        df_counts['terms'] = terms
        df_counts['counts'] = counts
        df_counts['percentages'] = percentages
        df_counts = df_counts.sort_values(by=['percentages'], ascending=False)

        print('name = ')
        if '/' in name:
            name = name.replace('/', '_')
            print('name = ')

        df_counts = clean_dataframe(df_counts)
        df_counts.to_csv(os.path.join(retrieve_path(name_unique), name + '.csv'))
        print('unique counts saved to: ' + str(os.path.join(retrieve_path(name_unique), name + '.csv')))


def add_year(name_src, name_summary):
    """
    add year with standard column name to dataset
    """

    df = pd.read_csv(os.path.join(retrieve_path(name_src), 'agg' + '.csv'))
    years = []

    # nih awards reference for year column
    if 'nih_award' in str(name_src):
        year_col_name = 'Fiscal Year'
        years = list(df[year_col_name])

    # clinical trials reference for year column
    elif 'clinical_trials' in str(name_src):
        year_col_name = 'Start Date'
        dates = list(df[year_col_name])

        years = []
        for date in dates:

            try:
                # print('date = ')
                # print(date)
                date_split = date.split(' ')
                # print('date_split = ')
                # print(date_split)
                year = date_split[-1]
                # print('year = ')
                # print(year)
                years.append(float(year))
            except:
                years.append(0)

    elif 'nsf_awards' in str(name_src):

        years = []
        dates = list(df['StartDate'])
        for date in dates:
            date_split = date.split('/')
            year = date_split[-1]
            year = float(year)
            years.append(year)


    # patent reference for year column
    elif 'patents' in str(name_src):

        for i in range(len(list(df['patent_date']))):
            try:
                date = list(df['patent_date'])[i]
                date_split = date.split(' ')
                years.append(float(date_split[-1]))
            except:
                try:
                    date = list(df['file_date'])[i]
                    date_split = date.split(' ')
                    years.append(float(date_split[-1]))
                except:
                    years.append('0')

    elif 'gscholar' in str(name_src):

        for info in list(df['publication_info']):

            try:
                year_findall = re.findall('[0-9]{4}', str(info))
                year = year_findall[0]
                print('year = ' + str(year))
                years.append(int(year))
            except:
                years.append(0)

    print('len(df.iloc[:,0]) = ' + str(len(df.iloc[:,0])))
    print('len(years) = ' + str(len(years)))
    df_with_year = df
    df_with_year['ref_year'] = years

    print('length before dropping 0 years = ' + str(len(list(df_with_year['ref_year']))))
    df_with_year = df_with_year[(df_with_year.ref_year > 0)]
    print('length after dropping 0 years = ' + str(len(list(df_with_year['ref_year']))))

    file_name = os.path.join(retrieve_path(name_src), 'agg_with_year' + '.csv')
    df_with_year = clean_dataframe(df_with_year)
    df_with_year.to_csv(file_name)
    summarize(file_name, name_summary)


def aggregate_articles(name_src, name_dst, name_summary):
    """
    aggregate articles
    save as a
    """

    df_agg = pd.DataFrame()

    for file in os.listdir(retrieve_path(name_src)):

        df_src = os.path.join(retrieve_path(name_src), file)
        # print('file = ' + str(file))
        # print('path = ' + str(retrieve_path(name_src)))
        # print('df_patent = ' + str(df_src))

        df = pd.read_csv(df_src)
        df_agg = df_agg.append(df)

    print('before dropping duplicated during aggregation: len of all articles = ' + str(len(df_agg.iloc[:,0])))

    unique_names = ['Serial Number', 'url', 'publication_info', 'title_link', 'abstract', 'claims', ]

    for name in unique_names:
        try:
            df_agg = df_agg.sort_values(by=['Support Year'], ascending=False)
        except:
            print('support year column not found')
        try:
            df_agg = df_agg.drop_duplicates(subset=[name])
        except:
            print('no duplicated dropped.')

    print('after dropping duplicated during aggregation: len of all articles = ' + str(len(df_agg.iloc[:,0])))

    for name in df_agg.columns:
        if 'year' in name:
            df_agg = df_agg.sort_values(by=[name], inplace=True)

        if 'Unnamed: ' in name:
            del df_agg[name]

    # save aggregated articles
    df_agg = df_agg.reset_index()
    # print('df_agg = ')
    # print(df_agg)

    df_agg = clean_dataframe(df_agg)
    file_name = os.path.join(retrieve_path(name_dst), 'agg' + '.csv')
    df_agg.to_csv(file_name)

    summarize(file_name, name_summary)


def summarize(name_src, name_summary):
    """

    """
    df = pd.read_csv(os.path.join(name_src))

    # savesummary articles
    df_summary = pd.DataFrame()
    df_summary['counts'] = [len(list(df.iloc[:,1]))]

    for name in df.columns:
        df_summary[name] = str((df.iloc[1][name]))

    df_summary = df_summary.T
    # print('df_summary = ')
    # print(df_summary)
    df_summary = clean_dataframe(df_summary)
    df_summary.to_csv(os.path.join(retrieve_path(name_summary)))


def name_paths(name_article):
    """
    provide article type
    make the needed files
    """

    name_src = str(name_article + '_search')
    name_dst = str('df_' + name_article + '_search')
    name_summary = str('sum_' + name_article)
    name_unique = str(name_article + '_unique')
    plot_unique = str(name_article + '_unique_plot')


    return name_src, name_dst, name_summary, name_unique, plot_unique
