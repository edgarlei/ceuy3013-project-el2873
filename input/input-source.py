# --- Imports ---------------------------
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import math
import statistics as st
import matplotlib.pyplot as plt

# Inline Plots
%matplotlib inline

# For High-Res Plots
%config InlineBackend.figure_formats = ['svg']

# Checking versions, updating to newest available
!pip install --upgrade pandas
#!pip install --upgrade numpy
#!pip install --upgrade scipy
#!pip install --upgrade stats
#!pip install --upgrade math
#!pip install --upgrade statistics
#!pip install --upgrade matplotlib

# --- Main ------------------------------
'''Because of the sheer size of the data files and the unwieldiness of having to
run through nearly 50 million data points each time, it was decided that a sample
of the dataset was to be used, while making sure that it is still reflective enough
of the overall datset. This also prevents overfitting, which would cause any
conclusions or analysis to be too overly specific.'''
def csv_redux(datafile):

  '''Reads CSV file and converts contents into dataframe.'''
  data = pd.read_csv(datafile)

  '''Retrieving only the necessary columns. The latitudes of the start and end
  stations and their corresponding station IDs, as well as the customer IDs, are
  not relevant to the purposes of this project. In addition, the stop times are
  not needed because the month and year of each trip is determined by the time at
  which they began.'''
  data_cols = data[['tripduration', 'starttime', 'start station name', 'end station name', 'usertype', 'birth year', 'gender']]

  '''Removing all trips with a duration of at least five hours. Chances are the
  high duration of most of these trips are due to improper docking. For example,
  some of the longest "trips" were reported to be at least several days long.'''
  data_err = data_cols[data_cols.tripduration < 18000]

  '''Removing all trips shorter than five minutes that start and end at the same
  CitiBike station. These also seem likely to be the result of user error, or if
  not, do not constitute significant trips.'''
  data_fil = data_err.drop(data_err[(data_err['tripduration'] < 300) & (data_err['start station name'] == data_err['end station name'])].index)

  '''Converting seconds to minutes for more practical application'''
  data_fil['tripduration'] = data_fil['tripduration'] / 60

  '''It was decided that 20% of each month's data set will be randomly extracted
  and used as the sample set. A proportion was used inside of a flat quantity in
  order to maintain the true frequency of trips per month. This proportion is small
  enough to work with, but still large enough to reflect the overall dataset no
  matter which datapoints are chosen. For example, the October 2020 dataset was
  reduced to 445,621 data points, which is equivalent to an average of
  just under 15,000 per day, around 620 per hour, and 10 per minute.'''

  '''In order to make sure the sample set statistically represents the original data
  to a certain degree, the mean of the sample trip durations is checked to make sure
  it is within 0.25 standard deviations from the population mean. If it is not in this
  range, the sample is continually regenerated until this requirement is met.'''
  lower_bound = data_fil.tripduration.mean() - 0.25 * data_fil.tripduration.std()
  upper_bound = data_fil.tripduration.mean() + 0.25 * data_fil.tripduration.std()
  def gen_sample():
    piece = data_fil.sample(frac=0.20, axis=0)
    return piece
  sample = gen_sample()
  sam_td_mn = sample.tripduration.mean()
  while sam_td_mn > 0:
    if (sam_td_mn > lower_bound) & (sam_td_mn < upper_bound):
      break
    else:
      sample = gen_sample()

  '''When the sample is taken, the original indices are kept. In order to be able
  to properly index any given data set, the index is reset from 0 to the length of
  the sample.'''
  sample.reset_index(drop=True, inplace=True)

  '''Extracting year and month from starttime column'''
  for i in str(len(sample)):
    sample['year'] = sample.starttime[int(i)][0:4]
    sample['month'] = sample.starttime[int(i)][5:7]
  return sample
