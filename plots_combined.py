#!/bin/python3

import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime
from matplotlib import dates
import argparse


font_size = 14
plt.rc('font', size=font_size)
plt.rc('axes', titlesize=font_size)
plt.tick_params(labelsize=font_size)

# Function to convert epoch to datetime
def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(epoch)

def load_data(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file, sep=' ')
    #, names=['timestamp', 'hostname', 'srvname', 'delta', 'error']
    # Convert the timestamp to datetime
    df['timestamp'] = df['timestamp'].apply(pd.to_numeric).apply(epoch_to_datetime)
    
    # TODO why is this required?
    #df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')
    return df

def find_closest(row, reference_table, r_timestamps):
    closest_idx = (r_timestamps - row['timestamp']).abs().idxmin()
    return reference_table.loc[closest_idx, 'timestamp_ref']


def merge_adjust(base, df):
    pass


def plot(df, ax, out_file):
    # if df.iloc[0]['clientname'] == 'raspi':
    #     df['delta'] = df['delta'] - 2174

    # Plotting the time series
    #ax.errorbar(df['timestamp'], df['delta'], yerr=df['delta_prec'], ecolor='red', capsize=2, fmt='o', markersize=1, label=df.iloc[0]['clientname'])
    ax.plot(df['timestamp'], df['delta'], 'o', markersize=1, label=df.iloc[0]['clientname'])

parser = argparse.ArgumentParser(description="Make the plots")
    
parser.add_argument('--ref', type=str, help='Reference time series')
parser.add_argument('--output', type=str, required=True, help='output file')
parser.add_argument('inputs', nargs='+', type=str, help='input .csv files')
parser.add_argument('--t0', action="store_true", help='start from t0=0')
parser.add_argument('--ref_t0', nargs='?', type=int, help='if set, offset reference time series by this rows value')
parser.add_argument('--no_ref_for', nargs='*', type=str, help='don\'t adjust these with reference time')
parser.add_argument('--markers', nargs='?', type=str)

args = parser.parse_args()
ref = args.ref
t0 = args.t0
output = args.output
inputs = args.inputs
markers = args.markers
no_ref_for= () if args.no_ref_for is None else args.no_ref_for

dfs=[]
fig,ax = plt.subplots(figsize=(14,8))
if ref is not None:
    try:
        inputs.remove(ref)
    except ValueError: pass

    ref = load_data(ref)
    plot(ref, ax, '')
    ref['timestamp_ref'] = ref['timestamp']
    del ref['timestamp']

for infile in inputs:
    df = load_data(infile)
    if ref is not None and infile not in no_ref_for:
        df['closest_timestamp_ref'] = df.apply(find_closest, axis=1, reference_table=ref, r_timestamps=ref['timestamp_ref'])
        df = pd.merge(df, ref, left_on='closest_timestamp_ref', right_on='timestamp_ref', suffixes=('', '_ref'))
        df['delta'] = df['delta'] + df['delta_ref']
    if t0:
        delta_t0 = df['delta'].iloc[0]
        df['delta'] = df['delta'] - delta_t0
    dfs.append(df)

    plot(df, ax, '')
if markers:
    last_sep=None
    with open(markers, 'r') as f:
        for m in f:
            m=m.strip().split(', ')
            x=datetime.strptime(m[0], "%Y-%m-%d %H:%M")
            ax.axvline(x=x, linestyle='--', label=m[1])
            df_i = df.copy()
            if last_sep is None:
                df_i = df_i[df_i['timestamp'] < x]
                #print("1",df_i.empty)
            else:
                #print(f"(row['timestamp'] >= {last_sep}) & (row['timestamp'] < {x})")
                df_i = df_i[df_i['timestamp'] >= last_sep]
                df_i = df_i[df_i['timestamp'] < x]
                #print("2",df_i.empty)
            last_sep = x
            k, d, r_val, p_val, std_err = linregress(df_i['timestamp'].apply(lambda d: d.timestamp()), df_i['delta'])
            print(k)
    #intervals.append(lambda row: row['timestamp'] > last_sep)
    df_i = df.copy()
    df_i = df_i[df_i['timestamp'] > last_sep]
    #print("3",df_i.empty)
    if not df_i.empty:
        k, d, r_val, p_val, std_err = linregress(df_i['timestamp'].apply(lambda d: d.timestamp()), df_i['delta'])
        print(k)
for df in dfs:
    print(df.iloc[0]['clientname'])
    print("---")
    k, d, r_val, p_val, std_err = linregress(df['timestamp'].apply(lambda d: d.timestamp()), df['delta'])
    print("overall ", k)

# Show the plot
plt.xlabel('Zeit', fontsize=font_size)
plt.ylabel('Delta', fontsize=font_size)
plt.title('Drift von Geräten')
plt.legend()
plt.grid(True)

# generate a formatter, using the fields required
#fmtr = dates.DateFormatter("%H:%M")
# need a handle to the current axes to manipulate it
#ax = plt.gca()
# set this formatter to the axis
#ax.xaxis.set_major_formatter(fmtr)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output)
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