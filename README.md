# CitiBike Data Analysis for Impact of COVID-19 on Trip Duration and Frequency

---

Given a CitiBike data file, this program calculates the monthly number of trips and average monthly duration for the overall population, as well as for different genders, user types, and age brackets. These calculations are presented in various graphs and plots. From these calculations, simple polynomial regression models are created, from which predictions for December 2020 can be made.

Assumptions:
* The provided data is an appropriate CitiBike data file (Using iris.csv or Salaries.csv, for example, will raise errors).

Initial Inputs (Setup):
* Monthly CitiBike data files for each desired year

Initial Output/Proper Input:
* combined, CitiBike data file with sample of total data per month

Outputs:
* graphs and plots of monthly number of trips and average monthly duration for each (sub)category
* tabulated predictions for December 2020

---

## Setup

This repository must be cloned or downloaded in order for the program to be used.
A virtual environment should then be created and activated.

```
$ python3 -m venv venv
```

```
For Linux/Mac OS:
$ source venv/bin/activate

For Windows:
> venv\Scripts\activate
```

To finish setting up the virtual environment, the required library versions need to be installed.

```
$ pip install -r requirements.txt
```

---

## How to use the program

Before any calculations or analysis can be done, the data files need to be manipulated. Given the sheer size of each file, it would be unwieldy and inefficient to use them at face value. From a statistical analysis standpoint, having so much data could lead to overfitting, which in turn could make the regression models too specific to be very useful.

First, each data file is run through the data reduction function. Before a sample is taken, outliers and data columns deemed unnecessary for this program are removed. The function takes a 20% sample, which is big enough to still be statistically significant but small enough to still be efficient and applicable. Once a sample is taken, it is checked to see if it still statistically resembles the entire dataset closely enough; if not, samples are continuously checked until one meets the aforementioned requirements.

```python
>>> jan19 = csv_redux('201901-citibike-tripdata.csv')
```

All of the reduced data files are then concatenated into one master dataset and converted into a csv file, which can then be used in the program proper.

```python
>>> comb = pd.concat([jan19, feb19, mar19, apr19, may19, jun19, jul19, aug19, sep19,
                  oct19, nov19, dec19, jan20, feb20, mar20, apr20, may20, jun20, 
                  jul20, aug20, sep20, oct20, nov20])
>>> comb.to_csv('masterdata.csv')
```

For the overall dataset, as well as for each sub-categorization, the following was done: (Here, the process for the overall dataset is shown.)

First, the monthly figures for number of trips and average trip duration are calculated. The results of this are then broken down per year for graphing/plotting purposes.

```python
>>> ovr = overall([2019, 2020])
>>> ovr19cnt, ovr20cnt = ovr[0][:]
>>> ovr19avg, ovr20avg = ovr[1][:]
```

The graphs and plots are created from the calculated data. Below is one example of a line plot and a bar graph each.

```python
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

# Titles
ovr_title_frq = 'Overall CitiBike Trips per Month'
ovr_title_avg = 'Overall Average Monthly CitiBike Trip Duration'

# Line plot
ax[0, 0].plot(months, ovr19cnt, label='2019')
ax[0, 0].plot(months11, ovr20cnt[0:11], label='2020')
ax[0, 0].set_title(ovr_title_frq, weight='bold')
ax[0, 0].set_xlabel(x_lab)
ax[0, 0].set_ylabel(y_lab_frq)
ax[0, 0].grid(ls='--')
ax[0, 0].legend()

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

# Display
fig.tight_layout()

plt.show()
```

This process is repeated for the following breakdowns: by gender, by user type, and by age bracket.

Finally the regression models for each line plot are created and graphed, of which there were two regression models: full 2020 and partial 2020. The below example shows the full 2020 regression model for the overall number of trips monthly.

```python
fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(15, 15))

# Overall Number of Trips Monthly
ax[0, 0].scatter(months, ovr19cnt, label='2019')
ax[0, 0].scatter(months11, ovr20cnt[0:11], label='2020')
ax[0, 0].set_title(ovr_title_frq, weight='bold')
ax[0, 0].set_xlabel(x_lab)
ax[0, 0].set_ylabel(y_lab_frq)
ax[0, 0].grid(ls='--')
ax[0, 0].legend()
ovr19cnt_poly = np.poly1d(np.polyfit(xmonths, ovr19cnt, 3))
ovr20cnt_poly = np.poly1d(np.polyfit(xmonths[0:11], ovr20cnt[0:11], 3))
ax[0, 0].plot(xmonths, ovr19cnt_poly(xmonths))
ax[0, 0].plot(xmonths, ovr20cnt_poly(xmonths))
```

