import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

from a0001_retrieve_meta import retrieve_path
from a0001_retrieve_meta import clean_dataframe
from a0001_retrieve_meta import retrieve_term_list

def bar_chart_percentage(name_article, terms_to_compare):
    """
    retrieve dataframe
    plot barchart
    """
    # collect list of terms for comparison
    file_name = os.path.join(retrieve_path('compare_terms'),terms_to_compare)
    df = pd.read_csv(file_name)
    term_list = list(df.iloc[:,0])
    print('term_list = ' + str(term_list))
    return(term_list)

    term_count_annual = str('count_term_annual_' + name_article)
    file_name = os.path.join(retrieve_path(term_count_annual), 'term_annual_count' + '.csv')
    print('name_article = ' + str(name_article))
    print('term_count_annual = ' + str(term_count_annual))
    print('file_name = ' + str(file_name))
    df = pd.read_csv(file_name)
    print('df = ')
    print(df)


    # begin figure
    plt.close('all')
    figure, axes = plt.subplots()
    plt.figure(figsize=(16, 6))
    plt.subplot(111)

    xx = list(df['years'])
    for i in range(len(term_list)):

        for col in df.columns:

            if col != str(term_list[i] + '_percentage'):
                continue

            yy = list(df[term_list[i] + '_percentage'])

            offsets = [0] * len(list(xx))

            if i > 0:
                offsets = []
                for k in range(len(list(df['years']))):
                    offset = 0
                    for j in range(i):
                        #term = term_list[j]
                        offset = offset + df.loc[k][term_list[j] + '_percentage']
                    offsets.append(offset)

            assert len(offsets) == len(xx)
            assert len(offsets) == len(yy)

            plt.bar(xx, yy, width=1.0, bottom=offsets, align='center', label = term_list[i])


    plt.xlabel('Years')
    plt.ylabel('Percentage of ' + name_article)
    plt.title(name_article)
    plt.legend(bbox_to_anchor=(1, 0.9), loc ="upper left")

    plot_count_annual = str('plot_term_annual_' + name_article)
    plot_dst = os.path.join(retrieve_path(plot_count_annual), terms_to_compare +  ' bar_term_annual' + '.png')
    plt.savefig(plot_dst, dpi = 600, edgecolor = 'w')
    print('saved plot: ' + plot_dst)
    plt.close('all')
