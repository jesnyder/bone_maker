import json

import logging
# import coloredlogs

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import requests

from c0001_retrieve_meta import retrieve_path


def build_dataframe():
    """
    Objective: Build dataframe - row each trial, column key descriptors

    Tasks:
        1. Define keys
        2. Retieve keys from json
        3. Build and save dataframe

    """

    print("running create_webpage")

    tasks = [1]

    if 1 in tasks: write_keys()
    # if 2 in tasks: read_json()

    print("completed create_webpage")


def write_keys():
    """
    Read json
    Extract keys
    Save keys to file
    """

    # read json

    # retrieve query terms
    df = pd.read_csv(retrieve_path('search_terms_nih_clinical_trials'))
    query_terms = list(df['search_terms'])

    # specify file_type
    file_type = 'json'

    for term in query_terms:

        # identify the folder
        trials_path = retrieve_path('trials_path')
        trials_path = os.path.join(trials_path, term)
        trials_list = os.listdir(trials_path)
        trial = trials_list[2]
        trials_json = os.path.join(trials_path, trial )
        # print('trials_path = ' + trials_json)

        # open JSON file
        f = open(trials_json)

        # return JSON object as dictionary
        data = json.load(f)

        key1st = []
        for key in data.keys():
            try: data.keys()
            except KeyError: continue
            key1st.append(key)
            print('Key Found: key1st = ' + key)

        key2nd = []
        for key1 in key1st:
            for key in data[key1].keys():
                try: data[key1].keys()
                except KeyError: continue
                key2nd.append(key)
                print('Key Found: key3rd = ' + key1 + ' ' + key)

        key3rd = ['Study']
        key3 = 'Study'

        key4th = []
        for key2 in key2nd:
            for key1 in key1st:
                for key in data[key1]['FullStudies'][0][key3].keys():
                    try: data[key1]['FullStudies'][0][key3].keys()
                    except KeyError: continue
                    key4th.append(key)
                    print('Key Found: key4th = ' + key1 + ' ' + key2 + ' ' + key )

        key5th = []
        for key4 in key4th:
            for key2 in key2nd:
                for key1 in key1st:
                    for key in data[key1]['FullStudies'][0][key3][key4].keys():

                        try: keys = data[key1]['FullStudies'][0][key3][key4].keys()
                        except KeyError: continue

                        print('Key5th  = ')
                        print(keys)
                        key5th.append(key)
                        print('Key Found: key5th = ' + key1 + ' ' + key2 + ' ' + key4 + ' ' + key )

        key6th = []
        for key5 in key5th:
            for key4 in key4th:
                for key2 in key2nd:
                    for key1 in key1st:

                        try: keys = data[key1]['FullStudies'][0][key3][key4][key5].keys()

                        except AttributeError: continue
                        except KeyError:
                            try: value = data[key1]['FullStudies'][0][key3][key4][key5]
                            except AttributeError: continue
                            except KeyError: continue

                            keysFound = [key1, 'FullStudies', 0, key3, key4, key5]
                            key_saved(key5, keysFound)
                            continue

                        for key in data[key1]['FullStudies'][0][key3][key4][key5].keys():
                            print('Key6th  = ')
                            print(keys)
                            key6th.append(key)
                            print('Key Found: key6th = ' + key1 + ' ' + key2 + ' ' + key4 + ' ' + key5 + ' ' + key )


        key7th = []
        for key6 in key6th:
            for key5 in key5th:
                for key4 in key4th:
                    for key2 in key2nd:
                        for key1 in key1st:

                            try: keys = data[key1]['FullStudies'][0][key3][key4][key5][key6].keys()

                            except KeyError:
                                try: value = data[key1]['FullStudies'][0][key3][key4][key5][key6]
                                except KeyError: continue

                                keysFound = [key1, 'FullStudies', 0, key3, key4, key5, key6]
                                key_saved(key6, keysFound)
                                continue

                            for key in data[key1]['FullStudies'][0][key3][key4][key5][key6].keys():
                                print('Key7th  = ')
                                print(keys)
                                key7th.append(key)
                                print('Key Found: key7th = ' + key1 + ' ' + key2 + ' ' + key4 + ' ' + key5 + ' ' + key6 + ' ' + key )

        key8th = []
        for key7 in key7th:
            for key6 in key6th:
                for key5 in key5th:
                    for key4 in key4th:
                        for key2 in key2nd:
                            for key1 in key1st:

                                try: keys = data[key1]['FullStudies'][0][key3][key4][key5][key6][key7].keys()

                                except KeyError:
                                    try: value = data[key1]['FullStudies'][0][key3][key4][key5][key6][key7]
                                    except KeyError: continue

                                    keysFound = [key1, 'FullStudies', 0, key3, key4, key5, key6, key7]
                                    key_saved(key7, keysFound)
                                    continue

                                for key in data[key1]['FullStudies'][0][key3][key4][key5][key6][key7].keys():
                                    print('Key8th  = ')
                                    print(keys)
                                    key7th.append(key)
                                    print('Key Found: key8th = ' + key1 + ' ' + key2 + ' ' + key4 + ' ' + key5 + ' ' + key6 + ' ' + key7 + ' ' + key8 )




def key_saved(key_name, keys):
    """

    """
    save_file = retrieve_path('json_keys_clinical')
    file = open(save_file, 'a')
    file.write(key_name + ',')
    for key in keys:
        file.write(key + ' ')
    file.write('\n')
    file.close()





if __name__ == "__main__":
    main()
