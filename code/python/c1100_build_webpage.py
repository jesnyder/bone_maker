import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests

from c0001_retrieve_meta import retrieve_path




def build_webpage():
    """
    Objective: Summarize the projects and findings

    Tasks:
        1. Write summary of html

    """

    print("running build_webpage")

    tasks = [1]

    if 1 in tasks: introduction_html()


    print("completed build_webpage")



def introduction_html():
    """

    """

    h0_str = 'Survey of Scaffold Parameters for Bone Tissue Engineering'
    h0_txt = 'Motivation: Make an ingishtful decision based on an survey of a public database. To minimize bias, lets audit the US Patent database to find freqeuncy of key design parameters. '

    h1_str = 'Introduction'
    h1_txt = 'We begin by outlining some of the quantifiable and critical design parameters of a scaffold. (1) Material and (2) Pore Size. '


    index_html = retrieve_path('index_html')
    f = open(index_html, "w")
    f.close()
    f = open(index_html, "w")
    f.close()

    f = open(index_html, "w")
    f.write('<!DOCTYPE html>' + '\n' )
    f.write('<html>' + '\n' )
    f.write('<title>PatentSurvey</title>' + '\n' )
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



    # plot of the number of patents per year
    f.write('<body>' + '\n')
    f.write('<center>' + '\n')
    f.write('<div class="container">')

    f.write('<h1>' + str(h0_str) + '</h1>' + '\n')
    f.write('<p>' + str(h0_txt) + '</p>' + '\n')
    f.write('</body>' + '\n')

    f.write('<h2>' + str('Objective & Tasks') + '</h2>' + '\n')
    f.write('<p>' + str('The objective is to query, scrape, and analyze the US Patent and Trademark Office for bone tissue engineering related articles and then examine that resource for trends.' ))
    f.write(str('The tasks to complete are: ') + '\n')
    f.write('\n' + str('(1) Build: Query the US Patent and Trademark database for bone tissue engineering terms, such as craniofacial, biomanufacturing, tissue engineering, biofabrication, osseointegration, mandible, and osteoconductive. '))
    f.write('\n' + str('(2) Clean: Aggregate unique patents specific to area of interest. Patents must have 3 of the following terms (in addition to one of the search terms) to be included in further analysis. Terms include:  regenerative medicine, tissue engineering, bone, scaffold, orthodontic, biocompatible, biodegradable, and tissue scaffold.'))
    f.write('\n' + str('(3) Define: Define the size of the database. Plot the number of patents per year (annual and cumulative).'))
    f.write('\n' + str('(4) Geolocation: Define the geographic footprint of the database. Map the assignee address of the patents per year.'))
    f.write('\n' + str('(5) Historical Material Usage: Plot the occurrances of specific materials in the patent database (annual and cumulative).'))
    f.write('\n' + str('(6) Text Analysis: Count the frequency of words to identify the most prominent materials, products, pore shapes, sizes, and use cases by text analysis.'))
    f.write('\n' + str('*** not yet completed ***'))
    f.write('\n' + str('(7) Cross-reference Google Scholar for cited-by metric to identify most impactful work.'))
    f.write('\n' + str('(8) Plot occurances of the terms found in '))
    f.write('\n' + str(''))
    f.write('</p>' + '\n')
    f.write('</body>' + '\n')

    f.write('<h2>' + str('The History of Bone Tissue Engineering in the Patent Archive') + '</h2>' + '\n')

    df = pd.read_csv(os.path.join(retrieve_path('df_patents_per_year')))
    year_min = min(list(df['year']))
    year_max = max(list(df['year']))
    year_span = year_max - year_min
    total_filed = max(list(df['file_cdf_counts']))
    total_patents = max(list(df['patent_cdf_counts']))

    f.write('<p>' + str('The plot represents ' + str(total_patents)))
    f.write(str(' patents filed'))
    f.write(str(' (' + str(total_filed) + ' documents filed) '))
    f.write('with the US Patent and Trademark Office over a ' + str(year_span) + ' year span, from ')
    f.write(str(str(year_min) + '-' + str(year_max) + '.') + '</p>' + '\n')

    f.write('<img alt="My Image" src="' + '../')
    f.write(str(retrieve_path('all_patents_vs_year')))
    f.write('" />')

    f.write('<img alt="My Image" src="' + '../')
    f.write(str(retrieve_path('material_count_yearly')))
    f.write('" />')

    f.write('</div>')
    f.write('</center>' + '\n')
    f.write('</body>' + '\n')

    # map of patents
    f.write('<body>' + '\n')
    f.write('<center>' + '\n')
    f.write('<div class="container">')
    f.write('<h2>' + str('Map of Bone Tissue Engineering in the Patent Archive') + '</h2>' + '\n')

    # Insert map gif
    f.write('<img alt="My Image" src="' + '../')
    f.write(str(retrieve_path('map_gif')))
    f.write('" />')

    # Insert static image of the current map
    f.write('<img alt="My Image" src="' + '../')
    f.write(str(retrieve_path('map_patent')))
    f.write('" />')
    f.write('</div>')
    f.write('</center>' + '\n')
    f.write('</body>' + '\n')

    # For all metadat, make a chart
    file_list = os.listdir(retrieve_path('count_patent'))
    for file in file_list:
        file_path = os.path.join(retrieve_path('count_patent'), file)

        if 'applicant_num' in file: continue
        if 'applicant_num' in file: continue
        if 'applicant_state' in file: continue
        if 'assignee_name_editted' in file: continue
        if 'city_editted' in file: continue
        if 'description' in file: continue
        if 'family_id' in file: continue
        if 'file_date' in file: continue
        if 'file_months_lapsed' in file: continue
        if 'file_month_index' in file: continue
        if 'gpsLat' in file: continue
        if 'gpsLong' in file: continue
        if 'level_0' in file: continue
        if 'patent_date' in file: continue
        if 'patent_months_lapsed' in file: continue
        if 'patent_month_index' in file: continue
        if 'patent_num' in file: continue
        if 'readable_address' in file: continue
        if 'scores' in file: continue
        if 'title' in file: continue
        if 'url' in file: continue

        try:
            write_table_count(file_path)
        except:
            print('table skipped')

    """
    f.write('<body>' + '\n')
    f.write('<h1>' + str(h1_str) + '</h1>' + '\n')
    f.write('<p>' + str(h1_txt) + '</p>' + '\n')
    f.write('</body>' + '\n')
    f.close()
    """


    # Close the html file
    f = open(index_html, "a")
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

    df['count'] = df['count'].astype(int)

    term = list(df[file_name])
    count = list(df['count'])

    chart_title = 'Trial counts for the metadata term:' + file_name

    index_html = retrieve_path('index_html')
    f = open(index_html, "a")
    f.write('<body>' + '\n')
    f.write('<center>' + '\n')
    f.write('<h3>' + str(chart_title) + '</h3>' + '\n')
    f.write('<table>' + '\n')

    f.write('<tr>' + '\n')
    f.write('<th>' + file_name + '        ' + '</th>' + '\n')
    f.write('<th>' + 'Number of Patents' + '</th>' + '\n')
    f.write('</tr>' + '\n')

    for i in range(len(term)):

        if count[i] < 50: continue

        f.write('<tr>' + '\n')
        f.write('<th>' + str(term[i]) + '</th>' + '\n')
        f.write('<th>' + str(count[i]) + '</th>' + '\n')
        f.write('</tr>' + '\n')

    f.write('</table>' + '\n')
    f.write('</center>' + '\n')
    f.write('</body>' + '\n')




if __name__ == "__main__":
    main()
