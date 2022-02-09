import os
import pandas as pd
import pypatent

from c0001_retrieve_meta import retrieve_path

def aggregate_patents():
  """

  """
  print('beginning aggregate_patents')

  df_aggregated = pd.DataFrame()

  total_queried = 0
  for file in os.listdir(retrieve_path('df_patent')):

      df_patent = os.path.join(retrieve_path('df_patent'), file)
      df = pd.read_csv(df_patent)

      print('file = ')
      print(file)
      print('len df = ' + str(len(list(df['url']))))
      print('total queried = ')
      total_queried = total_queried + len(list(df['url']))
      print(total_queried)

      df_aggregated = df_aggregated.append(df)

      df_aggregated = df_aggregated.drop_duplicates(subset=['url'])
      df_aggregated.sort_values(by=['patent_num'], inplace=True)
      print('len df_aggregated = ' + str(len(list(df_aggregated['url']))))

  df_aggregated = df_aggregated.drop_duplicates(subset=['url'])
  df_aggregated.sort_values(by=['patent_num'], inplace=True)
  df_aggregated.reset_index()

  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg' + '.csv')
  print('df_file = ' + str(df_file))
  print('df_aggregated = ')
  print(df_aggregated)
  df_aggregated.to_csv(df_file)

  print('completed aggregate_patents')
