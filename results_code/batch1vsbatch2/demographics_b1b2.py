import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import scikit_posthocs as sp  
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal 
from participant_dataloader import load_data

def analyze_demographic_differences(filepaths):
    combined_df = load_data(filepaths[0])  
    batch2_df = load_data(filepaths[2])

    batch1_df['batch'] = 'Batch 1'
    batch2_df['batch'] = 'Batch 2'

    df = pd.concat([batch1_df, batch2_df], ignore_index=True)

    print("\n=== DEMOGRAPHIC COMPARISON: BATCH 1 vs BATCH 2 ===")

    categorical_vars = ['gender', 'age_bracket', 'education', 'ai_familiarity']
    for var in categorical_vars:
        print(f"\n--- {var.upper()} ---")
        crosstab = pd.crosstab(df[var], df['batch'], dropna=False)
        print("Counts:")
        print(crosstab)

        
        chi2, p, dof, expected = chi2_contingency(crosstab)
        print(f"Chi-square test p-value: {p:.4f}")

    print("\n--- TRAINING TIME ---")

    batch1_df = batch1_df.drop_duplicates().head(110)
    batch2_df = batch2_df.drop_duplicates().head(112)

    print(f"Batch 1 total rows after filtering: {len(batch1_df)}")
    print(f"Batch 2 total rows after filtering: {len(batch2_df)}")

    train1 = batch1_df['training_time'].dropna()
    train2 = batch2_df['training_time'].dropna()

    print(f"Training time count in Batch 1 after dropna: {len(train1)}")
    print(f"Training time count in Batch 2 after dropna: {len(train2)}")

    if len(train1) > 0 and len(train2) > 0:
        stat, p_val = mannwhitneyu(train1, train2, alternative='two-sided')

        summary_df = pd.DataFrame({
            'Batch': ['Batch 1', 'Batch 2'],
            'Count': [len(train1), len(train2)],
            'Mean': [train1.mean(), train2.mean()],
            'Median': [train1.median(), train2.median()],
            'Std Dev': [train1.std(), train2.std()]
        })

        print(summary_df.to_string(index=False))
        print(f"Mann-Whitney U test p-value: {p_val:.4f}")

        combined = pd.concat([
            pd.DataFrame({'training_time': train1, 'batch': 'Batch 1'}),
            pd.DataFrame({'training_time': train2, 'batch': 'Batch 2'})
        ])

        plt.figure(figsize=(8, 6))
        sns.boxplot(x='batch', y='training_time', data=combined)
        sns.stripplot(x='batch', y='training_time', data=combined, color='black', alpha=0.3, jitter=True)
        plt.title("Distribution of Training Time by Batch")
        plt.ylabel("Training Time (units)")
        plt.xlabel("Batch")
        plt.tight_layout()
        plt.show()

def analyze_trust_differences(filepaths):

    combined_df = load_data(filepaths[0])
    batch1_df = load_data(filepaths[1])
    batch2_df = load_data(filepaths[2])

    batch1_df['batch'] = 'Batch 1'
    batch2_df['batch'] = 'Batch 2'
    df = pd.concat([batch1_df, batch2_df], ignore_index=True)

    print("\n=== TRUST BEHAVIOR COMPARISON: BATCH 1 vs BATCH 2 ===")

    trust_types = ['overtrust', 'undertrust', 'appropriate_yes', 'appropriate_no']

    for trust in trust_types:
        count_col = f"{trust}_count"
        conf_col = f"{trust}_avg_conf"

        print(f"\n--- {trust.replace('_', ' ').upper()} ---")

        counts1 = batch1_df[count_col].dropna()
        counts2 = batch2_df[count_col].dropna()

        if len(counts1) > 0 and len(counts2) > 0:
            stat, p_val = mannwhitneyu(counts1, counts2, alternative='two-sided')
            print(f"Median {trust} count (Batch 1): {counts1.median():.2f}")
            print(f"Median {trust} count (Batch 2): {counts2.median():.2f}")
            print(f"Mean {trust} count (Batch 1): {counts1.mean():.2f}")
            print(f"Mean {trust} count (Batch 2): {counts2.mean():.2f}")
            print(f"Std Dev {trust} count (Batch 1): {counts1.std():.2f}")
            print(f"Std Dev {trust} count (Batch 2): {counts2.std():.2f}")
            print(f"Count Mann-Whitney U test p-value: {p_val:.4f}")
            print(f"Total {trust} count (Batch 1): {counts1.sum()}")
            print(f"Total {trust} count (Batch 2): {counts2.sum()}")
        else:
            print("Count data missing or insufficient.")

        # Confidence comparison
        confs1 = batch1_df[conf_col].dropna()
        confs2 = batch2_df[conf_col].dropna()

        if len(confs1) > 0 and len(confs2) > 0:
            stat, p_val = mannwhitneyu(confs1, confs2, alternative='two-sided')
            print(f"Average {trust} confidence (Batch 1): {confs1.mean():.2f}")
            print(f"Average {trust} confidence (Batch 2): {confs2.mean():.2f}")
            print(f"Std Dev {trust} confidence (Batch 1): {confs1.std():.2f}")
            print(f"Std Dev {trust} confidence (Batch 2): {confs2.std():.2f}")
            print(f"Confidence Mann-Whitney U test p-value: {p_val:.4f}")
        else:
            print("Confidence data missing or insufficient.")

    # === SIDE-BY-SIDE BOXPLOTS FOR COUNTS ===
    count_melted = df.melt(
        id_vars="batch",
        value_vars=[f"{t}_count" for t in trust_types],
        var_name="Trust Type",
        value_name="Count"
    )
    count_melted["Trust Type"] = count_melted["Trust Type"].str.replace("_count", "").str.replace("_", " ").str.capitalize()

    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Trust Type", y="Count", hue="batch", data=count_melted)
    plt.title("Trust Behavior by Batch")
    plt.ylabel("Count")
    plt.xlabel("Trust Type")
    plt.legend(title="Batch")
    plt.tight_layout()
    plt.savefig("images/Trust_Behavior_by_Batch.png", dpi=300)
    #plt.show()

    # === SIDE-BY-SIDE BOXPLOTS FOR CONFIDENCE ===
    conf_melted = df.melt(
        id_vars="batch",
        value_vars=[f"{t}_avg_conf" for t in trust_types],
        var_name="Trust Type",
        value_name="Confidence"
    )
    conf_melted["Trust Type"] = conf_melted["Trust Type"].str.replace("_avg_conf", "").str.replace("_", " ").str.capitalize()

    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Trust Type", y="Confidence", hue="batch", data=conf_melted)
    plt.xlabel('')  # or plt.xlabel('Trust Category')
    plt.ylabel('')  # or plt.ylabel('Confidence Level')
    plt.legend(title="Batch")
    plt.tight_layout()
    plt.savefig("images/Trust_Behavior_and_Confidence_by_batch.png", dpi=300)
    #plt.show()

    # === SIDE-BY-SIDE BOXPLOTS FOR CONFIDENCE FOR THE COMBINED DATA ===
    palette = {
        'Overtrust': '#FE6100',
        'Undertrust': '#648FFF',
        'Appropriate yes': '#DC267F',
        'Appropriate no': '#DC267F'
    }

    conf_melted = combined_df.melt(
        id_vars=[],  # No id_vars since we don't want batch separation
        value_vars=[f"{t}_avg_conf" for t in trust_types],
        var_name="Trust Type",
        value_name="Confidence"
    )

    # Format the trust type labels
    conf_melted["Trust Type"] = (
        conf_melted["Trust Type"]
        .str.replace("_avg_conf", "")
        .str.replace("_", " ")
        .str.capitalize()
    )

    # Create the plot
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Trust Type", y="Confidence", data=conf_melted, palette=palette)
    plt.xlabel('')  
    plt.ylabel('')  
    plt.tight_layout()
    plt.savefig("images/Trust_Behavior_and_Confidence_combined.png", dpi=300)
    plt.show()


def analyze_trust_by_demographics_batch_comparison(filepaths):
    
    batch1_df = load_data(filepaths[1])
    batch2_df = load_data(filepaths[2])

    batch1_df['batch'] = 'Batch 1'
    batch2_df['batch'] = 'Batch 2'

    df = pd.concat([batch1_df, batch2_df], ignore_index=True)

    print("\n=== TRUST BEHAVIOR COMPARISON: BATCH 1 vs BATCH 2 ===")

    trust_types = ['overtrust', 'undertrust', 'appropriate']
    
    categorical_vars = ['gender', 'age_bracket', 'education', 'ai_familiarity']

    for demographic_var in categorical_vars:
        print(f"\n=== {demographic_var.upper()} ===")

        for trust in trust_types:
            count_col = f"{trust}_count"
            conf_col = f"{trust}_avg_conf"

            print(f"\n--- {trust.upper()} ---")

            grouped_batch1 = batch1_df.groupby([demographic_var])[[count_col, conf_col]].mean()
            grouped_batch2 = batch2_df.groupby([demographic_var])[[count_col, conf_col]].mean()

            for group in grouped_batch1.index:
                print(f"\nDemographic Group: {group}")
                
                counts1 = batch1_df[batch1_df[demographic_var] == group][count_col].dropna()
                counts2 = batch2_df[batch2_df[demographic_var] == group][count_col].dropna()
                confs1 = batch1_df[batch1_df[demographic_var] == group][conf_col].dropna()
                confs2 = batch2_df[batch2_df[demographic_var] == group][conf_col].dropna()

                if len(counts1) > 0 and len(counts2) > 0:
                    stat, p_val = mannwhitneyu(counts1, counts2, alternative='two-sided')
                    print(f"Median {trust} count (Batch 1): {counts1.median():.2f}")
                    print(f"Median {trust} count (Batch 2): {counts2.median():.2f}")
                    print(f"Mean {trust} count (Batch 1): {counts1.mean():.2f}")
                    print(f"Mean {trust} count (Batch 2): {counts2.mean():.2f}")
                    print(f"Std Dev {trust} count (Batch 1): {counts1.std():.2f}")
                    print(f"Std Dev {trust} count (Batch 2): {counts2.std():.2f}")
                    print(f"Count Mann-Whitney U test p-value: {p_val:.4f}")
                else:
                    print(f"Count data missing or insufficient for {trust} in group {group}.")

                if len(confs1) > 0 and len(confs2) > 0:
                    stat, p_val = mannwhitneyu(confs1, confs2, alternative='two-sided')
                    print(f"Average {trust} confidence (Batch 1): {confs1.mean():.2f}")
                    print(f"Average {trust} confidence (Batch 2): {confs2.mean():.2f}")
                    print(f"Std Dev {trust} confidence (Batch 1): {confs1.std():.2f}")
                    print(f"Std Dev {trust} confidence (Batch 2): {confs2.std():.2f}")
                    print(f"Confidence Mann-Whitney U test p-value: {p_val:.4f}")
                else:
                    print(f"Confidence data missing or insufficient for {trust} in group {group}.")

def analyze_trust_by_demographics(filepaths):

    output_dir = "batch1vsbatch2/files_generated"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "trust_analysis_output.txt")

    original_stdout = sys.stdout  
    with open(output_file, "w") as f:
        sys.stdout = f  

        try:
            df = load_data(filepaths[2])

            categorical_vars = ['gender', 'age_bracket', 'education', 'ai_familiarity']
            trust_types = ['overtrust', 'undertrust', 'appropriate']

            print("\n=== TRUST BEHAVIOR COMPARISON ACROSS DEMOGRAPHIC GROUPS ===")

            for demographic_var in categorical_vars:
                print(f"\n\n=== {demographic_var.upper()} ===")

                demographic_values = df[demographic_var].dropna().unique()

                # --- Kruskal-Wallis Tests Across Groups ---
                print(f"\nStatistical tests for {demographic_var.upper()}:")

                for trust in trust_types:
                    count_col = f"{trust}_count"
                    conf_col = f"{trust}_avg_conf"

                    groups_counts = [df[df[demographic_var] == group][count_col].dropna() for group in demographic_values]
                    groups_confs = [df[df[demographic_var] == group][conf_col].dropna() for group in demographic_values]

                    valid_counts_groups = [g for g in groups_counts if len(g) > 0]
                    if len(valid_counts_groups) > 1:
                        stat, p = kruskal(*valid_counts_groups)
                        print(f"Kruskal-Wallis test for {trust} count: H={stat:.3f}, p={p:.4f}")
                    else:
                        print(f"Not enough data for Kruskal-Wallis test on {trust} count.")

                    valid_confs_groups = [g for g in groups_confs if len(g) > 0]
                    if len(valid_confs_groups) > 1:
                        stat, p = kruskal(*valid_confs_groups)
                        print(f"Kruskal-Wallis test for {trust} confidence: H={stat:.3f}, p={p:.4f}")
                    else:
                        print(f"Not enough data for Kruskal-Wallis test on {trust} confidence.")

                # --- Descriptive stats by demographic groups ---
                for group in demographic_values:
                    print(f"\n--- DEMOGRAPHIC GROUP: {group} ---")

                    rows = []
                    for trust in trust_types:
                        count_col = f"{trust}_count"
                        conf_col = f"{trust}_avg_conf"

                        counts = df[df[demographic_var] == group][count_col].dropna()
                        confs = df[df[demographic_var] == group][conf_col].dropna()

                        row = {
                            "Trust Type": trust.capitalize()
                        }

                        if len(counts) > 0:
                            row["Median Count"] = f"{counts.median():.2f}"
                            row["Mean Count"] = f"{counts.mean():.2f}"
                            row["StdDev Count"] = f"{counts.std():.2f}"
                        else:
                            row["Median Count"] = row["Mean Count"] = row["StdDev Count"] = "N/A"

                        if len(confs) > 0:
                            row["Mean Confidence"] = f"{confs.mean():.2f}"
                            row["StdDev Confidence"] = f"{confs.std():.2f}"
                        else:
                            row["Mean Confidence"] = row["StdDev Confidence"] = "N/A"

                        rows.append(row)

                    result_df = pd.DataFrame(rows)
                    print(result_df.to_string(index=False))

        finally:
            sys.stdout = original_stdout 