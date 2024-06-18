#!/bin/python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import dates


# Function to convert epoch to datetime
def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)


def load_data(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file, sep=' ')
    #, names=['timestamp', 'hostname', 'srvname', 'delta', 'error']
    # Convert the timestamp to datetime
    df['timestamp'] = df['timestamp'].apply(pd.to_numeric).apply(epoch_to_datetime)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')
    return df


def plot(df, ax, out_file):
    # if df.iloc[0]['clientname'] == 'raspi':
    #     df['delta'] = df['delta'] - 2174

    # Plotting the time series
    ax.errorbar(df['timestamp'], df['delta'], yerr=df['delta_prec'], ecolor='red', capsize=2, label=df.iloc[0]['clientname'])

if sys.argv[1] == '-h':
    print('usage: plots_combined.py csv1 csv2 ... output_image')

dfs = []
fig,ax = plt.subplots(figsize=(14,8))
for x in range(1, len(sys.argv)-1):
    plot(load_data(sys.argv[x]), ax, '')

# Show the plot
plt.xlabel('Time')
plt.ylabel('Delta')
plt.title('Time Series of Delta with Error Bars')
plt.legend()
plt.grid(True)

# generate a formatter, using the fields required
fmtr = dates.DateFormatter("%H:%M")
# need a handle to the current axes to manipulate it
ax = plt.gca()
# set this formatter to the axis
ax.xaxis.set_major_formatter(fmtr)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(sys.argv[len(sys.argv)-1])
#
# df_combined = pd.merge(df_demon, df_raspi, left_on='closest_timestamp_raspi', right_on='timestamp_raspi')
# df_combined.info()
# # Add the values
# df_combined['timestamp'] = df_combined['timestamp_x']
# df_combined['delta'] = df_combined['delta_x'] + df_combined['delta_y']
# df_combined['delta_prec'] = df_combined['delta_prec_x'] + df_combined['delta_prec_y']
# plot(df_combined, sys.argv[len(sys.argv)-1])
# given n timeseries, get lstart=max(first-timestamp), get for all others the largest timestamp before lstart
# add r,a: for each x value of a get closest value of r, add corresponding rows -> out dimension same as dim(a)