import pandas as pd
import matplotlib.pyplot as plt

# Load CSV data (no header)
df = pd.read_csv('time.csv', header=None)

# First column is x-axis values
x_values = df[0].values

# Rest are the data for boxplots
data_rows = df.iloc[:, 1:].values

plt.figure(figsize=(12, 6))

# Plot each row as a separate boxplot at its x-position
for i, (x, row_data) in enumerate(zip(x_values, data_rows)):
    plt.boxplot(row_data, positions=[x], widths=100)

# Set labels and title
plt.xlabel('X values')
plt.ylabel('Data values')
plt.title('Boxplot for Each Row at Corresponding X Value')
plt.grid(True)
plt.show()
