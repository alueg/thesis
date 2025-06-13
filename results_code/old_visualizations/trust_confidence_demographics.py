import pandas as pd
import plotly.express as px
from dataloader import load_data  # assumes this is in dataloader.py

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

def plot_trust_by_facet(facet_col, facet_label=None, filepath="data/results.txt"):
    df = load_data(filepath)
    df[['trust_mismatch', 'appropriate_detail']] = df.apply(
        lambda row: pd.Series(identify_trust_mismatch_detailed(row)), axis=1
    )

    # Drop rows with missing data in the facet column or trust mismatch
    df = df.dropna(subset=[facet_col, "trust_mismatch"])

    # Ensure confidence is ordered
    df["confidence"] = pd.Categorical(df["confidence"], categories=[1, 2, 3, 4, 5], ordered=True)

    # Group and normalize
    group_df = df.groupby([facet_col, "trust_mismatch", "confidence"]).size().reset_index(name="Count")
    group_df["Proportion"] = group_df.groupby([facet_col, "trust_mismatch"])["Count"].transform(lambda x: x / x.sum())

    # Create title dynamically
    title = f"Trust Mismatch (Overtrust, Undertrust, Appropriate) vs. Confidence by {facet_label or facet_col.capitalize()}"

    # Plot
    fig = px.bar(
        group_df,
        x="confidence", y="Proportion",
        color="trust_mismatch", barmode="group",
        facet_col=facet_col, facet_col_wrap=2,
        category_orders={"confidence": [1, 2, 3, 4, 5]},
        labels={"confidence": "Confidence Level", "Proportion": "Proportion"},
        title=title,
        color_discrete_map={
            "Overtrust": "#ff9999",
            "Undertrust": "#66b3ff",
            "Appropriate": "#66ff66"
        }
    )

    fig.update_xaxes(type="category")
    fig.show()

# Optional direct run for testing
if __name__ == "__main__":
    plot_trust_by_facet("education", "Education Level")
    plot_trust_by_facet("ai_familiarity", "AI Familiarity")
    plot_trust_by_facet("age_bracket", "Age Bracket")
    plot_trust_by_facet("gender", "Gender")
