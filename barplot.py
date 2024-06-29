import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('results-drift.csv')
df['drift'] = df['drift'] * 10 ** 6

# Pivot the DataFrame to get devices as columns, intervals as index, and drift as values
pivot_df = df.pivot(index='device', columns='interval', values='drift')

# Plot the grouped bar chart
pivot_df.plot(kind='bar', figsize=(10, 6))

# Add labels and title
font_size = 14
plt.rc('font', size=font_size)
plt.rc('axes', titlesize=font_size)
plt.tick_params(labelsize=font_size)
plt.xlabel('Interval bei Gerät', fontsize=font_size)
plt.ylabel('Drift (ppm)', fontsize=font_size)
plt.title('Drift von Geräten bei Intervall')
plt.xticks(rotation=0)


# Show the plot
plt.legend(title='Intervall')
plt.savefig('drifts.png')