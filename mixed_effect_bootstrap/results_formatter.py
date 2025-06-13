
import json
import pandas as pd
import numpy as np
import math
from typing import Dict
from datetime import datetime


def print_bootstrap_results(results: Dict, trust_type: str, confidence_level: float = 0.95):
    if not results:
        print(f"No results available for {trust_type}")
        return
    
    print(f"\n{'='*70}")
    print(f"BOOTSTRAP RESULTS FOR {trust_type.upper()} TRUST")
    print(f"{'='*70}")
    print(f"Confidence Level: {confidence_level*100}%")
    
    print(f"\nVariable        Coef.    Std.Err. P-value  CI Lower  CI Upper")
    print("-" * 70)
    
    for factor, stats in results.items():
        #Calculate approximate p-value based on CI
        z_score = abs(stats['mean'] / stats['std']) if stats['std'] > 0 else float('inf')
        #Convert to p-value 
        p_value = 2 * (1 - 0.5 * (1 + math.erf(z_score / math.sqrt(2))))
        
        if factor == "Intercept":
            factor_label = "Intercept".ljust(15)
        else:
            #Try to format factor names like "A1" → "factorA[T.1]"
            if len(factor) == 2 and factor[0] in "ABCD" and factor[1] in "12":
                factor_label = f"factor{factor[0]}[T.{factor[1]}]".ljust(15)
            else:
                factor_label = factor.ljust(15)

        print(f"{factor_label} {stats['mean']:<8.4f} {stats['std']:<8.4f} "
            f"{p_value:<8.3f} {stats['ci_lower']:<8.4f} {stats['ci_upper']:<8.4f}")

def print_factor_summary(all_results: Dict, confidence_level: float = 0.95):

    print(f"\n{'='*90}")
    print("FACTOR SUMMARY ACROSS TRUST TYPES")
    print(f"{'='*90}")
    print(f"Confidence Level: {confidence_level*100}%")
    
    #Factors list
    factors = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2']
    trust_types = ['overtrust', 'undertrust', 'appropriate']
    
    #Print coefficients
    print(f"\nLOGISTIC REGRESSION COEFFICIENTS:")
    print(f"{'Factor':<8}", end="")
    for trust_type in trust_types:
        print(f"{trust_type.capitalize():<15}", end="")
    print()
    print("-" * 75)
    
    for factor in factors:
        print(f"{factor:<8}", end="")
        for trust_type in trust_types:
            if trust_type in all_results and factor in all_results[trust_type]:
                mean_val = all_results[trust_type][factor]['mean']
                is_sig = all_results[trust_type][factor]['significant']
                sig_marker = "*" if is_sig else " "
                print(f"{mean_val:>6.3f}{sig_marker:<8}", end="")
            else:
                print(f"{'N/A':<15}", end="")
        print()
    
    print(f"\n* = Statistically significant ({confidence_level*100}% CI does not include 0)")


def print_factor_interpretations():
    pass


def create_results_dataframe(all_results: Dict) -> pd.DataFrame:
    rows = []
    
    for trust_type, trust_results in all_results.items():
        for factor, stats in trust_results.items():
            row = {
                'trust_type': trust_type,
                'factor': factor,
                'coefficient_mean': stats.get('mean', np.nan),
                'coefficient_median': stats.get('median', np.nan),
                'coefficient_std': stats.get('std', np.nan),
                'ci_lower': stats.get('ci_lower', np.nan),
                'ci_upper': stats.get('ci_upper', np.nan),
                'significant': stats.get('significant', False),
                'odds_ratio': np.exp(stats.get('mean', 0)) if stats.get('mean') is not None else np.nan
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def save_detailed_results(all_results: Dict, effect_sizes: Dict, summary: Dict,
                         filename: str, bootstrap_params: Dict):
    
    #Prepare results for JSON serialization
    json_results = {}
    for trust_type, trust_results in all_results.items():
        json_results[trust_type] = {}
        for factor, stats in trust_results.items():
            #Remove bootstrap_samples array for JSON (too large)
            json_stats = {k: v for k, v in stats.items() if k != 'bootstrap_samples'}
            #Convert numpy types to Python types
            for key, value in json_stats.items():
                if isinstance(value, (np.integer, np.floating)):
                    json_stats[key] = float(value)
                elif isinstance(value, np.bool_):
                    json_stats[key] = bool(value)
            json_results[trust_type][factor] = json_stats  
    
    #Add analysis_type if it exists in bootstrap_params
    analysis_type = bootstrap_params.get('analysis_type', 'bootstrap logistic regression')
    
    output = {
        'analysis_info': {
            'timestamp': datetime.now().isoformat(),
            'bootstrap_parameters': bootstrap_params,
            'confidence_level': bootstrap_params.get('confidence_level', 0.95),
            'analysis_type': analysis_type
        },
        'bootstrap_results': json_results,
        'effect_sizes': effect_sizes,
        'summary': summary,
        'factor_coding': {
            'A': {'1': 'Percentage format', '2': 'Raw output format', '3': 'Not present (baseline)'},
            'B': {'1': 'Short explanation', '2': 'Long explanation', '3': 'Not present (baseline)'},
            'C': {'1': 'Text description', '2': 'F1 score', '3': 'Not present (baseline)'},
            'D': {'1': 'Text description', '2': 'F1/F2/etc labels', '3': 'Not present (baseline)'}
        },
        'interpretation_guide': {
            'coefficients': 'Positive coefficients increase the log-odds of the trust type',
            'odds_ratios': 'OR > 1 increases odds, OR < 1 decreases odds',
            'significance': 'Based on confidence interval not containing 0'
        }
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: {filename}")


def export_to_csv(results_df: pd.DataFrame, filename: str):
    results_df.to_csv(filename, index=False)
    print(f"Results exported to CSV: {filename}")


