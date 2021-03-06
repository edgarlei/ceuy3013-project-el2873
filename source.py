# Please have patience when running the code.
# It takes around ten minutes to fully run through,
# and then the figures take an additional minute
# or so to show up.

# --- Imports ---------------------------
import pandas as pd
import numpy as np
import scipy as sp
from scipy import stats
import math
import statistics as st
import matplotlib.pyplot as plt

# --- SETUP ------------------------------
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

# --- PROGRAM PROPER -----------------------------------
def program_proper():
    # --- CSV Redux, Concatenation, and Extraction
    '''Because of the size of each original data file, it was better to run them through
    individually instead of all at once (hence the lack of a for loop in the csv_redux
    function). This also allows the user to check for individual file errors without
    stopping the entire process all at once.'''
    '''Due to the way Atom processed some of the file names, a z had to be added to the
    front of the file name to get around the issue.'''
    jan19 = csv_redux('input\jan2019-citibike-tripdata.csv')
    feb19 = csv_redux('input\zfeb2019-citibike-tripdata.csv')
    mar19 = csv_redux('input\mar2019-citibike-tripdata.csv')
    apr19 = csv_redux('input\zapr2019-citibike-tripdata.csv')
    may19 = csv_redux('input\may2019-citibike-tripdata.csv')
    jun19 = csv_redux('input\jun2019-citibike-tripdata.csv')
    jul19 = csv_redux('input\jul2019-citibike-tripdata.csv')
    aug19 = csv_redux('input\zaug2019-citibike-tripdata.csv')
    sep19 = csv_redux('input\sep2019-citibike-tripdata.csv')
    oct19 = csv_redux('input\oct2019-citibike-tripdata.csv')
    nov19 = csv_redux('input\znov2019-citibike-tripdata.csv')
    dec19 = csv_redux('input\dec2019-citibike-tripdata.csv')
    jan20 = csv_redux('input\jan2019-citibike-tripdata.csv')
    feb20 = csv_redux('input\zfeb2019-citibike-tripdata.csv')
    mar20 = csv_redux('input\mar2019-citibike-tripdata.csv')
    apr20 = csv_redux('input\zapr2019-citibike-tripdata.csv')
    may20 = csv_redux('input\may2019-citibike-tripdata.csv')
    jun20 = csv_redux('input\jun2019-citibike-tripdata.csv')
    jul20 = csv_redux('input\jul2019-citibike-tripdata.csv')
    aug20 = csv_redux('input\zaug2019-citibike-tripdata.csv')
    sep20 = csv_redux('input\sep2019-citibike-tripdata.csv')
    oct20 = csv_redux('input\oct2019-citibike-tripdata.csv')
    nov20 = csv_redux('input\znov2019-citibike-tripdata.csv')
    '''Once all the original datasets are reduced, they are all concatenated into a
    new master dataset for use in the program proper.'''
    md = pd.concat([jan19, feb19, mar19, apr19, may19, jun19, jul19, aug19, sep19,
              oct19, nov19, dec19, jan20, feb20, mar20, apr20, may20, jun20,
              jul20, aug20, sep20, oct20, nov20])

    # --- Graphing/Plotting Labels ------------------------------
    # Label(s) for all figures
    x_lab = 'Month'
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
            'Nov', 'Dec']
    months11 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
            'Nov']

    # Label(s) specific to frequency figures
    y_lab_frq = 'Number of Trips'

    # Label(s) specific to duration figures
    y_lab_avg = 'Trip Duration (minutes)'

    # Bar Graph Bar Widths and Spacing
    xlab_interval = np.arange(len(months))
    width = 0.4

    # --- OVERALL ------------------------------
    # Given the years for which data is desired, the monthly number of trips and average trip duration are calculated

    def overall(yrs):
        # Creates two empty lists: one for frequency, one for average duration.
        freq_lists = []
        avg_lists = []
        '''Iterates through two layers of for loops: for each month in each year. The frequency and average duration
        for each month is calculated and added to the corresponding list.
        '''
        for i in yrs:
            for j in range(1, 13):
                freq_count = 5 * len(md[(md['year'] == i) & (md['month'] == j)])
                freq_lists.append(freq_count)
                avg_count = md[(md['year'] == i) & (md['month'] == j)]['tripduration'].mean()
                avg_lists.append(avg_count)
        # Splits each of the two lists by intervals of twelve for each year.
        freq_splits = [freq_lists[x:x + 12] for x in range(0, len(freq_lists), 12)]
        avg_splits = [avg_lists[x:x + 12] for x in range(0, len(avg_lists), 12)]
        return freq_splits, avg_splits

    ovr = overall([2019, 2020])
    ovr19cnt, ovr20cnt = ovr[0][:]
    ovr19avg, ovr20avg = ovr[1][:]

    # Creating Grid of Comparison Figures by Month Overall

    fig, ax = plt.subplots(nrows=9, ncols=2, figsize=(15, 20))

    # Titles
    ovr_title_frq = 'Overall CitiBike Trips per Month'
    ovr_title_avg = 'Overall Average Monthly CitiBike Trip Duration'

    ## --- Overall Frequency --------------------

    # Line plot
    ax[0, 0].plot(months, ovr19cnt, label='2019')
    ax[0, 0].plot(months11, ovr20cnt[0:11], label='2020')
    ax[0, 0].set_title(ovr_title_frq, weight='bold')
    ax[0, 0].set_xlabel(x_lab)
    ax[0, 0].set_ylabel(y_lab_frq)
    ax[0, 0].grid(ls='--')
    ax[0, 0].legend()

    # Bar graph
    ax[0, 1].bar(xlab_interval - width/2, ovr19cnt, width, label='2019')
    ax[0, 1].bar(xlab_interval + width/2, ovr20cnt, width, label='2020')
    ax[0, 1].set_title(ovr_title_frq, weight='bold')
    ax[0, 1].set_xlabel(x_lab)
    ax[0, 1].set_xticks(xlab_interval)
    ax[0, 1].set_xticklabels(months)
    ax[0, 1].set_ylabel(y_lab_frq)
    ax[0, 1].grid(ls='--')
    ax[0, 1].legend()

    ## --- Overall Duration --------------------

    # Line plot
    ax[1, 0].plot(months, ovr19avg, label='2019')
    ax[1, 0].plot(months, ovr20avg, label='2020')
    ax[1, 0].set_title(ovr_title_avg, weight='bold')
    ax[1, 0].set_xlabel(x_lab)
    ax[1, 0].set_ylabel(y_lab_avg)
    ax[1, 0].grid(ls='--')
    ax[1, 0].legend()

    # Bar graph
    ax[1, 1].bar(xlab_interval - width/2, ovr19avg, width, label='2019')
    ax[1, 1].bar(xlab_interval + width/2, ovr20avg, width, label='2020')
    ax[1, 1].set_title(ovr_title_avg, weight='bold')
    ax[1, 1].set_xlabel(x_lab)
    ax[1, 1].set_xticks(xlab_interval)
    ax[1, 1].set_xticklabels(months)
    ax[1, 1].set_ylabel(y_lab_avg)
    ax[1, 1].grid(ls='--')
    ax[1, 1].legend()

    # --- BY GENDER ------------------------------
    # Given the years for which data is desired, the monthly number of trips and average trip duration are calculated for each gender
    # 0: Other/unknown
    # 1: Male
    # 2: Female
    def by_gender(yrs):
        # Creates two empty lists: one for frequency, one for average duration.
        freq_lists = []
        avg_lists = []
        '''Iterates through three layers of for loops: for each month in each year for each gender. The frequency and average duration
        for each month for each gender is calculated and added to the corresponding list.
        '''
        for k in range(0, 3):
            for i in yrs:
                for j in range(1, 13):
                    freq_count = 5 * len(md[(md['year'] == i) & (md['month'] == j) & (md['gender'] == k)])
                    freq_lists.append(freq_count)
                    avg_count = md[(md['year'] == i) & (md['month'] == j) & (md['gender'] == k)]['tripduration'].mean()
                    avg_lists.append(avg_count)
        # Splits each of the two lists by intervals of twelve for each year.
        freq_splits = [freq_lists[x:x + 12] for x in range(0, len(freq_lists), 12)]
        avg_splits = [avg_lists[x:x + 12] for x in range(0, len(avg_lists), 12)]
        return freq_splits, avg_splits

    gender = by_gender([2019, 2020])
    o19cnt, o20cnt, m19cnt, m20cnt, f19cnt, f20cnt = gender[0][:]
    o19avg, o20avg, m19avg, m20avg, f19avg, f20avg = gender[1][:]


    # Titles
    gen_title_frq = 'Monthly CitiBike Trips per Gender'
    gen_title_avg = 'Average Monthly CitiBike Trip Duration per Gender'
    other_title_frq = 'Monthly CitiBike Trips for Riders of Other/Unknown Gender'
    other_title_avg = 'Average Monthly CitiBike Trip Duration for Riders of Other/Unknown Gender'
    male_title_frq = 'Monthly CitiBike Trips for Male Riders'
    male_title_avg = 'Average Monthly CitiBike Trip Duration for Male Riders'
    female_title_frq = 'Monthly CitiBike Trips for Female Riders'
    female_title_avg = 'Average Monthly CitiBike Trip Duration for Female Riders'

    # --- Gender Plots --------------------

    # Line plot for frequency
    ax[2, 0].plot(months, o19cnt, color='indigo', label='2019 Other/Unknown')
    ax[2, 0].plot(months11, o20cnt[0:11], color='forestgreen', label='2020 Other/Unknown')
    ax[2, 0].plot(months, m19cnt, color='blue', label='2019 Male')
    ax[2, 0].plot(months11, m20cnt[0:11], color='orange', label='2020 Male')
    ax[2, 0].plot(months, f19cnt, color='coral', label='2019 Female')
    ax[2, 0].plot(months11, f20cnt[0:11], color='teal', label='2020 Female')
    ax[2, 0].set_title(gen_title_frq, weight='bold')
    ax[2, 0].set_xlabel(x_lab)
    ax[2, 0].set_ylabel(y_lab_frq)
    ax[2, 0].grid(ls='--')
    ax[2, 0].legend()

    # Line plot for duration
    ax[2, 1].plot(months, o19avg, color='indigo', label='2019 Other/Unknown')
    ax[2, 1].plot(months, o20avg, color='forestgreen', label='2020 Other/Unknown')
    ax[2, 1].plot(months, m19avg, color='blue', label='2019 Male')
    ax[2, 1].plot(months, m20avg, color='orange', label='2020 Male')
    ax[2, 1].plot(months, f19avg, color='coral', label='2019 Female')
    ax[2, 1].plot(months, f20avg, color='teal', label='2020 Female')
    ax[2, 1].set_title(gen_title_avg, weight='bold')
    ax[2, 1].set_xlabel(x_lab)
    ax[2, 1].set_ylabel(y_lab_avg)
    ax[2, 1].grid(ls='--')
    ax[2, 1].legend()

    # --- Gender Bar Graphs --------------------

    # Bar graph for 'other/unknown' frequency
    ax[3, 0].bar(xlab_interval - width/2, o19cnt, width, color='indigo', label='2019')
    ax[3, 0].bar(xlab_interval + width/2, o20cnt, width, color='forestgreen', label='2020')
    ax[3, 0].set_title(other_title_frq, weight='bold')
    ax[3, 0].set_xlabel(x_lab)
    ax[3, 0].set_xticks(xlab_interval)
    ax[3, 0].set_xticklabels(months)
    ax[3, 0].set_ylabel(y_lab_frq)
    ax[3, 0].grid(ls='--')
    ax[3, 0].legend()

    # Bar graph for 'other/unknown' duration
    ax[3, 1].bar(xlab_interval - width/2, o19avg, width, color='indigo', label='2019')
    ax[3, 1].bar(xlab_interval + width/2, o20avg, width, color='forestgreen', label='2020')
    ax[3, 1].set_title(other_title_avg, weight='bold')
    ax[3, 1].set_xlabel(x_lab)
    ax[3, 1].set_xticks(xlab_interval)
    ax[3, 1].set_xticklabels(months)
    ax[3, 1].set_ylabel(y_lab_avg)
    ax[3, 1].grid(ls='--')
    ax[3, 1].legend()

    # Bar graph for 'male' frequency
    ax[4, 0].bar(xlab_interval - width/2, m19cnt, width, color='blue', label='2019')
    ax[4, 0].bar(xlab_interval + width/2, m20cnt, width, color='orange', label='2020')
    ax[4, 0].set_title(male_title_frq, weight='bold')
    ax[4, 0].set_xlabel(x_lab)
    ax[4, 0].set_xticks(xlab_interval)
    ax[4, 0].set_xticklabels(months)
    ax[4, 0].set_ylabel(y_lab_frq)
    ax[4, 0].grid(ls='--')
    ax[4, 0].legend()

    # Bar graph for 'male' duration
    ax[4, 1].bar(xlab_interval - width/2, m19avg, width, color='blue', label='2019')
    ax[4, 1].bar(xlab_interval + width/2, m20avg, width, color='orange', label='2020')
    ax[4, 1].set_title(male_title_avg, weight='bold')
    ax[4, 1].set_xlabel(x_lab)
    ax[4, 1].set_xticks(xlab_interval)
    ax[4, 1].set_xticklabels(months)
    ax[4, 1].set_ylabel(y_lab_avg)
    ax[4, 1].grid(ls='--')
    ax[4, 1].legend()

    # Bar graph for 'female' frequency
    ax[5, 0].bar(xlab_interval - width/2, f19cnt, width, color='coral', label='2019')
    ax[5, 0].bar(xlab_interval + width/2, f20cnt, width, color='teal', label='2020')
    ax[5, 0].set_title(female_title_frq, weight='bold')
    ax[5, 0].set_xlabel(x_lab)
    ax[5, 0].set_xticks(xlab_interval)
    ax[5, 0].set_xticklabels(months)
    ax[5, 0].set_ylabel(y_lab_frq)
    ax[5, 0].grid(ls='--')
    ax[5, 0].legend()

    # Bar graph for 'female' duration
    ax[5, 1].bar(xlab_interval - width/2, f19avg, width, color='coral', label='2019')
    ax[5, 1].bar(xlab_interval + width/2, f20avg, width, color='teal', label='2020')
    ax[5, 1].set_title(female_title_avg, weight='bold')
    ax[5, 1].set_xlabel(x_lab)
    ax[5, 1].set_xticks(xlab_interval)
    ax[5, 1].set_xticklabels(months)
    ax[5, 1].set_ylabel(y_lab_avg)
    ax[5, 1].grid(ls='--')
    ax[5, 1].legend()

    # --- BY USER TYPE ------------------------------
    # Given the years for which data is desired, the monthly number of trips and average trip duration are calculated for each user type
    # Customer: 24-hr/3-day pass
    # Subscriber: Annual pass
    def by_user(yrs):
        # Creates two empty lists: one for frequency, one for average duration.
        freq_lists = []
        avg_lists = []
        '''Iterates through three layers of for loops: for each month in each year for each user type. The frequency and average duration
        for each month for each user type is calculated and added to the corresponding list.
        '''
        for k in (['Customer', 'Subscriber']):
            for i in yrs:
                for j in range(1, 13):
                    freq_count = 5 * len(md[(md['year'] == i) & (md['month'] == j) & (md['usertype'] == k)])
                    freq_lists.append(freq_count)
                    avg_count = md[(md['year'] == i) & (md['month'] == j) & (md['usertype'] == k)]['tripduration'].mean()
                    avg_lists.append(avg_count)
        # Splits each of the two lists by intervals of twelve for each year.
        freq_splits = [freq_lists[x:x + 12] for x in range(0, len(freq_lists), 12)]
        avg_splits = [avg_lists[x:x + 12] for x in range(0, len(avg_lists), 12)]
        return freq_splits, avg_splits

    user_stats = by_user([2019, 2020])
    cus19cnt, cus20cnt, sub19cnt, sub20cnt = user_stats[0][:]
    cus19avg, cus20avg, sub19avg, sub20avg = user_stats[1][:]

    # Creating Grid of Comparison Figures by User Type

    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))

    # Titles
    user_title_frq = 'Monthly CitiBike Trips per User Type'
    cus_title_frq = 'Monthly CitiBike Trips for Customers'
    sub_title_frq = 'Monthly CitiBike Trips for Subscribers'
    user_title_avg = 'Average Monthly CitiBike Trip Duration per User Type'
    cus_title_avg = 'Average Monthly CitiBike Trip Duration for Customers'
    sub_title_avg = 'Average Monthly CitiBike Trip Duration for Subscribers'

    # --- User Type Plots --------------------

    # Line plot for frequency
    ax[6, 0].plot(months, cus19cnt, color='blue', label='2019 Customers')
    ax[6, 0].plot(months11, cus20cnt[0:11], color='orange', label='2020 Customers')
    ax[6, 0].plot(months, sub19cnt, color='indigo', label='2019 Subscribers')
    ax[6, 0].plot(months11, sub20cnt[0:11], color='teal', label='2020 Subscribers')
    ax[6, 0].set_title(user_title_frq, weight='bold')
    ax[6, 0].set_xlabel(x_lab)
    ax[6, 0].set_ylabel(y_lab_frq)
    ax[6, 0].grid(ls='--')
    ax[6, 0].legend()

    # Line plot for duration
    ax[6, 1].plot(months, cus19avg, color='blue', label='2019 Customers')
    ax[6, 1].plot(months, cus20avg, color='orange', label='2020 Customers')
    ax[6, 1].plot(months, sub19avg, color='indigo', label='2019 Subscribers')
    ax[6, 1].plot(months, sub20avg, color='teal', label='2020 Subscribers')
    ax[6, 1].set_title(user_title_avg, weight='bold')
    ax[6, 1].set_xlabel(x_lab)
    ax[6, 1].set_ylabel(y_lab_avg)
    ax[6, 1].grid(ls='--')
    ax[6, 1].legend()

    # --- User Type Bar Graphs --------------------

    # Bar graph for customer frequency
    ax[7, 0].bar(xlab_interval - width/2, cus19cnt, width, color='blue', label='2019')
    ax[7, 0].bar(xlab_interval + width/2, cus20cnt, width, color='orange', label='2020')
    ax[7, 0].set_title(cus_title_frq, weight='bold')
    ax[7, 0].set_xlabel(x_lab)
    ax[7, 0].set_xticks(xlab_interval)
    ax[7, 0].set_xticklabels(months)
    ax[7, 0].set_ylabel(y_lab_frq)
    ax[7, 0].grid(ls='--')
    ax[7, 0].legend()

    # Bar graph for customer duration
    ax[7, 1].bar(xlab_interval - width/2, cus19avg, width, color='blue', label='2019')
    ax[7, 1].bar(xlab_interval + width/2, cus20avg, width, color='orange', label='2020')
    ax[7, 1].set_title(cus_title_avg, weight='bold')
    ax[7, 1].set_xlabel(x_lab)
    ax[7, 1].set_xticks(xlab_interval)
    ax[7, 1].set_xticklabels(months)
    ax[7, 1].set_ylabel(y_lab_avg)
    ax[7, 1].grid(ls='--')
    ax[7, 1].legend()

    # Bar graph for subscriber frequency
    ax[8, 0].bar(xlab_interval - width/2, sub19cnt, width, color='indigo', label='2019')
    ax[8, 0].bar(xlab_interval + width/2, sub20cnt, width, color='teal', label='2020')
    ax[8, 0].set_title(sub_title_frq, weight='bold')
    ax[8, 0].set_xlabel(x_lab)
    ax[8, 0].set_xticks(xlab_interval)
    ax[8, 0].set_xticklabels(months)
    ax[8, 0].set_ylabel(y_lab_frq)
    ax[8, 0].grid(ls='--')
    ax[8, 0].legend()

    # Bar graph for subscriber duration
    ax[8, 1].bar(xlab_interval - width/2, sub19avg, width, color='indigo', label='2019')
    ax[8, 1].bar(xlab_interval + width/2, sub20avg, width, color='teal', label='2020')
    ax[8, 1].set_title(sub_title_avg, weight='bold')
    ax[8, 1].set_xlabel(x_lab)
    ax[8, 1].set_xticks(xlab_interval)
    ax[8, 1].set_xticklabels(months)
    ax[8, 1].set_ylabel(y_lab_avg)
    ax[8, 1].grid(ls='--')
    ax[8, 1].legend()

    # Display
    fig.tight_layout()

    plt.show()

    # --- REGRESSION LINES ------------------------------------------
    '''Because the regression model can't take in months, they have to be replaced
    with the corresponding indices.'''
    xmonths = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    # --- REGRESSION LINES: FULL 2020 MODEL -------------------------
    '''From the plotted data points, polynomial regression models were derived from
    the 2020 data.
    '''
    fig1, ax1 = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))

    # Overall Number of Trips Monthly
    ax1[0, 0].scatter(months, ovr19cnt, label='2019')
    ax1[0, 0].scatter(months11, ovr20cnt[0:11], label='2020')
    ax1[0, 0].set_title(ovr_title_frq, weight='bold')
    ax1[0, 0].set_xlabel(x_lab)
    ax1[0, 0].set_ylabel(y_lab_frq)
    ax1[0, 0].grid(ls='--')
    ax1[0, 0].legend()
    ovr19cnt_poly = np.poly1d(np.polyfit(xmonths, ovr19cnt, 3))
    ovr20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], ovr20cnt[0:11], 3))
    ax1[0, 0].plot(xmonths, ovr19cnt_poly(xmonths))
    ax1[0, 0].plot(xmonths, ovr20cnt_poly(xmonths))

    # Overall Average Monthly Trip Duration
    ax1[0, 1].scatter(months, ovr19avg, label='2019')
    ax1[0, 1].scatter(months, ovr20avg, label='2020')
    ax1[0, 1].set_title(ovr_title_avg, weight='bold')
    ax1[0, 1].set_xlabel(x_lab)
    ax1[0, 1].set_ylabel(y_lab_avg)
    ax1[0, 1].grid(ls='--')
    ax1[0, 1].legend()
    ovr19avg_poly = np.poly1d(np.polyfit(xmonths, ovr19avg, 3))
    ovr20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], ovr20avg[0:11], 3))
    ax1[0, 1].plot(xmonths, ovr19avg_poly(xmonths))
    ax1[0, 1].plot(xmonths, ovr20avg_poly(xmonths))

    # Number of Trips Monthly per Gender
    ax1[1, 0].scatter(months, o19cnt, color='indigo', label='2019 Other/Unknown')
    ax1[1, 0].scatter(months11, o20cnt[0:11], color='forestgreen', label='2020 Other/Unknown')
    ax1[1, 0].scatter(months, m19cnt, color='blue', label='2019 Male')
    ax1[1, 0].scatter(months11, m20cnt[0:11], color='orange', label='2020 Male')
    ax1[1, 0].scatter(months, f19cnt, color='coral', label='2019 Female')
    ax1[1, 0].scatter(months11, f20cnt[0:11], color='teal', label='2020 Female')
    ax1[1, 0].set_title(gen_title_frq, weight='bold')
    ax1[1, 0].set_xlabel(x_lab)
    ax1[1, 0].set_ylabel(y_lab_frq)
    ax1[1, 0].grid(ls='--')
    ax1[1, 0].legend()
    o19cnt_poly = np.poly1d(np.polyfit(xmonths, o19cnt, 3))
    o20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], o20cnt[0:11], 3))
    ax1[1, 0].plot(xmonths, o19cnt_poly(xmonths), color='indigo')
    ax1[1, 0].plot(xmonths, o20cnt_poly(xmonths), color='forestgreen')
    m19cnt_poly = np.poly1d(np.polyfit(xmonths, m19cnt, 3))
    m20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], m20cnt[0:11], 3))
    ax1[1, 0].plot(xmonths, m19cnt_poly(xmonths), color='blue')
    ax1[1, 0].plot(xmonths, m20cnt_poly(xmonths), color='orange')
    f19cnt_poly = np.poly1d(np.polyfit(xmonths, f19cnt, 3))
    f20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], f20cnt[0:11], 3))
    ax1[1, 0].plot(xmonths, f19cnt_poly(xmonths), color='coral')
    ax1[1, 0].plot(xmonths, f20cnt_poly(xmonths), color='teal')

    # Average Monthly Trip Duration per Gender
    ax1[1, 1].scatter(months, o19avg, color='indigo', label='2019 Other/Unknown')
    ax1[1, 1].scatter(months, o20avg, color='forestgreen', label='2020 Other/Unknown')
    ax1[1, 1].scatter(months, m19avg, color='blue', label='2019 Male')
    ax1[1, 1].scatter(months, m20avg, color='orange', label='2020 Male')
    ax1[1, 1].scatter(months, f19avg, color='coral', label='2019 Female')
    ax1[1, 1].scatter(months, f20avg, color='teal', label='2020 Female')
    ax1[1, 1].set_title(gen_title_avg, weight='bold')
    ax1[1, 1].set_xlabel(x_lab)
    ax1[1, 1].set_ylabel(y_lab_avg)
    ax1[1, 1].grid(ls='--')
    ax1[1, 1].legend()
    o19avg_poly = np.poly1d(np.polyfit(xmonths, o19avg, 3))
    o20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], o20avg[0:11], 3))
    ax1[1, 1].plot(xmonths, o19avg_poly(xmonths), color='indigo')
    ax1[1, 1].plot(xmonths, o20avg_poly(xmonths), color='forestgreen')
    m19avg_poly = np.poly1d(np.polyfit(xmonths, m19avg, 3))
    m20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], m20avg[0:11], 3))
    ax1[1, 1].plot(xmonths, m19avg_poly(xmonths), color='blue')
    ax1[1, 1].plot(xmonths, m20avg_poly(xmonths), color='orange')
    f19avg_poly = np.poly1d(np.polyfit(xmonths, f19avg, 3))
    f20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], f20avg[0:11], 3))
    ax1[1, 1].plot(xmonths, f19avg_poly(xmonths), color='coral')
    ax1[1, 1].plot(xmonths, f20avg_poly(xmonths), color='teal')

    # Number of Trips Monthly per User Type
    ax1[2, 0].scatter(months, cus19cnt, color='blue', label='2019 Customers')
    ax1[2, 0].scatter(months11, cus20cnt[0:11], color='orange', label='2020 Customers')
    ax1[2, 0].scatter(months, sub19cnt, color='indigo', label='2019 Subscribers')
    ax1[2, 0].scatter(months11, sub20cnt[0:11], color='teal', label='2020 Subscribers')
    ax1[2, 0].set_title(user_title_frq, weight='bold')
    ax1[2, 0].set_xlabel(x_lab)
    ax1[2, 0].set_ylabel(y_lab_frq)
    ax1[2, 0].grid(ls='--')
    ax1[2, 0].legend()
    cus19cnt_poly = np.poly1d(np.polyfit(xmonths, cus19cnt, 3))
    cus20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], cus20cnt[0:11], 3))
    ax1[2, 0].plot(xmonths, cus19cnt_poly(xmonths), color='blue')
    ax1[2, 0].plot(xmonths, cus20cnt_poly(xmonths), color='orange')
    sub19cnt_poly = np.poly1d(np.polyfit(xmonths, sub19cnt, 3))
    sub20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], sub20cnt[0:11], 3))
    ax1[2, 0].plot(xmonths, sub19cnt_poly(xmonths), color='indigo')
    ax1[2, 0].plot(xmonths, sub20cnt_poly(xmonths), color='teal')

    # Average Monthly Trip Duration per User Type
    ax1[2, 1].scatter(months, cus19avg, color='blue', label='2019 Customers')
    ax1[2, 1].scatter(months, cus20avg, color='orange', label='2020 Customers')
    ax1[2, 1].scatter(months, sub19avg, color='indigo', label='2019 Subscribers')
    ax1[2, 1].scatter(months, sub20avg, color='teal', label='2020 Subscribers')
    ax1[2, 1].set_title(user_title_avg, weight='bold')
    ax1[2, 1].set_xlabel(x_lab)
    ax1[2, 1].set_ylabel(y_lab_avg)
    ax1[2, 1].grid(ls='--')
    ax1[2, 1].legend()
    cus19avg_poly = np.poly1d(np.polyfit(xmonths, cus19avg, 3))
    cus20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], cus20avg[0:11], 3))
    ax1[2, 1].plot(xmonths, cus19avg_poly(xmonths), color='blue')
    ax1[2, 1].plot(xmonths, cus20avg_poly(xmonths), color='orange')
    sub19avg_poly = np.poly1d(np.polyfit(xmonths, sub19avg, 3))
    sub20avg_poly = np.poly1d(np.polyfit(xmonths[0:11], sub20avg[0:11], 3))
    ax1[2, 1].plot(xmonths, sub19avg_poly(xmonths), color='indigo')
    ax1[2, 1].plot(xmonths, sub20avg_poly(xmonths), color='teal')

    # Display
    fig.tight_layout()

    plt.show()

    # --- REGRESSION LINES: PARTIAL 2020 MODEL -------------------------
    '''Looking at the 2020 data points, one might point out that the data for the
    months of March to June are unusual compared to the trend of the other months
    and to the previous year's data. If they are considered anomalies, or perhaps
    outliers as well, then another set of regression models can be derived that only
    consider January, February, and July to November.
    '''
    xmn_part = xmonths[0:2] + xmonths[6:11]
    ovr20cnt_part = ovr20cnt[0:2] + ovr20cnt[6:11]
    ovr20avg_part = ovr20avg[0:2] + ovr20avg[6:11]
    o20cnt_part = o20cnt[0:2] + o20cnt[6:11]
    o20avg_part = o20avg[0:2] + o20avg[6:11]
    m20cnt_part = m20cnt[0:2] + m20cnt[6:11]
    m20avg_part = m20avg[0:2] + m20avg[6:11]
    f20cnt_part = f20cnt[0:2] + f20cnt[6:11]
    f20avg_part = f20avg[0:2] + f20avg[6:11]
    cus20cnt_part = cus20cnt[0:2] + cus20cnt[6:11]
    cus20avg_part = cus20avg[0:2] + cus20avg[6:11]
    sub20cnt_part = sub20cnt[0:2] + sub20cnt[6:11]
    sub20avg_part = sub20avg[0:2] + sub20avg[6:11]
    fig, ax2 = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))

    # Overall Number of Trips Monthly
    ax2[0, 0].scatter(months, ovr19cnt, label='2019')
    ax2[0, 0].scatter(months11, ovr20cnt[0:11], label='2020')
    ax2[0, 0].set_title(ovr_title_frq, weight='bold')
    ax2[0, 0].set_xlabel(x_lab)
    ax2[0, 0].set_ylabel(y_lab_frq)
    ax2[0, 0].grid(ls='--')
    ax2[0, 0].legend()
    ovr19cnt_poly = np.poly1d(np.polyfit(xmonths, ovr19cnt, 3))
    ovr20cnt_polypt = np.poly1d(np.polyfit(xmn_part, ovr20cnt_part, 3))
    ax2[0, 0].plot(xmonths, ovr19cnt_poly(xmonths))
    ax2[0, 0].plot(xmonths, ovr20cnt_poly(xmonths))

    # Overall Average Monthly Trip Duration
    ax2[0, 1].scatter(months, ovr19avg, label='2019')
    ax2[0, 1].scatter(months, ovr20avg, label='2020')
    ax2[0, 1].set_title(ovr_title_avg, weight='bold')
    ax2[0, 1].set_xlabel(x_lab)
    ax2[0, 1].set_ylabel(y_lab_avg)
    ax2[0, 1].grid(ls='--')
    ax2[0, 1].legend()
    ovr19avg_poly = np.poly1d(np.polyfit(xmonths, ovr19avg, 3))
    ovr20avg_polypt = np.poly1d(np.polyfit(xmn_part, ovr20avg_part, 3))
    ax2[0, 1].plot(xmonths, ovr19avg_poly(xmonths))
    ax2[0, 1].plot(xmonths, ovr20avg_poly(xmonths))

    # Number of Trips Monthly per Gender
    ax2[1, 0].scatter(months, o19cnt, color='indigo', label='2019 Other/Unknown')
    ax2[1, 0].scatter(months11, o20cnt[0:11], color='forestgreen', label='2020 Other/Unknown')
    ax2[1, 0].scatter(months, m19cnt, color='blue', label='2019 Male')
    ax2[1, 0].scatter(months11, m20cnt[0:11], color='orange', label='2020 Male')
    ax2[1, 0].scatter(months, f19cnt, color='coral', label='2019 Female')
    ax2[1, 0].scatter(months11, f20cnt[0:11], color='teal', label='2020 Female')
    ax2[1, 0].set_title(gen_title_frq, weight='bold')
    ax2[1, 0].set_xlabel(x_lab)
    ax2[1, 0].set_ylabel(y_lab_frq)
    ax2[1, 0].grid(ls='--')
    ax2[1, 0].legend()
    o19cnt_poly = np.poly1d(np.polyfit(xmonths, o19cnt, 3))
    o20cnt_polypt = np.poly1d(np.polyfit(xmn_part, o20cnt_part, 3))
    ax2[1, 0].plot(xmonths, o19cnt_poly(xmonths), color='indigo')
    ax2[1, 0].plot(xmonths, o20cnt_poly(xmonths), color='forestgreen')
    m19cnt_poly = np.poly1d(np.polyfit(xmonths, m19cnt, 3))
    m20cnt_polypt = np.poly1d(np.polyfit(xmn_part, m20cnt_part, 3))
    ax2[1, 0].plot(xmonths, m19cnt_poly(xmonths), color='blue')
    ax2[1, 0].plot(xmonths, m20cnt_poly(xmonths), color='orange')
    f19cnt_poly = np.poly1d(np.polyfit(xmonths, f19cnt, 3))
    f20cnt_polypt = np.poly1d(np.polyfit(xmn_part, f20cnt_part, 3))
    ax2[1, 0].plot(xmonths, f19cnt_poly(xmonths), color='coral')
    ax2[1, 0].plot(xmonths, f20cnt_poly(xmonths), color='teal')

    # Average Monthly Trip Duration per Gender
    ax2[1, 1].scatter(months, o19avg, color='indigo', label='2019 Other/Unknown')
    ax2[1, 1].scatter(months, o20avg, color='forestgreen', label='2020 Other/Unknown')
    ax2[1, 1].scatter(months, m19avg, color='blue', label='2019 Male')
    ax2[1, 1].scatter(months, m20avg, color='orange', label='2020 Male')
    ax2[1, 1].scatter(months, f19avg, color='coral', label='2019 Female')
    ax2[1, 1].scatter(months, f20avg, color='teal', label='2020 Female')
    ax2[1, 1].set_title(gen_title_avg, weight='bold')
    ax2[1, 1].set_xlabel(x_lab)
    ax2[1, 1].set_ylabel(y_lab_avg)
    ax2[1, 1].grid(ls='--')
    ax2[1, 1].legend()
    o19avg_poly = np.poly1d(np.polyfit(xmonths, o19avg, 3))
    o20avg_polypt = np.poly1d(np.polyfit(xmn_part, o20avg_part, 3))
    ax2[1, 1].plot(xmonths, o19avg_poly(xmonths), color='indigo')
    ax2[1, 1].plot(xmonths, o20avg_poly(xmonths), color='forestgreen')
    m19avg_poly = np.poly1d(np.polyfit(xmonths, m19avg, 3))
    m20avg_polypt = np.poly1d(np.polyfit(xmn_part, m20avg_part, 3))
    ax2[1, 1].plot(xmonths, m19avg_poly(xmonths), color='blue')
    ax2[1, 1].plot(xmonths, m20avg_poly(xmonths), color='orange')
    f19avg_poly = np.poly1d(np.polyfit(xmonths, f19avg, 3))
    f20avg_polypt = np.poly1d(np.polyfit(xmn_part, f20avg_part, 3))
    ax2[1, 1].plot(xmonths, f19avg_poly(xmonths), color='coral')
    ax2[1, 1].plot(xmonths, f20avg_poly(xmonths), color='teal')

    # Number of Trips Monthly per User Type
    ax2[2, 0].scatter(months, cus19cnt, color='blue', label='2019 Customers')
    ax2[2, 0].scatter(months11, cus20cnt[0:11], color='orange', label='2020 Customers')
    ax2[2, 0].scatter(months, sub19cnt, color='indigo', label='2019 Subscribers')
    ax2[2, 0].scatter(months11, sub20cnt[0:11], color='teal', label='2020 Subscribers')
    ax2[2, 0].set_title(user_title_frq, weight='bold')
    ax2[2, 0].set_xlabel(x_lab)
    ax2[2, 0].set_ylabel(y_lab_frq)
    ax2[2, 0].grid(ls='--')
    ax2[2, 0].legend()
    cus19cnt_poly = np.poly1d(np.polyfit(xmonths, cus19cnt, 3))
    cus20cnt_polypt = np.poly1d(np.polyfit(xmn_part, cus20cnt_part, 3))
    ax2[2, 0].plot(xmonths, cus19cnt_poly(xmonths), color='blue')
    ax2[2, 0].plot(xmonths, cus20cnt_poly(xmonths), color='orange')
    sub19cnt_poly = np.poly1d(np.polyfit(xmonths, sub19cnt, 3))
    sub20cnt_polypt = np.poly1d(np.polyfit(xmn_part, sub20cnt_part, 3))
    ax2[2, 0].plot(xmonths, sub19cnt_poly(xmonths), color='indigo')
    ax2[2, 0].plot(xmonths, sub20cnt_poly(xmonths), color='teal')

    # Average Monthly Trip Duration per User Type
    ax2[2, 1].scatter(months, cus19avg, color='blue', label='2019 Customers')
    ax2[2, 1].scatter(months, cus20avg, color='orange', label='2020 Customers')
    ax2[2, 1].scatter(months, sub19avg, color='indigo', label='2019 Subscribers')
    ax2[2, 1].scatter(months, sub20avg, color='teal', label='2020 Subscribers')
    ax2[2, 1].set_title(user_title_avg, weight='bold')
    ax2[2, 1].set_xlabel(x_lab)
    ax2[2, 1].set_ylabel(y_lab_avg)
    ax2[2, 1].grid(ls='--')
    ax2[2, 1].legend()
    cus19avg_poly = np.poly1d(np.polyfit(xmonths, cus19avg, 3))
    cus20avg_polypt = np.poly1d(np.polyfit(xmn_part, cus20avg_part, 3))
    ax2[2, 1].plot(xmonths, cus19avg_poly(xmonths), color='blue')
    ax2[2, 1].plot(xmonths, cus20avg_poly(xmonths), color='orange')
    sub19avg_poly = np.poly1d(np.polyfit(xmonths, sub19avg, 3))
    sub20avg_polypt = np.poly1d(np.polyfit(xmn_part, sub20avg_part, 3))
    ax2[2, 1].plot(xmonths, sub19avg_poly(xmonths), color='indigo')
    ax2[2, 1].plot(xmonths, sub20avg_poly(xmonths), color='teal')

    # Display
    fig.tight_layout()

    plt.show()

# --- DECEMBER 2020 PREDICTIONS TABLE  -----------------------

def preds(month):
  full2020 = [ovr20cnt_poly(month), o20cnt_poly(month), m20cnt_poly(month), f20cnt_poly(month),
              cus20cnt_poly(month), sub20cnt_poly(month), ovr20avg_poly(month), o20avg_poly(month),
              m20avg_poly(month), f20avg_poly(month), cus20avg_poly(month), sub20avg_poly(month)]
  part2020 = [ovr20cnt_polypt(month), o20cnt_polypt(month), m20cnt_polypt(month), f20cnt_polypt(month),
              cus20cnt_polypt(month), sub20cnt_polypt(month), ovr20avg_polypt(month), o20avg_polypt(month),
              m20avg_polypt(month), f20avg_polypt(month), cus20avg_polypt(month), sub20avg_polypt(month)]
  preds_summary = pd.DataFrame({"Full 2020": full2020, "Partial 2020": part2020})
  pd.options.display.float_format = '{:.2f}'.format
  preds_summary.index = ["Overall Number of Trips", "Number of Trips by Riders of Other/Unknown Gender",
                       "Number of Trips by Male Riders", "Number of Trips by Female Riders",
                       "Number of Trips by Customers", "Number of Trips by Subscribers",
                       "Overall Average Trip Duration (min)", "Average Trip Duration of Riders of Other/Unknown Gender (min)",
                       "Average Trip Duration of Male Riders (min)", "Average Trip Duration of Female Riders (min)",
                       "Average Trip Duration of Customers (min)", "Average Trip Duration of Subscribers (min)"]
  return preds_summary

def overlord():
    program_proper()
    print(preds(11))

overlord()

# The original code from Colab with minor changes took around 3 minutes to run. 
# The code as it is now with the suggested changes takes 10-12 minutes to run, with less consistency in execution.
