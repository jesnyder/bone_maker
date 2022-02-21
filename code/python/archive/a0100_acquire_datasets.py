import numpy as np
import os
import pandas as pd
import wikipedia

from a0001_retrieve_meta import retrieve_path
from acquire_nsf_awards import acquire_nsf_awards
from acquire_nih_awards import acquire_nih_awards
from acquire_clinical_trials import acquire_clinical_trials
from acquire_patents import acquire_patents
from acquire_gscholar import acquire_gscholar


def acquire_datasets():
    """
    Objective:
        Scrape information from websites

    Tasks:
        1. Acquire NIH Awards
        2. Acquire NSF Awards
        3. Acquire Clinical Trials
        4. Acquire US Patent Office
        5. Acquire Peer Reviewed Literature
    """
    tasks = [6]
    print('beginning main')
    if 0 in tasks: tasks = np.arange(1, 101, 1)

    if 1 in tasks: acquire_nsf_awards()
    if 2 in tasks: acquire_nih_awards()
    if 3 in tasks: acquire_clinical_trials()

    # list search terms
    df = pd.read_csv(os.path.join(retrieve_path('search_terms')))
    for term in list(df['term']):
        if 4 in tasks: acquire_patents(term)
        if 5 in tasks: acquire_gscholar(term)
        if 6 in tasks: acquire_wikipedia(term)

    print('completed main')


def acquire_wikipedia(term):
    """

    """

    result = wikipedia.summary(term)
    print(result)

    result = wikipedia.summary('allogeneic')
    print(result)

    result = wikipedia.summary('autologous')
    print(result)
