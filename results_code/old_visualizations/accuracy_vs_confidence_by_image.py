import plotly.express as px
import pandas as pd
from dataloader import load_data

def plot_confidence_vs_accuracy_plotly(filepath="results_combined/Batch1ResultsAll.txt"):
    # Load the data
    df = load_data(filepath)
    
    # Make sure 'confidence' is numeric
    df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')

    grouped = df.groupby("image").agg({
        "trust_correct": "mean",
        "confidence": "mean"
    }).reset_index()

    fig = px.scatter(
        grouped,
        x="confidence",
        y="trust_correct",
        color="image",
        text="image",
        labels={
            "confidence": "Mean Confidence (1–5)",
            "trust_correct": "Accuracy (Proportion Correct)",
        },
        title="Confidence vs. Accuracy by Image",
    )

    # Customize marker size and text position
    fig.update_traces(marker=dict(size=10), textposition='top center')

    # Axes limits
    fig.update_layout(
        xaxis=dict(range=[0, 5]),
        yaxis=dict(range=[0, 1]),
        showlegend=False,  # Hide legend if too cluttered
        plot_bgcolor='white'
    )

    fig.show()
