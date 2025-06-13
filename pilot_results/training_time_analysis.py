import plotly.express as px
from participant_dataloader import load_data

# Load the data
df = load_data("results.txt")

# Calculate training time in milliseconds
df['training_time'] = df['questions_start'] - df['demographics_end']

# Convert to minutes
df['training_time_minutes'] = df['training_time'] / 60000  # 60,000 ms in a minute

# Add a participant index for plotting (assuming each row is one participant)
df['participant'] = range(1, len(df) + 1)

# Create scatter plot
fig = px.scatter(
    df,
    x="participant",
    y="training_time_minutes",
    labels={
        "participant": "Participant",
        "training_time_minutes": "Training Time (minutes)"
    },
    title="Training Time per Participant",
)

fig.show()
