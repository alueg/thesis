import plotly.express as px
import pandas as pd
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

def plot_mismatch(file_path):
    # Load the data
    df = load_data(file_path)

    # Apply detailed mismatch classification
    df[['trust_mismatch', 'appropriate_detail']] = df.apply(lambda row: pd.Series(identify_trust_mismatch_detailed(row)), axis=1)

    # Pie Chart: Overtrust vs Undertrust
    trust_counts = df['trust_mismatch'].value_counts().reset_index()
    trust_counts.columns = ['Trust Mismatch', 'Count']
    fig1 = px.pie(trust_counts[trust_counts['Trust Mismatch'].isin(['Overtrust', 'Undertrust'])],
                  values='Count', names='Trust Mismatch',
                  title="Proportion of Overtrust vs Undertrust",
                  color='Trust Mismatch',
                  color_discrete_map={'Overtrust': '#ff9999', 'Undertrust': '#66b3ff'})

    # Pie Chart: Trust Yes vs Trust No
    trust_yes_no_counts = df['trust'].value_counts().reset_index()
    trust_yes_no_counts.columns = ['Trust', 'Count']
    fig2 = px.pie(trust_yes_no_counts, values='Count', names='Trust',
                  title="Proportion of Trust Yes vs Trust No",
                  color='Trust', color_discrete_map={'Yes': '#ff9999', 'No': '#66b3ff'})

    # Pie Chart: Overtrust, Undertrust, and Appropriate
    trust_mismatch_counts = df['trust_mismatch'].value_counts().reset_index()
    trust_mismatch_counts.columns = ['Trust Mismatch', 'Count']
    fig3 = px.pie(trust_mismatch_counts, values='Count', names='Trust Mismatch',
                  title="Proportion of Overtrust, Undertrust, and Appropriate Trust",
                  color='Trust Mismatch',
                  color_discrete_map={'Overtrust': '#ff9999', 'Undertrust': '#66b3ff', 'Appropriate': '#66ff66'})

    # Sunburst Chart: Overtrust, Undertrust, and split of Appropriate
    df_sunburst = df.copy()
    df_sunburst['Subcategory'] = df_sunburst['appropriate_detail']
    df_sunburst['Subcategory'] = df_sunburst['Subcategory'].fillna("")

    fig4 = px.sunburst(df_sunburst,
                       path=['trust_mismatch', 'Subcategory'],
                       title="Detailed Trust Mismatch with Appropriate Split",
                       color='trust_mismatch',
                       color_discrete_map={'Overtrust': '#ff9999',
                                           'Undertrust': '#66b3ff',
                                           'Appropriate': '#66ff66'})
    
    # Filter for overtrust cases
    overtrust_df = df[df['trust_mismatch'] == "Overtrust"]

    # Ensure confidence is treated as categorical with ordered levels 1–5
    overtrust_df['confidence'] = pd.Categorical(overtrust_df['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Histogram of confidence for Overtrust cases
    fig5 = px.histogram(overtrust_df, x='confidence',
                        category_orders={'confidence': [1, 2, 3, 4, 5]},
                        title="Confidence Distribution for Overtrust Cases",
                        labels={'confidence': 'Confidence Level'},
                        color_discrete_sequence=['#ff9999'])

    fig5.update_xaxes(type='category')  # Force categorical x-axis

    # Filter for undertrust cases
    undertrust_df = df[df['trust_mismatch'] == "Undertrust"]

    # Ensure confidence is treated as categorical with ordered levels 1–5
    undertrust_df['confidence'] = pd.Categorical(undertrust_df['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Histogram of confidence for Undertrust cases
    fig6 = px.histogram(undertrust_df, x='confidence',
                        category_orders={'confidence': [1, 2, 3, 4, 5]},
                        title="Confidence Distribution for Undertrust Cases",
                        labels={'confidence': 'Confidence Level'},
                        color_discrete_sequence=['#66b3ff'])

    fig6.update_xaxes(type='category')  # Force categorical x-axis

    # Combine overtrust and undertrust data
    combined_df = df[df['trust_mismatch'].isin(['Overtrust', 'Undertrust'])].copy()

    # Ensure confidence is categorical
    combined_df['confidence'] = pd.Categorical(combined_df['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Count occurrences
    count_df = combined_df.groupby(['trust_mismatch', 'confidence']).size().reset_index(name='Count')

    # Normalize to get proportion per trust_mismatch
    total_counts = count_df.groupby('trust_mismatch')['Count'].transform('sum')
    count_df['Proportion'] = count_df['Count'] / total_counts

    # Create grouped bar chart (proportion)
    fig7 = px.bar(count_df, x='confidence', y='Proportion', color='trust_mismatch',
                  barmode='group',
                  title='Proportion of Confidence Levels for Overtrust vs Undertrust',
                  labels={'confidence': 'Confidence Level', 'Proportion': 'Proportion'},
                  color_discrete_map={'Overtrust': '#ff9999', 'Undertrust': '#66b3ff'})

    fig7.update_xaxes(type='category')
    fig7.show()

    # Combine overtrust, undertrust, and appropriate data
    combined_df_all = df[df['trust_mismatch'].isin(['Overtrust', 'Undertrust', 'Appropriate'])].copy()

    # Ensure confidence is categorical and ordered
    combined_df_all['confidence'] = pd.Categorical(combined_df_all['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Group and count
    count_all_df = combined_df_all.groupby(['trust_mismatch', 'confidence']).size().reset_index(name='Count')

    # Normalize to proportions within each trust_mismatch group
    total_counts_all = count_all_df.groupby('trust_mismatch')['Count'].transform('sum')
    count_all_df['Proportion'] = count_all_df['Count'] / total_counts_all

    # Grouped bar chart: Proportion of confidence levels across all trust mismatches
    fig8 = px.bar(count_all_df, x='confidence', y='Proportion', color='trust_mismatch',
                  barmode='group',
                  title='Proportion of Confidence Levels for Overtrust, Undertrust, and Appropriate Trust',
                  labels={'confidence': 'Confidence Level', 'Proportion': 'Proportion'},
                  color_discrete_map={
                      'Overtrust': '#ff9999',
                      'Undertrust': '#66b3ff',
                      'Appropriate': '#66ff66'
                  })

    fig8.update_xaxes(type='category')

        # Add a new column for fine-grained categories
    df['trust_mismatch_split'] = df.apply(
        lambda row: row['appropriate_detail'] if row['trust_mismatch'] == "Appropriate" else row['trust_mismatch'],
        axis=1
    )

    # Filter relevant categories
    relevant_categories = ['Overtrust', 'Undertrust', 'Trust Yes, Correct', 'Trust No, Correct']
    df_split = df[df['trust_mismatch_split'].isin(relevant_categories)].copy()

    # Ensure confidence is treated as ordered categorical
    df_split['confidence'] = pd.Categorical(df_split['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Group by trust mismatch split and confidence, then count
    count_split_df = df_split.groupby(['trust_mismatch_split', 'confidence']).size().reset_index(name='Count')

    # Normalize to get proportions
    count_split_df['Proportion'] = count_split_df.groupby('trust_mismatch_split')['Count'].transform(lambda x: x / x.sum())

    # Create grouped bar chart
    fig9 = px.bar(count_split_df, x='confidence', y='Proportion', color='trust_mismatch_split',
                  barmode='group',
                  title='Proportion of Confidence Levels by Trust Category (Split Appropriate)',
                  labels={'confidence': 'Confidence Level', 'Proportion': 'Proportion'},
                  color_discrete_map={
                      'Overtrust': '#ff9999',
                      'Undertrust': '#66b3ff',
                      'Trust Yes, Correct': '#66ff66',
                      'Trust No, Correct': '#99ffcc'
                  })

    fig9.update_xaxes(type='category')

    # Ensure confidence is treated as ordered categorical
    df['confidence'] = pd.Categorical(df['confidence'], categories=[1, 2, 3, 4, 5], ordered=True)

    # Group by trust and confidence, then count
    trust_conf_df = df.groupby(['trust', 'confidence']).size().reset_index(name='Count')

    # Normalize to proportions within each trust group
    trust_conf_df['Proportion'] = trust_conf_df.groupby('trust')['Count'].transform(lambda x: x / x.sum())

    # Create grouped bar chart
    fig10 = px.bar(trust_conf_df, x='confidence', y='Proportion', color='trust',
                barmode='group',
                title='Proportion of Confidence Levels by Trust Decision (Yes/No)',
                labels={'confidence': 'Confidence Level', 'Proportion': 'Proportion'},
                color_discrete_map={'Yes': '#ff9999', 'No': '#66b3ff'})

    fig10.update_xaxes(type='category')



    #Show all charts

    #Overtrust vs undertrust
    #fig1.show()


    #fig2.show()
    #fig3.show()
    #fig4.show()
    #fig5.show()
    #fig6.show()
    #fig7.show()
    #fig8.show()
    #fig9.show()
    #fig10.show()
    

