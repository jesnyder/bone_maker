import numpy as np
import os
import pandas as pd
import pypatent

from c0001_retrieve_meta import retrieve_path
from c0001_retrieve_meta import retrieve_datetime

def check_claims():
  """

  """
  print('beginning check_claims')

  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg' + '.csv')
  df = pd.read_csv(df_file)
  # del df['Unnamed: 0']
  # df = df.reset_index()

  df_inclusive_terms = pd.read_csv(retrieve_path('inclusive_terms'))

  claims = list(df['claims'])
  descriptions = list(df['description'])

  scores = []
  for i in range(len(claims)):
      score = 0
      for term in list(df_inclusive_terms['inclusive_terms']):

          if term in str(claims[i]): score = score + 1
          if term in str(descriptions[i]): score = score + 1

      # print('score = ' + str(score))
      scores.append(score)

  count_scores(scores)
  df['scores'] = scores

  df.sort_values(by=['patent_num'], inplace=True)
  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim' + '.csv')
  df.to_csv(df_file)

  print('before claim drop len df = ' + str(len(list(df['url']))))
  df = df.drop(df[df.scores < 2].index)
  print('after plain drop len df = ' + str(len(list(df['url']))))
  df_file = os.path.join(retrieve_path('df_aggregated'), 'agg_claim_drop' + '.csv')
  df.to_csv(df_file)

  print('completed check_claims')


def count_scores(scores):
     """

     """
     print('len before truncation = ' + str(len(scores)))

     score_range = np.arange(0, max(scores)+1, 1)
     df = pd.DataFrame()
     df['scores'] = score_range

     score_range_counts = []
     score_percentage = []
     score_sum = []
     for item in score_range:

        # number of patents with that score or higher
        score_sum.append( len(scores) - sum(score_range_counts))

        # percentage of patents with that score or higher
        percentage = 100*float( 1 - sum(score_range_counts) / len(scores))
        score_percentage.append(str(round(percentage,3)))

        # number of patents with a specific score
        score_range_counts.append(scores.count(int(item)))

     df['counts'] = score_range_counts
     df['cumulative_counts'] = score_sum
     df['cumulative_percentage'] = score_percentage

     df_file = os.path.join(retrieve_path('score_count'))
     df.to_csv(df_file)
