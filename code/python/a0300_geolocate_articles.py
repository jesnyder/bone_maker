from bs4 import BeautifulSoup
import datetime
import json
import lxml
import matplotlib.pyplot as plt
import numpy as np
import os
from os.path import exists
import pandas as pd
from serpapi import GoogleSearch
import re
import requests
import time
import urllib.parse

from a0001_admin import clean_dataframe
from a0001_admin import name_paths
from a0001_admin import retreive_categories
from a0001_admin import retrieve_format
from a0001_admin import retrieve_list
from a0001_admin import retrieve_path
from a0001_admin import write_paths
from a0200_aggregate_info  import list_unique_values
from a0200_aggregate_info  import plot_unique_values
from a0200_aggregate_info  import cross_plot_unique
from find_color import find_color
from gif_maker import build_gif


def geolocate_articles():
    """

    """
    print('began geolocate_articles')

    # List task numbers to complete
    tasks = [0]
    write_paths()
    if  0 in tasks: tasks = np.arange(1, 101, 1)
    if  1 in tasks: find_address()
    #if  2 in tasks: list_address()

    print('completed geolocate_articles')

"""
def list_address():

    #consolidate all addresses to reference later

    df = pd.DataFrame()

    #for name_article in retrieve_list('type_article'):
    for name_article in ['patents', 'clinical_trials', 'nih_awards', 'nsf_awards']:

        print('name_article = ' + name_article)

        f = os.path.join(retrieve_path(name_article + '_aggregate_df'),  name_article + '_with_address' + '.csv' )
        df_ref = pd.read_csv(f)
        df_ref = clean_dataframe(df)

        df_temp = pd.DataFrame()
        df_temp['ref_complete_address'] = list(df_ref['ref_complete_address'])
        df_temp[i, 'ref_address'] = list(df_ref['ref_address'])
        df_temp[i, 'ref_lat'] = list(df_ref['lat'])
        df_temp[i, 'ref_lon'] = list(df_ref['lon'])
        df.append(df_temp)

    df = df.clean_dataframe(df)
    df.to_csv(retrieve_path(all_institutions))

    unique_ref_address, counts = [], []
    for i in range(len(list(df_ref['ref_address']))):
        i = i-1
        address = df_ref.loc[i,'ref_address']
        if address not in unique_ref_address:
            unique_ref_address.append(address)
            count =  list(df_ref['ref_address']).count(address)
            counts = counts.append(count)

    df = pd.DataFrame()
    df['ref_address'] = unique_ref_address
    df['counts'] = counts
    df = df.clean_dataframe(df)
    df.to_csv(retrieve_path(count_institutions))
"""

# completed programs

def build_clinical_address(df):
    """
    find address and lat/lon for each trial
    """
    #print('df = ')
    #print(df)

    locations = df['Locations']
    sponsors = df['Sponsor/Collaborators']

    address = ''
    address = address + str(sponsors) + ' ; '
    address = address + str(locations)
    address_complete = address
    print('address_complete =   ')
    print(address_complete)

    sponsor_location = []
    try:
        locations_split = locations.split(',')
        for item in locations_split:
            sponsor_location.append(item)
    except:
        hello = 'hello'
    try:
        sponsors_split = sponsors.split('|')
        for item in sponsors_split:
            sponsor_location.append(item)
    except:
        hello = 'hello'


    # hard code address changes
    if 'Hadassah Medical Organization' in sponsor_location:
        target = 'Jerusalem, Israel'
        sponsor_location.append(target)
    elif 'CAR-T (Shanghai) Biotechnology Co., Ltd.' in sponsor_location:
        target = 'Shanghai, China'
        sponsor_location.append(target)
    elif 'Peking University People\'s Hospital' in sponsor_location:
        target = 'Beijing, China'
        sponsor_location.append(target)
    elif 'The First People\'s Hospital of Yunnan' in sponsor_location:
        target = 'Yunnan, China'
        sponsor_location.append(target)
    elif 'Institute of Hematology & Blood Diseases Hospital' in sponsor_location:
        target = 'San Francisco, CA'
        sponsor_location.append(target)
    elif 'Direct Biologics, LLC' in sponsor_location:
        target = 'Austin, TX'
        sponsor_location.append(target)
    elif 'Sclnow Biotechnology Co., Ltd.' in sponsor_location:
        target = '231 S Whisman Rd, Mountain View, CA'
        sponsor_location.append(target)
    elif 'Shandong Qilu Stem Cells Engineering Co., Ltd.' in sponsor_location:
        target = 'South San Francisco, CA'
        sponsor_location.append(target)
    elif 'Vinmec Research Institute of Stem Cell and Gene Technology' in sponsor_location:
        target = 'Times City, Vietnam'
        sponsor_location.append(target)
    elif 'Affiliated Hospital of Jiangsu University' in sponsor_location:
        target = 'Zhenjiang, Jiangsu, China'
        sponsor_location.append(target)
    elif 'Masonic Cancer Center, University of Minnesota' in sponsor_location:
        target = 'University of Minnesota'
        sponsor_location.append(target)
    elif 'Pharmicell Co., Ltd.' in sponsor_location:
        target = 'San Francisco, CA'
        sponsor_location.append(target)
    elif 'Mesoblast, Inc.' in sponsor_location:
        target = '505 5th Ave, New York, NY 10017'
        sponsor_location.append(target)
    elif 'Institute of Biophysics and Cell Engineering of National Academy of Sciences of Belarus' in sponsor_location:
        target = 'Minsk, Belarus'
        sponsor_location.append(target)
    elif 'Ministry of Public Health, Republic of Belarus' in sponsor_location:
        target = 'Minsk, Belarus'
        sponsor_location.append(target)
    elif 'Celltex Therapeutics Corporation' in sponsor_location:
        target = 'Houston, TX 77057'
        sponsor_location.append(target)
    elif 'Celltex Therapeutics Corporation' in sponsor_location:
        target = 'Houston, TX 77057'
        sponsor_location.append(target)
    elif 'PT. Prodia Stem Cell Indonesia' in sponsor_location:
        target = 'Daerah Khusus Ibukota Jakarta, Indonesia'
        sponsor_location.append(target)
    elif 'South China Research Center for Stem Cell and Regenerative Medicine' in sponsor_location:
        target = 'Guangzhou, China'
        sponsor_location.append(target)
    elif 'Regeneris Medical' in sponsor_location:
        target = 'North Attleboro, MA 02760'
        sponsor_location.append(target)
    elif 'Ontario Institute for Regenerative Medicine (OIRM)' in sponsor_location:
        target = '661 University Avenue, Toronto, Ontario, CANADA'
        sponsor_location.append(target)
    elif 'The First Affiliated Hospital of Dalian Medical University' in sponsor_location:
        target = '222 Zhongshan Rd, Xigang District, Dalian, China'
        sponsor_location.append(target)
    elif 'Sorrento Therapeutics, Inc.' in sponsor_location:
        target = '4955 Directors Place, San Diego, CA 92121'
        sponsor_location.append(target)
    elif 'Department of Neurology, University Hospital Motol, Prague, Czech Republic' in sponsor_location:
        target = 'Prague, Czech Republic'
        sponsor_location.append(target)
    elif 'Xinhua Hospital, Shanghai Jiao Tong University School of Medicine' in sponsor_location:
        target = '1555 Kongjiang Rd, Yangpu District, Shanghai, China'
        sponsor_location.append(target)
    elif 'Nature Cell Co. Ltd.' in sponsor_location:
        target = 'Seoul, South Korea '
        sponsor_location.append(target)
    elif 'PLA General Hospital, Beijing' in sponsor_location:
        target = 'Beijing'
        sponsor_location.append(target)
    elif 'Papworth Hospital NHS Foundation Trust' in sponsor_location:
        target = 'Cambridge, United Kingdom'
        sponsor_location.append(target)
    elif 'Cell Therapy Catapult' in sponsor_location:
        target = 'London, United Kingdom'
        sponsor_location.append(target)
    elif 'Royal Free Hospital NHS Foundation Trust' in sponsor_location:
        target = 'London, United Kingdom'
        sponsor_location.append(target)
    elif 'Stem Cells Arabia' in sponsor_location:
        target = 'Ibn Khaldoun St. 40, Amman 11183, Jordan'
        sponsor_location.append(target)
    elif 'Mesoblast, Ltd.' in sponsor_location:
        target = '505 5th Ave, New York, NY 10017'
        sponsor_location.append(target)
    elif 'Fuzhou General Hospital' in sponsor_location:
        target = 'Gulou District, Fuzhou, Fuzhou, China'
        sponsor_location.append(target)
    elif 'The Oxford Dental College, Hospital and Research Center, Bangalore, India' in sponsor_location:
        target = 'Bangalore, India'
        sponsor_location.append(target)
    elif 'The Oxford Dental College, Hospital and Research Center, Bangalore, India' in sponsor_location:
        target = 'Bangalore, India'
        sponsor_location.append(target)
    elif 'Aegle Therapeutics' in sponsor_location:
        target = '400 TradeCenter, Woburn, MA 01801'
        sponsor_location.append(target)
    elif 'Anterogen Co., Ltd.' in sponsor_location:
        target = 'Seoul, South Korea'
        sponsor_location.append(target)
    elif 'Department of Spine Surgery, University Hospital Motol, Prague, Czech Republilc' in sponsor_location:
        target = 'Prague, Czech Republic'
        sponsor_location.append(target)
    elif 'Longeveron Inc.' in sponsor_location:
        target = 'MIAMI, FL 33136'
        sponsor_location.append(target)
    elif 'Medipost Co Ltd.' in sponsor_location:
        target = 'Seoul, South Korea'
        sponsor_location.append(target)
    elif 'Chinese PLA General Hospital' in sponsor_location:
        target = '4th Ring Road, Beijing, China'
        sponsor_location.append(target)
    elif 'Baylx Inc.' in sponsor_location:
        target = 'Irvine, CA 92618'
        sponsor_location.append(target)
    elif 'BioRestorative Therapies' in sponsor_location:
        target = 'Melville, NY 11747'
        sponsor_location.append(target)
    elif 'Celyad Oncology SA' in sponsor_location:
        target = 'New York, NY 10004'
        sponsor_location.append(target)
    elif 'Vitro Biopharma Inc.' in sponsor_location:
        target = 'Golden, CO 80403'
        sponsor_location.append(target)
    elif 'Shenzhen Geno-Immune Medical Institute' in sponsor_location:
        target = 'Shenzhen'
        sponsor_location.append(target)
    elif 'Bright Cell, Inc.' in sponsor_location:
        target = 'Prince George, BC, Canada'
        sponsor_location.append(target)
    elif 'Paean Biotechnology Inc.' in sponsor_location:
        target = 'Seoul, Korea'
        sponsor_location.append(target)
    elif 'National Cancer Institute (NCI)' in sponsor_location:
        target = 'Washington, DC'
        sponsor_location.append(target)
    elif 'Global Stem Cell Center, Baghdad' in sponsor_location:
        target = 'Baghdad'
        sponsor_location.append(target)
    elif 'Rejuva Medical Aesthetics' in sponsor_location:
        target = 'Los Angeles, CA 90025'
        sponsor_location.append(target)
    elif 'Institute of Anatomy TU Dresden' in sponsor_location:
        target = 'Dresden, Germany'
        sponsor_location.append(target)
    elif 'University of Sao Paulo General Hospital' in sponsor_location:
        target = 'Sao Paulo'
        sponsor_location.append(target)
    elif 'The Nordic Network For Clinical Islet Transplantation' in sponsor_location:
        target = 'Torbjörn'
        sponsor_location.append(target)
    elif 'Taiwan Mitochondrion Applied Technology Co., Ltd.' in sponsor_location:
        target = 'Taiwan'
        sponsor_location.append(target)


    print('sponsor_location = ')
    print(sponsor_location)

    addresses = []
    address = sponsor_location[0]
    addresses.append(address)

    for i in range(len(sponsor_location)):
        address = sponsor_location[i]
        addresses.append(address)

    if len(sponsor_location) > 1:
        address = sponsor_location[1]
        addresses.append(address)

    if len(sponsor_location) > 2:
        address = sponsor_location[1] + ', '
        address = sponsor_location[2]
        addresses.append(address)

        address = sponsor_location[2]
        addresses.append(address)

    if len(sponsor_location) > 3:
        address = sponsor_location[1] + ', '
        address = sponsor_location[2] + ', '
        address = sponsor_location[3]
        addresses.append(address)

        address = sponsor_location[-2] + ', '
        address = sponsor_location[-1]
        addresses.append(address)

        address = sponsor_location[3]
        addresses.append(address)

    for address in addresses:
        print('address_complete =   ')
        print(address_complete)
        print('address =   ')
        print(address)
        lat, lon = findLatLong(address)
        if lat != None: return(address_complete, address, lat, lon)


def build_nih_address(df):
    """
    identify organization name and lat/lon
    """
    address = df['Organization Name']
    lat = df['Latitude']
    lon = df['Longitude']

    """
    print('address = ' + str(address))
    print('lat = ' + str(lat))
    print('lon = ' + str(lon))
    """

    return(address, address, lat, lon)


def build_nsf_address(df):
    """
    build the address and retrieve lat and lon
    for each entry of the grant
    """
    address = ''
    assignee_name = df['Organization']
    street = df['OrganizationStreet']
    city = df['OrganizationCity']
    state = df['OrganizationState']
    country = 'US'

    address = ''
    address = address + str(assignee_name) + ' |  '
    address = address + str(street) + ', '
    address = address + str(city) + ', '
    address = address + str(state) + ', '
    address = address + str(country)
    address_complete = address
    print('address_complete =   ')
    print(address_complete)

    # format elements for OpenStreets search
    try:
        if '(' in city: city = city.replace('(','')
        if ')' in city: city = city.replace(')','')
    except:
        hello = 'hello'

    try:
        addresses = []

        address = assignee_name
        addresses.append(address)

        address = str(street) + ', '
        address = address + str(city) + ', '
        address = address + str(state) + ', '
        address = address + str(country)
        addresses.append(address)

        address = str(city) + ', '
        address = address + str(state) + ', '
        address = address + str(country)
        addresses.append(address)

        address = str(city) + ', '
        address = address + str(state)
        addresses.append(address)

        address = str(city) + ', '
        address = address + str(country)
        addresses.append(address)

        address = str(city)
        addresses.append(address)

        address = str(country)
        addresses.append(address)

        for address in addresses:
            print('address_complete =   ')
            print(address_complete)
            print('address =   ')
            print(address)
            lat, lon = findLatLong(address)
            if lat != None: return(address_complete, address, lat, lon)

        lat = 0
        lon = 0
        return(address_complete, address, lat, lon)

    except:
        lat = 0
        lon = 0
        return(address_complete, address, lat, lon)


def build_gscholar(df):
    """

    """
    df = clean_dataframe(df)

    address_complete, address, lat, lon = None, None, None, None
    return(address_complete, address, lat, lon)


def build_patent_address(df):
    """
    build address and look up lat/lon
    """
    #print('df = ')
    #print(df)

    # identify fields
    assignee_name = df['assignee_name']
    assignee_loc = df['assignee_loc']
    name = df['applicant_name']
    city = df['applicant_city']
    state = df['applicant_state']
    country = df['applicant_country']

    # format retrieved info
    try:
        if '(' in city: city = city.replace('(','')
        if ')' in city: city = city.replace(')','')
    except:
        hello = 'hello'
    try:
        if ',' in assignee_name: assignee_name = assignee_name.split(',')[0]
        if '.' in assignee_name: assignee_name = assignee_name.split('.')[0]
    except:
        hello = 'hello'

    # write all address info into a string
    address = ''
    address = address + str(assignee_name) + ', '
    address = address + str(assignee_loc) + ' | '
    address = address + str(name) + ', '
    address = address + str(city) + ', '
    address = address + str(state) + ', '
    address = address + str(country)
    address_complete = address
    print('address_complete =   ')
    print(address_complete)

    # create a list of possible addresses
    addresses = []

    address = str(assignee_name)
    addresses.append(address)

    address = str(assignee_loc)
    addresses.append(address)

    address = str(name)
    addresses.append(address)

    address = str(name) + ', '
    address = address + str(city) + ', '
    address = address + str(state) + ', '
    address = address + str(country)
    addresses.append(address)

    address = str(city) + ', '
    address = address + str(state) + ', '
    address = address + str(country)
    addresses.append(address)

    address = str(city) + ', '
    address = address + str(country)
    addresses.append(address)

    try:
        city_split = city.split(',')
        address = str(city_split[0]) + ', '
        address = address + str(country)
        addresses.append(address)

        address = str(city_split[1]) + ', '
        address = address + str(country)
        addresses.append(address)

        address = str(city)
        addresses.append(address)

        address = str(city_split[0])
        addresses.append(address)

        address = str(city_split[1])
        addresses.append(address)
    except:
        hello = 'hello'

    address = str(country)
    addresses.append(address)

    for address in addresses:
        print('address_complete =   ')
        print(address_complete)
        print('address =   ')
        print(address)
        lat, lon = findLatLong(address)
        if lat != None: return(address_complete, address, lat, lon)


    try:
        names = []
        states = []
        countries = []
        for i in range(len(state)-1):
            if i%2 == 0: continue
            state_i = str(state)[i-1:i+1]
            country_i = str(country)[i-1:i+1]
            states.append(state_i)
            countries.append(country_i)

        address = ''
        address = address + str(states[0]) + ', '
        address = address + str(countries[0])
        print('address = ' + str(address))
        lat, lon = findLatLong(address)
        if lat != None: return(address_complete, address, lat, lon)
    except:
        hello = 'hello'


    try:
        names = []
        countries = []
        for i in range(len(country)-1):
            if i%2 == 0: continue
            country_i = str(country)[i-1:i+1]
            countries.append(country_i)

        address = ''
        address = address + str(countries[0])
        print('address = ' + str(address))
        lat, lon = findLatLong(address)
        if lat != None: return(address_complete, address, lat, lon)
    except:
        hello = 'hello'


def find_address():
    """
    for all found aticles
    list unique institutions
    """

    #for name_article in ['clinical_trials', 'nih_awards', 'nsf_awards', 'patents']:
    for name_article in retrieve_list('type_article'):

        print('name_article = ' + name_article)

        if name_article != 'nih_awards': continue

        f = os.path.join(retrieve_path(name_article + '_aggregate_df'),  name_article + '.csv' )
        df_ref = clean_dataframe(pd.read_csv(f))

        df_ref['ref_complete_address'] = [None] * len(list(df_ref.iloc[:,0]))
        df_ref['ref_address'] = [None] * len(list(df_ref.iloc[:,0]))
        df_ref['ref_lat'] = [None] * len(list(df_ref.iloc[:,0]))
        df_ref['ref_lon'] = [None] * len(list(df_ref.iloc[:,0]))

        for i in range(len(list(df_ref.iloc[:,0]))):

            i= i-1

            complete_num = round(100*i/len(list(df_ref.iloc[:,0])),2)
            print(name_article + ' % complete: ' + str(complete_num) + '    i = ' + str(i))
            df_ref_row = df_ref.iloc[i,:]

            if 'nih_awards' in name_article:
                address_complete, address, lat, lon = build_nih_address(df_ref_row)

            if 'nsf_award' in name_article:
                address_complete, address, lat, lon = build_nsf_address(df_ref_row)

            if 'clinical' in name_article:
                address_complete, address, lat, lon = build_clinical_address(df_ref_row)

            if 'patent' in name_article:
                address_complete, address, lat, lon = build_patent_address(df_ref_row)

            if 'gscholar' in name_article:
                address_complete, address, lat, lon = build_gscholar_address(df_ref_row)


            df_ref.loc[i, 'ref_complete_address'] = address_complete
            df_ref.loc[i, 'ref_address'] = address
            df_ref.loc[i, 'ref_lat'] = lat
            df_ref.loc[i, 'ref_lon'] = lon

        f = os.path.join(retrieve_path(name_article + '_aggregate_df'),  name_article + '_with_address' + '.csv' )
        df_ref = clean_dataframe(df_ref)
        df_ref.to_csv(f)

        list_unique_values(name_article, df_ref)
        plot_unique_values(name_article)
        cross_plot_unique(name_article, df_ref)


def findLatLong(address):
    """

    """

    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    #print('url = ')
    #print(url)
    response = requests.get(url).json()
    print(response)

    #print('searching for long/lat url = ')
    #print(url)

    try:
        #print(response[0]["lat"])
        #print(response[0]["lon"])
        lat = response[0]["lat"]
        lon = response[0]["lon"]

    except:
        lat = None
        lon = None

    print('lat/lon = ' + str(lat) + ' / ' + str(lon))

    return(lat, lon)



if __name__ == "__main__":
    main()
