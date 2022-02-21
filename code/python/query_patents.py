from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.peds.tasks import UsptoPatentExaminationDataSystemDownloader

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pypatent
import statistics
from selenium import webdriver

from a0001_admin import retrieve_format
from a0001_admin import retrieve_path
from a0001_admin import retrieve_datetime
from a0001_admin import retrieve_list
from a0001_admin import name_paths

def query_patents(name_article, term, result_limits):
  """

  """
  print('beginning query_patents')


  # Try pypatent
  # https://pypi.org/project/pypatent/
  conn = pypatent.WebConnection(use_selenium=False, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')

  #driver = webdriver.Firefox()  # Requires geckodriver in your PATH
  #conn = pypatent.WebConnection(use_selenium=True, selenium_driver=driver)


  for term in retrieve_list('term_search'):

      for year in np.arange(1980, 1982, 1):

          for result_limit in list(retrieve_format('patent_result_limits')):

              print('result_limit = ' + str(result_limit))
              result_limit = int(result_limit)

              print('result_limit = ' + str(result_limit) + ' ' + str(retrieve_datetime()))
              print(term + ' searching with pypatent: began ' + str(retrieve_datetime()))

              query_term  = str('abst=' + term + ' , ' + 'aclm=' + term + ' , ' + 'spec=' + term + ' , ' + ' isd=' + str(2020) )
              query_term  = str('isd=' + str(year) )
              query_term  = str('aclm/' + term + ' and ' + ' isd/' + str(year) )
              query_term  = str(term + ' and ' + ' isd/' + str(year) )
              # did not work query_term  = str(term + ', ' + ' isd=' + str(year) )
              query_term  = str(term)
              # did not work query_term  = str('aclm=' + term)
              print('query_term = ' + str(query_term))

              df = pd.DataFrame()
              df = pypatent.Search(query_term , results_limit=result_limit , get_patent_details=True , web_connection=conn).as_dataframe()
              # df = pypatent.Search((query_term), web_connection=conn).as_dataframe()
              # *** [Makefile:6: pythonanalysis] Error 1 df = pypatent.Search(query_term).as_dataframe()
              # df = pypatent.Search(query_term, web_connection=conn).as_dataframe()

              print(term + ' searching with pypatent: ended ' + str(retrieve_datetime()))
              print('result_limit = ' + str(result_limit) + ' ' + str(retrieve_datetime()))
              print(' df = ')
              print(df)
              print('len(df[url]) = ' )
              print(len(list(df['url'])))
              print('column names = ')
              print(df.columns.values.tolist())

              name_src, name_dst, name_summary, name_unique, plot_unique = name_paths(name_article)
              df_patent = os.path.join(retrieve_path(name_src), term + '-' + str(result_limit) + ' ' + str(retrieve_datetime()) + '.csv')
              print('file saved to df_patent = ' + str(df_patent))
              df.to_csv(df_patent)

              print(df.iloc[:,0])
              print(list(df.iloc[:,0]))
              print(len(list(df.iloc[:,0])))
              if len(list(df.iloc[:,0])) < result_limit: break
              df = pd.DataFrame()

  print('completed query_patents')
