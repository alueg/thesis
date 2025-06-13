import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from participant_dataloader import load_data

def plot_demographic_barcharts(filepath="results_combined/Batch1ResultsAll.txt"):
    """
    Generates an interactive Plotly figure with 4 subplots showing demographic distributions:
    gender, age bracket, education, and AI familiarity.
    """
    df = load_data(filepath)

    # Drop missing values for each demographic
    df = df.dropna(subset=["gender", "age_bracket", "education", "ai_familiarity"])

    # Mappings for better display labels
    gender_map = {
        "male": "Male",
        "female": "Female",
        "non_binary": "Non-binary",
        "prefer_not_say": "Prefer not to say"
    }

    age_order = ["18_24", "25_34", "35_44", "45_54", "55_64", "65_plus"]
    age_map = {
        "18_24": "18–24",
        "25_34": "25–34",
        "35_44": "35–44",
        "45_54": "45–54",
        "55_64": "55–64",
        "65_plus": "65+"
    }

    edu_order = ["high_school_diploma", "some_college", "bachelor", "master", "doctoral", "other"]
    edu_map = {
        "high_school_diploma": "High School Diploma",
        "some_college": "Some College",
        "bachelor": "Bachelor",
        "master": "Master",
        "doctoral": "Doctoral",
        "other": "Other"
    }

    ai_order = ["none", "basic", "moderate", "high"]
    ai_map = {
        "none": "None",
        "basic": "Basic",
        "moderate": "Moderate",
        "high": "High"
    }

    # Apply mappings
    df["gender_clean"] = df["gender"].map(gender_map)
    df["age_clean"] = df["age_bracket"].map(age_map)
    df["education_clean"] = df["education"].map(edu_map)
    df["ai_familiarity_clean"] = df["ai_familiarity"].map(ai_map)

    # Prepare counts with proper order
    gender_counts = df["gender_clean"].value_counts().reindex(gender_map.values())
    age_counts = df["age_clean"].value_counts().reindex([age_map[k] for k in age_order])
    edu_counts = df["education_clean"].value_counts().reindex([edu_map[k] for k in edu_order])
    ai_counts = df["ai_familiarity_clean"].value_counts().reindex([ai_map[k] for k in ai_order])

    # Create subplot grid
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Gender Distribution", "Age Bracket Distribution", "Education Level Distribution", "AI Familiarity")
    )

    # Add traces
    fig.add_trace(go.Bar(x=gender_counts.index, y=gender_counts.values), row=1, col=1)
    fig.add_trace(go.Bar(x=age_counts.index, y=age_counts.values), row=1, col=2)
    fig.add_trace(go.Bar(x=edu_counts.index, y=edu_counts.values), row=2, col=1)
    fig.add_trace(go.Bar(x=ai_counts.index, y=ai_counts.values), row=2, col=2)

    # Layout update
    fig.update_layout(
        height=800,
        width=1000,
        title_text="Demographic Distributions",
        showlegend=False
    )

    fig.show()
