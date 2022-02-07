import requests
import urllib.parse
import os
from os.path import exists
import pandas as pd
import time



def retrieve_gps(s, parameters):
    """

    """



    for i in range(len(parameters)):

        url = 'https://nominatim.openstreetmap.org/search/'
        url = url + urllib.parse.quote(s.location[i])
        url = url +'?format=json'

        print('searching for long/lat url = ')
        print(url)

        try:
            response = requests.get(url).json()

            print(response[0]["lat"])
            print(response[0]["lon"])

            lat = response[0]["lat"]
            lon = response[0]["lon"]

            break

        except:
            lat = None
            lon = None

        return(lat, lon)




def findLatLong(df):
    """
    Add two columns to a structured dataset for lat and long of an address
    """

    #df = pd.read_csv(sourceFile)
    #del df['Unnamed: 0']

    #df = df.dropna(subset=['Address'])
    addresses = list(df['readable_address'])

    lats, lons = [], []
    for address in addresses:

        print('print address = ')
        print(address)

        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        print('url = ')
        print(url)

        try:
            print('url = ')
            print(url)
            print('address = ')
            print(address)

            response = requests.get(url).json()
            # print('response = ')
            # print(response)

            print(response[0]["lat"])
            print(response[0]["lon"])

            lat = response[0]["lat"]
            lon = response[0]["lon"]

            print('lat/lon = ' + str(lat) + ' / ' + str(lon))

        except:
            lat = None
            lon = None

        lats.append(lat)
        lons.append(lon)
        #df.loc[len(df.index)] = [address, lat, lon]
        #print('df = ')
        #print(df)

    df['gpsLat'] = lats
    df['gpsLong'] = lons

    print('df = ')
    print(df)

    #df.to_csv(saveFile)
    #print('gps saved: ' + saveFile)

    print('completed findLongLat')

    return(df)
