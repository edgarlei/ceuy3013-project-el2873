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
#!pip install --upgrade pandas
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

# --- CSV Redux, Concatenation, and Extraction
'''Because of the size of each original data file, it was better to run them through
individually instead of all at once (hence the lack of a for loop in the csv_redux
function). This also allows the user to check for individual file errors without
stopping the entire process all at once.'''
jan19 = csv_redux('201901-citibike-tripdata.csv')
feb19 = csv_redux('201902-citibike-tripdata.csv')
mar19 = csv_redux('201903-citibike-tripdata.csv')
apr19 = csv_redux('201904-citibike-tripdata.csv')
may19 = csv_redux('201905-citibike-tripdata.csv')
jun19 = csv_redux('201906-citibike-tripdata.csv')
jul19 = csv_redux('201907-citibike-tripdata.csv')
aug19 = csv_redux('201908-citibike-tripdata.csv')
sep19 = csv_redux('201909-citibike-tripdata.csv')
oct19 = csv_redux('201910-citibike-tripdata.csv')
nov19 = csv_redux('201911-citibike-tripdata.csv')
dec19 = csv_redux('201912-citibike-tripdata.csv')
jan20 = csv_redux('202001-citibike-tripdata.csv')
feb20 = csv_redux('202002-citibike-tripdata.csv')
mar20 = csv_redux('202003-citibike-tripdata.csv')
apr20 = csv_redux('202004-citibike-tripdata.csv')
may20 = csv_redux('202005-citibike-tripdata.csv')
jun20 = csv_redux('202006-citibike-tripdata.csv')
jul20 = csv_redux('202007-citibike-tripdata.csv')
aug20 = csv_redux('202008-citibike-tripdata.csv')
sep20 = csv_redux('202009-citibike-tripdata.csv')
oct20 = csv_redux('202010-citibike-tripdata.csv')
nov20 = csv_redux('202011-citibike-tripdata.csv')
'''Once all the original datasets are reduced, they are all concatenated into a
new master dataset for use in the program proper.'''
comb = pd.concat([jan19, feb19, mar19, apr19, may19, jun19, jul19, aug19, sep19,
                  oct19, nov19, dec19, jan20, feb20, mar20, apr20, may20, jun20,
                  jul20, aug20, sep20, oct20, nov20])
comb.to_csv('masterdata.csv')
print(comb)

# from google.colab import files
# files.download('masterdata.csv')
