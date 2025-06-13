import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('time.csv', header=None)

# Get row identifiers (the first column)
row_ids = df[0].values

# Get only the data values
data = df.iloc[:, 1:].values
print(data)

# Calculate row-wise statistics
means = data.mean(axis=1)
print(means)

# Find row with mean closest to 3
target_mean = 3
mean_diffs = np.abs(means - target_mean)
closest_mean_idx = np.argmin(mean_diffs)
closest_mean_row = df.iloc[closest_mean_idx]

# Output results
print("Row with mean closest to 3:")
print(closest_mean_row.values)
