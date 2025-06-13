import json
import pandas as pd
import plotly.express as px
from participant_dataloader import load_data

# Load data
df = load_data("results.txt")

# Print the first few rows of the DataFrame
print(df)

# Calculate the mean of the 'helpful', 'confidence', and 'coverage' columns
mean_values = df[['helpful', 'confidence', 'coverage']].mean()

# Print the mean values
print("Mean values for helpful, confidence, and coverage:")
print(mean_values)
