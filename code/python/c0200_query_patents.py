from uspto.peds.client import UsptoPatentExaminationDataSystemClient
from uspto.peds.tasks import UsptoPatentExaminationDataSystemDownloader

import os
import pandas as pd
import pypatent

from c0001_retrieve_meta import retrieve_path

def query_patents():
  """

  """
  print('beginning query_patents')

  # Try pypatent
  # https://pypi.org/project/pypatent/

  conn = pypatent.WebConnection(use_selenium=False, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')

  # search_terms
  path = retrieve_path('search_terms')
  df = pd.read_csv(path)
  search_terms = list(df['search_terms'])
  # search_terms = ['craniofacial', 'biomanufacturing', 'tissue engineering', 'biofabrication', 'osseointegration', 'mandible', 'osteoconductive']
  result_limits = [10, 50, 100, 500, 1000, 5000, 300000]

  for term in search_terms:

      for result_limit in result_limits:

          # result_limit = 300000
          # result_limit = 10
          df = pypatent.Search(term , results_limit=result_limit , get_patent_details=True , web_connection=conn).as_dataframe()

          print('df = ')
          print(df)

          print('len(df[url]) = ' )
          print(len(list(df['url'])))

          df_patent = os.path.join(retrieve_path('df_patent'), term + '-' + str(result_limit) + '.csv')
          print('file saved to df_patent = ' + str(df_patent))
          df.to_csv(df_patent)

          my_list = df.columns.values.tolist()
          print('column names = ')
          print(my_list)


  """
  downloader = UsptoPatentExaminationDataSystemDownloader()

  # Start downloading single document
  # Automatically guesses the document type
  # Will acquire both XML and JSON formats
  downloader.run('PP28532')

  # Start downloading multiple documents, with document type autoguessing and dual format acquisition
  downloader.run(['PP28532', 'US20170293197A1'])

  # Wait until results arrived
  result = downloader.poll()

  print(result)
  """

  print('completed query_patents')
