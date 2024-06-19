import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('results-drift.csv')

# Pivot the DataFrame to get devices as columns, intervals as index, and drift as values
pivot_df = df.pivot(index='device', columns='interval', values='drift')

# Plot the grouped bar chart
pivot_df.plot(kind='bar', figsize=(10, 6))

# Add labels and title
plt.xlabel('Interval')
plt.ylabel('Drift')
plt.title('Drift by Device and Interval')
plt.xticks(rotation=45)


# Show the plot
plt.legend(title='Device')
plt.savefig('drifts.svg')