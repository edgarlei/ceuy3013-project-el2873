# --- Imports ---------------------------
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import math
import statistics as st
import matplotlib.pyplot as plt

from source import csv_redux

oct20 = csv_redux('input\oct2019-citibike-tripdata.csv')
nov20 = csv_redux('input\znov2019-citibike-tripdata.csv')
comb = pd.concat([oct20, nov20])

oct20_run = oct20.head(n=15)

def add_col(data):
  for i in str(len(data)):
    data['year'] = data.starttime[int(i)][0:4]
    data['month'] = data.starttime[int(i)][5:7]
  return data

add_col(oct20_run)

def check_sample(data):
  lower_bound = data.tripduration.mean() - 0.25 * data.tripduration.std()
  upper_bound = data.tripduration.mean() + 0.25 * data.tripduration.std()
  def gen_sample():
    piece = data.sample(frac=0.25, axis=0)
    return piece
  sample = gen_sample()
  sam_td_mn = sample.tripduration.mean()
  while sam_td_mn > 0:
    if (sam_td_mn > lower_bound) & (sam_td_mn < upper_bound):
      break
    else:
      sample = gen_sample()
  return sample

check_sample(oct20)

# Given the years for which data is desired, the total number of trips per month is calculated (extrapolated back to size of original dataset)
def monthly_count(yrs):
  lists = []
  for i in yrs:
    for j in range(1, 13):
      count = 5 * len(md[(md['year'] == i) & (md['month'] == j)])
      lists.append(count)
  splits = [lists[x:x + 12] for x in range(0, len(lists), 12)]
  return splits

month_cnt = monthly_count([2019, 2020])
ovr19, ovr20 = month_cnt[:]

# Given the years for which data is desired, the average trip duration for each month is calculated
def monthly_average(yrs):
  lists = []
  for i in yrs:
    for j in range(1, 13):
      count = md[(md['year'] == i) & (md['month'] == j)]['tripduration'].mean()
      lists.append(count)
  splits = [lists[x:x + 12] for x in range(0, len(lists), 12)]
  return splits

month_avg = monthly_average([2019, 2020])
ovr19_avg, ovr20_avg = month_avg[:]

# Given the years for which data is desired, the total number of trips per month per gender is calculated (extrapolated back to size of original dataset)
def gender_count(yrs):
  lists = []
  for k in range(0, 3):
    for i in yrs:
      for j in range(1, 13):
        count = 5 * len(md[(md['year'] == i) & (md['month'] == j) & (md['gender'] == k)])
        lists.append(count)
  splits = [lists[x:x + 12] for x in range(0, len(lists), 12)]
  return splits

gender_cnt = gender_count([2019, 2020])
o19cnt, o20cnt, m19cnt, m20cnt, f19cnt, f20cnt = gender_cnt[:]

# Given the years for which data is desired, the average duration of trips per month per gender is calculated (extrapolated back to size of original dataset)
def gender_average(yrs):
  lists = []
  for k in range(0, 3):
    for i in yrs:
      for j in range(1, 13):
        count = md[(md['year'] == i) & (md['month'] == j) & (md['gender'] == k)]['tripduration'].mean()
        lists.append(count)
  splits = [lists[x:x + 12] for x in range(0, len(lists), 12)]
  return splits

gender_avg = gender_average([2019, 2020])
o19avg, o20avg, m19avg, m20avg, f19avg, f20avg = gender_avg[:]
