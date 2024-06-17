import sys

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Function to convert epoch to datetime
def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)


def find_closest(row, r_timestamps):
    closest_idx = (r_timestamps - row['timestamp_demon']).abs().idxmin()
    return df_raspi.loc[closest_idx, 'timestamp_raspi']


def load_data(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file, sep=' ')
    #, names=['timestamp', 'hostname', 'srvname', 'delta', 'error']
    # Convert the timestamp to datetime
    df['timestamp'] = df['timestamp'].apply(pd.to_numeric).apply(epoch_to_datetime)
    return df


def plot(df, out_file):

    # Plotting the time series
    plt.figure(figsize=(10, 6))
    plt.errorbar(df['timestamp'], df['delta'], yerr=df['delta_prec'], ecolor='red', capsize=2, label='Delta with error')
    plt.xlabel('Time')
    plt.ylabel('Delta')
    plt.title('Time Series of Delta with Error Bars')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.savefig(out_file)

dfs = []
for x in range(1, len(sys.argv)-1):
    dfs.append(load_data(x))
#
# df_demon['closest_timestamp_raspi'] = df_demon.apply(find_closest, axis=1, r_timestamps=df_raspi['timestamp_raspi'])
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