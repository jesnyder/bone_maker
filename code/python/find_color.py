import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

from a0001_admin import retrieve_color
from a0001_admin import retrieve_path
from a0001_admin import retrieve_format

def find_color(num):
    """

    """

    # print('finding color')

    #colorTransparency = retrieve_ref('scatterTransparency')
    colorTransparency = 0.8

    """
    colorOrange = [240/255, 83/255, 35/255]
    colorPurple = [23/255, 27/255, 96/255]
    colorBlueDark = [0/255, 153/255, 216/255]
    colorBlueLight = [0/255, 188/255, 231/255]
    colorGray = [233/255, 225/255, 223/255]

    colorGreen = [233/255, 25/255, 223/255]
    colorPink = [240/255, 10/255, 10/255]
    colorYellow = [240/255, 100/255, 10/255]
    colorBlue = [10/255, 10/255, 223/255]

    colorMarker = colorOrange
    colorEdge = colorPurple
    """

    variant = random.randint(-50,50)
    variant = variant/50
    variant_change_strong = 0.2
    variant_change_weak = 0.1


    color_values =  retrieve_color(num)
    colorMarker = color_values
    colorEdge = color_values

    for j in range(len(color_values)):
        if color_values[j] == max(color_values):
            colorMarker[j] = color_values[j] + variant*variant_change_weak
        else:
            colorMarker[j] = color_values[j] + variant*variant_change_strong

    """
    for j in range(len(colorMarker)):

        if num%8 == 0:
            if j == 0:  colorMarker[j] = colorOrange[0] + variant*variant_change_weak
            if j == 1:  colorMarker[j] = colorOrange[1] - variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorOrange[2] + variant*variant_change_strong

        if num%8 == 1:
            if j == 0:  colorMarker[j] = colorBlueDark[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorBlueDark[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorBlueDark[2] + variant*variant_change_weak

        if num%8 == 2:
            if j == 0:  colorMarker[j] = colorBlueLight[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorBlueLight[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorBlueLight[2] + variant*variant_change_weak

        if num%8 == 3:
            if j == 0:  colorMarker[j] = colorPurple[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorPurple[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorPurple[2] + variant*variant_change_weak

        if num%8 == 4:
            if j == 0:  colorMarker[j] = colorGreen[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorGreen[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorGreen[2] + variant*variant_change_weak

        if num%8 == 5:
            if j == 0:  colorMarker[j] = colorPink[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorPink[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorPink[2] + variant*variant_change_weak

        if num%8 == 6:
            if j == 0:  colorMarker[j] = colorYellow[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorYellow[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorYellow[2] + variant*variant_change_weak

        if num%8 == 7:
            if j == 0:  colorMarker[j] = colorBlue[0] - variant*variant_change_strong
            if j == 1:  colorMarker[j] = colorBlue[1] + variant*variant_change_strong
            if j == 2:  colorMarker[j] = colorBlue[2] + variant*variant_change_weak
    """

    for ii in range(len(colorMarker)):
        colorMarker[ii] = round(colorMarker[ii],4)
        if colorMarker[ii] > 1: colorMarker[ii] = 1
        elif colorMarker[ii] < 0: colorMarker[ii] = 0

    colorEdge[j] = 0.25*colorMarker[j]

    """
    print('colorMarker = ')
    print(colorMarker)

    print('colorEdge = ')
    print(colorEdge)

    print('scatterTransparency = ' + str(scatterTransparency))
    """

    return(colorMarker, colorEdge, colorTransparency)
