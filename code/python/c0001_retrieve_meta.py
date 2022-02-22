from datetime import datetime
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def retrieve_ref(variableName):

    file = os.path.join(retrieve_path('ref_variable'))
    df = pd.read_csv(file)

    variableNames = list(df['name'])
    variableValues = list(df['value'])

    value = 0
    for i in range(len(variableNames)):
        if variableName == variableNames[i]:
            value = variableValues[i]
            break

    # print('value = ' + str(value))
    return value



def retrieve_path(description):
    """
    retrieve path to find the file
    """

    # print("running retrieve_path")

    path_file = os.path.join('user_provided', 'paths', 'paths.csv')
    df = pd.read_csv(path_file)


    df = df.loc[df['description'] == description]

    path = list(df['path'])
    path = path[0]
    path = path.split(' ')


    # build the folder required to save a file
    for folder in path:

        # skip file names
        if '.' in str(folder):
            break

        # intiate a new variable to describe the path
        if folder == path[0]:
            path_short = os.path.join(folder)

        # add folders iteratively to build path
        else:
            path_short = os.path.join(path_short, folder)

        # check if the path exists
        if not os.path.exists(path_short):
            os.makedirs(path_short)


    path = os.path.join(*path)

    # print("completed retrieve_path")

    return(path)


def retrieve_datetime():
    """

    """

    # datetime object containing current date and time
    now = datetime.now()

    print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H %M %S")
    print("date and time =", dt_string)

    return(dt_string)


if __name__ == "__main__":
    main()


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

    del df['index']

    return(df)
