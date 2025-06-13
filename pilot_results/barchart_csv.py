import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv('time.csv', header=None)

# Extract x-axis values
x_values = df[0].values

# Extract data (excluding the first column)
data = df.iloc[:, 1:].values

# Compute mean and median for each row
means = data.mean(axis=1)
medians = np.median(data, axis=1)

# Create the plot
plt.figure(figsize=(12, 6))

# Plot bar chart for means
plt.bar(x_values, means, width=300, label='Mean', color='skyblue')

# Plot line chart for medians
plt.plot(x_values, medians, marker='o', color='orange', linewidth=2, label='Median')

# Labels and legend
plt.xlabel('X values')
plt.ylabel('Value')
plt.title('Mean and Median of Each Row')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
