import sys

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Function to convert epoch to datetime
def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)


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


df_demon=load_data(sys.argv[1])

plot(df_demon, sys.argv[2])

# given n timeseries, get lstart=max(first-timestamp), get for all others the largest timestamp before lstart
# add r,a: for each x value of a get closest value of r, add corresponding rows -> out dimension same as dim(a)