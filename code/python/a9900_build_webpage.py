import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from a0001_admin import clean_dataframe
from a0001_admin import name_paths
from a0001_admin import retreive_categories
from a0001_admin import retrieve_format
from a0001_admin import retrieve_list
from a0001_admin import retrieve_path


def build_webpage():
    """
    build index.html
    """

    print("running build_webpage")

    tasks = [0]

    if  0 in tasks: tasks = np.arange(1,101,1)
    if  1 in tasks: introduction_html()

    print("completed build_webpage")



def introduction_html():
    """

    """

    print("began introduction_html")

    index_html = os.path.join(retrieve_path('html_index'))
    f = open(index_html, "w")
    f.close()
    f = open(index_html, "w")
    f.close()

    f = open(index_html, "w")
    f.write('<!DOCTYPE html>' + '\n' )
    f.write('<html>' + '\n' )
    f.write('<title>SupportYears</title>' + '\n' )
    f.write('</head>' + '\n' )

    f.write('<style>' + '\n' )
    f.write('.container {' + '\n' )
    f.write('width: 100%;' + '\n' )
    f.write('height: 100%;' + '\n' )
    f.write('}' + '\n' )
    f.write('img {' + '\n' )
    f.write('width: 80%;' + '\n' )
    f.write('height: 80%;' + '\n' )
    f.write('object-fit: cover;' + '\n' )
    f.write('}' + '\n' )
    f.write('</style>' + '\n' )


    for name_article in retrieve_list('type_article'):

        # list compare term files
        compare_terms = os.path.join(retrieve_path('term_compare'))

        for category in retreive_categories():

            f.write('<div class="container">')
            f.write('<body>' + '\n')
            f.write('<center>' + '\n')

            f.write('<img alt="My Image" src="' + '')
            gif_dst = str(name_article + '_map_gif')
            gif_file = os.path.join(retrieve_path(gif_dst) , category + '.gif')
            print(gif_file)
            f.write(str(gif_file))
            f.write('" />')
            f.write('</div>' + '\n')
            f.write('</body>' + '\n')
            f.write('</center>' + '\n')

            plot_count_annual = str(name_article + '_compare_terms_plot')
            plot_dst = os.path.join(retrieve_path(plot_count_annual), category + '.png')
            f.write('<img alt="My Image" src="' + '')
            print(plot_dst)
            f.write(str(plot_dst))
            f.write('" />')
            f.write('</div>' + '\n')
            f.write('</body>' + '\n')
            f.write('</center>' + '\n')
            f.write('</div>')


    """
    for name_article in name_articles:

        name_src, name_dst, name_summary, name_unique, plot_unique = name_paths(name_article)

        png_files = os.path.join(retrieve_path(plot_unique))
        print('png_files = ' + str(png_files))
        for file in os.listdir(png_files):

            if '.png' not in str(file): continue

            f.write('<div class="container">')
            f.write('<body>' + '\n')
            f.write('<center>' + '\n')

            f.write('<img alt="My Image" src="' + '')
            plot_dst = os.path.join(png_files, file)
            print(plot_dst)
            f.write(str(plot_dst))
            f.write('" />')
            f.write('</div>' + '\n')
            f.write('</body>' + '\n')
            f.write('</center>' + '\n')


        annual_plot = str(name_article + '_annual_plot')
        png_files = os.path.join(retrieve_path(annual_plot), term + '.png')
        for file in os.listdir(png_files):

            if '.png' not in str(file): continue

            f.write('<div class="container">')
            f.write('<body>' + '\n')
            f.write('<center>' + '\n')

            f.write('<img alt="My Image" src="' + '')
            plot_dst = os.path.join(png_files, file)
            print(plot_dst)
            f.write(str(plot_dst))
            f.write('" />')
            f.write('</div>' + '\n')
            f.write('</body>' + '\n')
            f.write('</center>' + '\n')
    """

    f.write('</html>' + '\n' )
    f.close()


def write_table_count(file_path):
    """

    """

    print('file_path = ')
    print(file_path)

    file_split = file_path.split('/')
    file_name = file_split[-1]
    file_split = file_name.split('.')
    file_name = file_split[0]

    # retrieve trial counts
    df = pd.read_csv(file_path)
    del df['Unnamed: 0']

    print('df = ')
    print(df)

    df['counts'] = df['counts'].astype(int)

    term = list(df['terms'])
    count = list(df['counts'])


    chart_title = 'Trial counts for the metadata term: ' + file_name

    index_html = retrieve_path('index_html')
    f = open(index_html, "a")

    f.write('<body>' + '\n')
    f.write('<center>' + '\n')
    f.write('<h3>' + str(chart_title) + '</h3>' + '\n')
    f.write('<table>' + '\n')

    f.write('<tr>' + '\n')
    f.write('<th>' + file_name + '        ' + '</th>' + '\n')
    f.write('<th>' + ' Count ' + '</th>' + '\n')

    try:
        percents = list(df['percentages'])
        f.write('<th>' + ' Percents ' + '</th>' + '\n')
    except:
        print('no percentages found.')

    f.write('</tr>' + '\n')

    for i in range(len(term)):

        # print('i = ' + str(i))

        #if count[i] < 50: continue

        f.write('<tr>' + '\n')
        f.write('<th>' + str(term[i]) + '</th>' + '\n')
        f.write('<th>' + str(count[i]) + '</th>' + '\n')

        try:
            f.write('<th>' + str(round(float(percents[i]),2)) + '</th>' + '\n')
        except:
            print('no percentage found.')

        f.write('</tr>' + '\n')

    f.write('</table>' + '\n')
    f.write('</center>' + '\n')
    f.write('</body>' + '\n')
    f.close()


if __name__ == "__main__":
    main()
