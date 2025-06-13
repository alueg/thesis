import pandas as pd
import matplotlib.pyplot as plt
from dataloader import load_data

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

def plot_nested_pie(file_path):
    df = load_data(file_path)
    
    df[['trust_mismatch', 'appropriate_detail']] = df.apply(
        lambda row: pd.Series(identify_trust_mismatch_detailed(row)), axis=1
    )
    
    # Replace None with a string for consistent grouping
    df['appropriate_detail'] = df['appropriate_detail'].fillna('None')

    # Aggregate counts
    inner_counts = df['trust_mismatch'].value_counts()
    outer_counts = df.groupby(['trust_mismatch', 'appropriate_detail']).size()

    # Colors for the main categories
    color_map = {
        'Overtrust': '#FE6100',
        'Undertrust': '#648FFF',
        'Appropriate': '#DC267F'
    }

    inner_colors = [color_map.get(cat, '#AAAAAA') for cat in inner_counts.index]

    # Generate colors for outer ring: slightly lighter/darker variations
    import matplotlib.colors as mcolors
    def lighten_color(color, amount=0.5):
        c = mcolors.to_rgb(color)
        c = [1 - (1 - x) * amount for x in c]
        return c

    outer_colors = []
    for cat, subcat in outer_counts.index:
        base_color = color_map.get(cat, '#AAAAAA')
        outer_colors.append(lighten_color(base_color, amount=0.7))

    fig, ax = plt.subplots(figsize=(8, 8))

    # Inner pie (main categories)
    ax.pie(inner_counts, labels=inner_counts.index, radius=1.0, colors=inner_colors,
           wedgeprops=dict(width=0.3, edgecolor='w'), autopct='%1.1f%%', pctdistance=0.8)

    # Outer pie (subcategories)
    ax.pie(outer_counts, labels=outer_counts.index.get_level_values(1), radius=1.3,
           colors=outer_colors, wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance=1.1,
           autopct='%1.1f%%', pctdistance=0.85)

    plt.title("Trust Mismatch Breakdown - Nested Pie Chart")
    plt.show()
