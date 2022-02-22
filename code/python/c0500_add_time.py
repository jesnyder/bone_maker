import os
import pandas as pd
import pypatent
import re

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_datetime

from retrieve_long_lat import findLatLong

def add_time():
  """

  """
  print('beginning add_time')

  month_list = []
  month_list.append('January')
  month_list.append('February')
  month_list.append('March')
  month_list.append('April')
  month_list.append('May')
  month_list.append('June')
  month_list.append('July')
  month_list.append('August')
  month_list.append('September')
  month_list.append('October')
  month_list.append('November')
  month_list.append('December')

  # Find current time
  time = retrieve_datetime()
  time_split = time.split('-')
  year_now = int(time_split[0])
  month_now = int(time_split[1])
  month_now_num = int(month_now)
  print('time = ')
  print(time)
  print('year_now = ' + str(year_now))
  print('month_now = ' + str(month_now))

  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop' + '.csv')
  df = pd.read_csv(df_file)
  df = clean_dataframe(df)
  # del df['Unnamed: 0']
  # df = df.reset_index()

  dates = list(df['file_date'])

  months, years, month_index, months_lapsed = [], [], [], []
  for date in dates:

      date = date.replace(',', '')
      date_split = date.split(' ')
      months.append(date_split[0])
      month_index.append(1+month_list.index(months[-1]))
      years.append(date_split[-1])
      months_lapsed.append( (year_now - int(date_split[-1]))*12 + month_now - month_index[-1] )

  df['file_month'] = months
  df['file_month_index'] = month_index
  df['file_year'] = years
  df['file_months_lapsed'] = months_lapsed

  dates = list(df['patent_date'])

  months, years, month_index, months_lapsed = [], [], [], []
  for date in dates:

      date = date.replace(',', '')
      date_split = date.split(' ')
      months.append(date_split[0])

      if date_split[0] =='*': month_index.append(1)
      else: month_index.append(1+month_list.index(date_split[0]))

      years.append(date_split[-1])
      months_lapsed.append( (year_now - int(date_split[-1]))*12 + month_now - month_index[-1] )

  df['patent_month'] = months
  df['patent_month_index'] = month_index
  df['patent_year'] = years
  df['patent_months_lapsed'] = months_lapsed

  #del df['claims']
  #del df['description']

  df.sort_values(by=['patent_num'], inplace=True)
  df = edit_city(df)
  df = edit_state(df)
  df = edit_country(df)
  df = edit_assignee_name(df)
  df = add_readable_address(df)

  df = findLatLong(df)

  print(df)

  # df.sort_values(by=['patent_num'], inplace=True)

  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop_time' + '.csv')
  df.to_csv(df_file)


  df_map = pd.DataFrame()
  df_map['gpsLat'] = list(df['gpsLat'])
  df_map['gpsLong'] = list(df['gpsLong'])
  df_map['file_year'] = list(df['file_year'])
  df_map['patent_year'] = list(df['patent_year'])
  file_name = os.path.join(retrieve_path('df_map'))
  df_map.to_csv(file_name)

  print('completed add_time')


def add_readable_address(df):
    """
    Add a readable address
    """

    readable_address = []

    for i in range(len(df['url'])):


        try:
            assignee = str(df.loc[i]['assignee_name_editted'])
            assignee_list = assignee.split(',')
            assignee_lead = assignee_list[0]
            address = str(assignee_lead + ', ')

        except:
            address = ''

        if 'None' not in str(df.loc[i]['city_editted']):
            address = str(address + str(df.loc[i]['city_editted']) + ' , ')

        if '/' not in str(df.loc[i]['state_editted']):
            address = str(address  + str(df.loc[i]['state_editted']))

        address = str(address + ' , ' + str(df.loc[i]['country_editted']))

        readable_address.append(address)

    df['readable_address'] = readable_address

    return(df)



def edit_city(df):

    df['city_editted'] = len(list(df['url'])) * [None]

    for i in range(len(list(df['applicant_city']))):

        city = df.loc[i]['applicant_city']
        city = str(city)

        for i in range(len(city)):

            print('city  = ')
            print(city)

            if city[i] >='A' and city[i] <= 'Z':

                if i > 0:

                    if city[i-1] != ' ':

                        city = city[:i] + ' , ' + city[i:]

        try:
            city = city.split(',')
            df.loc[i]['city_editted'] = city[0]

        except:
            df.loc[i]['city_editted'] = city

        print('city = ')
        print(city)


    print('df = ')
    print(df)

    return(df)



def edit_assignee_name(df):

    assignee_name_editted = []

    for name in list(df['assignee_name']):

        name = str(name)
        # print('assignee_name = ' + name )
        #if '"' in name:
        name = name.strip(' " "" ')
        name = name.replace('"', '')
        name = name.replace('\"', '')
        name = name.replace('The', '')
        # print('assignee_name_editted = ' + name )

        assignee_name_editted.append(name)

    df['assignee_name_editted'] = assignee_name_editted

    return(df)



def edit_state(df):


    state_editted = []
    for state in list(df['applicant_state']):

        #print('country = ' + country)
        try:
            if len(state) > 2:
                state = state[0:2]
                # print('truncated country = ' + country)
            state_editted.append(state)

        except:
            state = 'US'
            state_editted.append('US')


        # print('len(country_editted) = ' + str(len(country_editted)))

    df['state_editted'] = state_editted

    return(df)



def edit_country(df):

    country_editted = []
    for country in list(df['applicant_country']):

        #print('country = ' + country)
        try:
            if len(country) > 2:
                country = country[0:2]
                # print('truncated country = ' + country)
            country_editted.append(country)

        except:
            country = 'US'
            country_editted.append('US')


        # print('len(country_editted) = ' + str(len(country_editted)))

    df['country_editted'] = country_editted

    return(df)


def clean_dataframe(df):

    col_names = df.columns

    for name in col_names:

        if 'Unnamed' in name:
            del df[name]

    try:
        df = df.drop_duplicates(subset = 'patent_num')
        df = df.sort_values('patent_num', ascending=True)
    except:
        print('cleaning dataframe without patent_num.')

    df = df.reset_index()

    return(df)
