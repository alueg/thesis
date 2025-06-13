import pandas as pd
import plotly.express as px
from dataloader import load_data  

# Function to classify trust mismatch categories
def identify_trust_mismatch_detailed(row):
    if row['trust'] == "Yes" and row['trust_correct'] == False:
        return "Overtrust", None
    elif row['trust'] == "No" and row['trust_correct'] == False:
        return "Undertrust", None
    elif row['trust'] == "Yes" and row['correct_response'] == "Yes":
        return "Appropriate", "Trust Yes, Correct"
    elif row['trust'] == "No" and row['correct_response'] == "No":
        return "Appropriate", "Trust No, Correct"
    else:
        return "Appropriate", "Other"

# Generic function for pie chart plotting
def plot_trust_pie_by_facet(facet_col, title_label, filepath="data/results.txt"):
    # Load data
    df = load_data(filepath)

    # Apply classification
    df[['trust_mismatch', 'appropriate_detail']] = df.apply(lambda row: pd.Series(identify_trust_mismatch_detailed(row)), axis=1)

    # Drop rows with missing trust mismatch categories or facet_col
    df = df.dropna(subset=["trust_mismatch", facet_col])

    # Count occurrences
    trust_mismatch_counts = df.groupby([facet_col, 'trust_mismatch']).size().reset_index(name="Count")

    # Plot pie chart
    fig = px.pie(
        trust_mismatch_counts,
        values='Count', names='trust_mismatch',
        title=f"Proportion of Overtrust, Undertrust, and Appropriate Trust by {title_label}",
        color='trust_mismatch',
        color_discrete_map={'Overtrust': '#ff9999', 'Undertrust': '#66b3ff', 'Appropriate': '#66ff66'},
        facet_col=facet_col, facet_col_wrap=2,
        category_orders={"trust_mismatch": ['Overtrust', 'Undertrust', 'Appropriate']}
    )

    fig.update_traces(textinfo="percent+label")
    fig.show()

if __name__ == "__main__":
    plot_trust_pie_by_facet("education", "Education Level")
    plot_trust_pie_by_facet("ai_familiarity", "AI Familiarity")
    plot_trust_pie_by_facet("age_bracket", "Age Bracket")
    plot_trust_pie_by_facet("gender", "Gender")
