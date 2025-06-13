import pandas as pd
import plotly.graph_objects as go
from participant_dataloader import load_data

def plot_demographic_sankey(filepath="results_combined/Batch1ResultsAll.txt"):
    """
    Generates and shows a Sankey diagram of participant demographics.
    """
    df = load_data(filepath)

    # Ensure no missing values in required columns
    df = df.dropna(subset=["gender", "age_bracket", "education", "ai_familiarity"])

    # Define the columns to visualize
    cols = ["gender", "age_bracket", "education", "ai_familiarity"]

    # Build label list and mapping
    label_list = []
    for col in cols:
        label_list.extend(df[col].unique())
    labels = list(pd.unique(label_list))
    label_to_index = {label: i for i, label in enumerate(labels)}

    # Generate source-target-value triplets
    source, target, value = [], [], []
    for i in range(len(cols) - 1):
        grouped = df.groupby([cols[i], cols[i+1]]).size().reset_index(name='count')
        for _, row in grouped.iterrows():
            source.append(label_to_index[row[cols[i]]])
            target.append(label_to_index[row[cols[i+1]]])
            value.append(row['count'])

    # Build Sankey figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    )])

    fig.update_layout(title_text="Demographic Flow of Participants", font_size=10)
    fig.show()