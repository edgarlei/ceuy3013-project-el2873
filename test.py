# --- Imports ---------------------------
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import math
import statistics as st
import matplotlib.pyplot as plt

from source import csv_redux, program_proper, preds, overall

# Example of CSV File Reduction
print(csv_redux('input\oct2019-citibike-tripdata.csv'))

# Example of Subcategorical Analysis
print(overall([2019, 2020]))

# Main bulk of program
print(program_proper())

# Predictions for December 2020
print(preds(11))
