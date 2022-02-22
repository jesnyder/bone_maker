import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import clean_dataframe



def count_words():
    """
    count the words

    untargetted:
    (1) count the frequency of all words in the patent title, claims, and description

    targetted:
    (2) use lists of scaffold design paramters and count if the word appears in the patent
    (3) sum how many patents mention a term each year
    (4) calculate the percentage of patents that cite a term each year
    (5) plot the ratio of patents that include a term each year


    """

    tasks = [2]

    # untargetted text analysis
    # count the frequency of all words in patents
    if 1 in tasks: untargetted_word_count()
    if 2 in tasks: sort_untargetted()

    # targetted text analysis
    # list files in a folder
    path = retrieve_path('scaffold_design_elements')
    for file in os.listdir(path):

        path_file = os.path.join(path, file)
        print('path_file = ' + str(path_file))
        df = pd.read_csv(path_file)
        df = clean_dataframe(df)
        # print(df)

        # identify if scaffold parameters found in each patent
        col_name = list(df.columns)[0]
        terms = list(df[col_name])

        # count if a term appears in a patent
        if 3 in tasks:count_words_each_patent(col_name, terms)

        # count frequency of scaffold design elements per year
        if 4 in tasks: yearly_term_count(col_name, terms)
        if 5 in tasks: cumulative_term_count(col_name, terms)
        if 6 in tasks: yearly_term_percent(col_name, terms)

        # plot counts - yearly and cumulative
        if 7 in tasks: plot_term_count(col_name, terms)
        if 8 in tasks: plot_term_cumulative(col_name, terms)

        # bar chart / flow chart frequency
        if 9 in tasks: plot_bar_percentage(col_name, terms)


def plot_term_count(col_name, terms):
    """
    retrieve dataframe
    plot barchart
    """
    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('term_count_yearly'), col_name + '.csv')
    df = pd.read_csv(file_name)

    figure, axes = plt.subplots()
    plt.figure(figsize=(16, 6))
    plt.subplot(111)

    xx = list(df['year'])
    for term in terms:
        yy = list(df[term])
        plt.plot(xx, yy, '-o', label = term)

    plt.xlabel('Years')
    plt.ylabel('Yearly Number of Patents')
    plt.yscale('log')
    plt.title(col_name)
    plt.legend(bbox_to_anchor=(1, 0.7), loc ="upper left")

    df_file = os.path.join(retrieve_path('plot_term_yearly'), col_name + '.png')
    plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')


def plot_term_cumulative(col_name, terms):
    """
    retrieve dataframe
    plot barchart
    """
    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('df_term_cumulative'), col_name + '.csv')
    df = pd.read_csv(file_name)

    figure, axes = plt.subplots()
    plt.figure(figsize=(16, 6))
    plt.subplot(111)

    xx = list(df['year'])
    for term in terms:
        yy = list(df[term])
        plt.plot(xx, yy, '-o',  label = term)

    plt.xlabel('Years')
    plt.ylabel('Cumulative Number of Patents')
    plt.yscale('log')
    plt.title(col_name)
    plt.legend(bbox_to_anchor=(1, 0.7), loc ="upper left")

    df_file = os.path.join(retrieve_path('plot_term_cumulative'), col_name + '.png')
    plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')



def plot_bar_percentage(col_name, terms):
    """
    retrieve dataframe
    plot barchart
    """
    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('term_count_percentage'), col_name + '.csv')
    df = pd.read_csv(file_name)

    # figure
    try:
        plt.close('all')
    except:
        print('did not close plots.')

    figure, axes = plt.subplots()
    plt.figure(figsize=(16, 6))
    plt.subplot(111)

    xx = list(df['year'])
    for i in range(len(terms)):

        term = terms[i]
        yy = list(df[term])

        # print('i = ' + str(i))

        offsets = [0] * len(list(df['year']))

        if i > 0:
            offsets = []
            for k in range(len(list(df['year']))):
                offset = 0
                for j in range(i):
                    term = terms[j]
                    offset = offset + df.loc[k][term]
                offsets.append(offset)

        #print('len(xx) = ' + str(len(xx)))
        #print('len(offsets) = ' + str(len(offsets)))

        assert len(offsets) == len(xx)
        assert len(offsets) == len(yy)

        plt.bar(xx, yy, width=1.0, bottom=offsets, align='center', label = terms[i])


    plt.xlabel('Years')
    plt.ylabel('Percentage of Patents')
    plt.title(col_name)
    plt.legend(bbox_to_anchor=(1, 0.9), loc ="upper left")

    df_file = os.path.join(retrieve_path('term_percentage_bar'), col_name + '.png')
    plt.savefig(df_file, bbox_inches='tight', dpi=600, edgecolor = 'w')


def yearly_term_percent(col_name, terms):
    """
    retrieve a database
    convert from counts to percentage
    """
    # retrieve list of counts per year
    file_name = os.path.join(retrieve_path('term_count_yearly'), col_name + '.csv')
    df = pd.read_csv(file_name)

    # build dataframe
    df_percent = pd.DataFrame()
    df_percent['year'] = list(df['year'])

    totals = []
    for i in range(len(list(df['year']))):
        total = 0
        for term in terms:
            for col in list(df.columns):
                if col == term:
                    total = df.iloc[i][term] + total
        totals.append(total)
    df['totals'] = totals

    for term in terms:

        df_percent[term] = len(list(df['year'])) * [0]

        for i in range(len(list(df['year']))):

            total = df.iloc[i]['totals']
            value = df.loc[i, term]
            assert value <= total
            df_percent.loc[i , term] = value/total

            if total == 0:
                df_percent.loc[i , term] = 0

    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('term_count_percentage'), col_name + '.csv')
    df_percent.to_csv(file_name)


def yearly_term_count(col_name, terms):
    """
    total words each year
    save as datarame
    """
    # retrieve list of patents
    file_name = os.path.join(retrieve_path('word_count_per_patent'), col_name + '.csv')
    print('file name = ' + str(file_name))
    df = pd.read_csv(file_name)
    years = np.arange(min(list(df['patent_year'])), max(list(df['patent_year'])), 1)

    # build dataframe
    df_yearly = pd.DataFrame()
    df_yearly['year'] = years

    # count the number of patents with the terms per year
    for term in terms:
        df_yearly[term] = len(years) * [0]

        for i in range(len(years)):
            df_subset = df[(df.patent_year == years[i])]
            count = sum(list(df_subset[term]))
            df_yearly.loc[i , term] = count

    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('term_count_yearly'), col_name + '.csv')
    df_yearly.to_csv(file_name)


def cumulative_term_count(col_name, terms):
    """
    total words each year
    save as datarame
    """
    # retrieve list of patents
    file_name = os.path.join(retrieve_path('word_count_per_patent'), col_name + '.csv')
    df = pd.read_csv(file_name)
    years = np.arange(min(list(df['patent_year'])), max(list(df['patent_year'])), 1)

    # build dataframe
    df_yearly = pd.DataFrame()
    df_yearly['year'] = years

    # count the number of patents with the terms per year
    for term in terms:
        df_yearly[term] = len(years) * [0]

        for i in range(len(years)):
            df_subset = df[(df.patent_year <= years[i])]
            count = sum(list(df_subset[term]))
            df_yearly.loc[i , term] = count

    # save count of terms per year as a dataframe
    file_name = os.path.join(retrieve_path('df_term_cumulative'), col_name + '.csv')
    df_yearly.to_csv(file_name)




def count_words_each_patent(col_name, terms):
    """
    provide scaffold design parameter name and values
    identify if it is included in a patent
    save dataframe of counts
    """
    # retrieve patent list
    df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop_time' + '.csv')
    df = pd.read_csv(df_file)

    # begin new dataframe with counts
    df_patents = pd.DataFrame()
    df_patents['patent_num'] = list(df['patent_num'])
    df_patents['patent_year'] = list(df['patent_year'])
    df_patents['file_year'] = list(df['file_year'])

    # build the rest of the dataframe
    for term in terms:
        df_patents[term] = len(list(df_patents['patent_num'])) * [0]

    for i in range(len(list(df['patent_num']))):

        print(col_name + ' % complete = ' + str(round(100*i/len(list(df['patent_num'])),2)))

        # aggregate text in patent as a list of words
        all_words = ''
        all_words += clean_text(list(df['title'])[i])
        all_words += ' '
        all_words += clean_text(list(df['claims'])[i])
        all_words += ' '
        all_words += clean_text(list(df['description'])[i])
        word_list = all_words.split(' ')

        for term in terms:

            if term in all_words:
                df_patents.loc[i , term] = [1]

            """
            if count > 1:
                df_patents.loc[i , term] = [1]
                # print('term found: ' + term + ' ' + str(count))
            """

        file_name = os.path.join(retrieve_path('word_count_per_patent'), col_name + '.csv')
        df_patents.to_csv(file_name)
        #print('file_name saved: ' + file_name)


def clean_text(text):
    """
    provide text and return text
    remove characters for text analysis
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
    string = string.replace(';', ' ')
    string = string.replace('/', ' ')

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


def sort_untargetted():
    """
    """
    file_name = os.path.join(retrieve_path('word_count_all'))
    df = pd.read_csv(file_name)

    df_short = pd.DataFrame()

    for i in range(len(list(df['count']))):

        if int(list(df['count'])[i]) > 500:

            df_temp = pd.DataFrame()
            df_temp['word'] = [list(df['word'])[i]]
            df_temp['count'] = [int(list(df['count'])[i])]
            #print('term found = ')
            #print(df_temp)
            df_short = df_short.append(df_temp)
            print('df_short = ' + str(len(list(df_short['count']))))

    # df_short =  df[(df.count == 100)]
    df_short = df_short.sort_values(by=['count'], ascending=False)
    #df_short.sort_values(by=['count'], inplace=True, ascending=False)
    print('df_short = ' + str(len(list(df_short['count']))))
    file_name = os.path.join(retrieve_path('word_count_trim'))
    df_short.to_csv(file_name)



def untargetted_word_count():
    """
    list all the unique words and how common they are
    """
    df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop_time' + '.csv')
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

    for title in list(df['title']):
        string = clean_text(title)
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
        df.sort_values(by=['count'], ascending=False)
        file_name = os.path.join(retrieve_path('word_count_all'))
        df.to_csv(file_name)
