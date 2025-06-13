#Import modules
from data_processor import (
    load_jsonl_data, process_all_data, create_design_matrix, 
    get_data_summary, print_data_summary
)

from mixed_effects_bootstrap import (
    run_full_bootstrap_analysis, calculate_effect_sizes, get_bootstrap_summary,
)

from results_formatter import (
    print_bootstrap_results, print_factor_summary,
    print_factor_interpretations, save_detailed_results,
)


def main():
    #Bootstrap configuration
    data_file = 'CombinedBatch.txt'
    n_bootstraps = 1000
    confidence_level = 0.95
    output_file = 'bootstrap_results'
    random_seed = 42
    trust_types = ['overtrust', 'undertrust', 'appropriate']
    
    print("="*70)
    print("MIXED-EFFECTS BOOTSTRAP TRUST ANALYSIS")
    print("="*70)
    
    #Load and process data
    print(f"\nLoading data from: {data_file}")
    json_data_list = load_jsonl_data(data_file)
    print(f"Loaded {len(json_data_list)} participants")
    
    #Process the data
    print("Processing data...")
    df = process_all_data(json_data_list)
    
    #Print data summary
    data_summary = get_data_summary(df)
    print_data_summary(data_summary)
    
    #Create design matrix
    X = create_design_matrix(df)
    print(f"\nDesign matrix created with {X.shape[1]} factors")
    print(f"Factors: {list(X.columns)}")
    
    #Prepare bootstrap parameters
    bootstrap_params = {
        'n_bootstrap': n_bootstraps,
        'confidence_level': confidence_level,
        'random_state': random_seed,
        'trust_types_analyzed': trust_types,
        'analysis_type': 'mixed-effects logistic regression',
        'n_participants': len(df['participant_id'].unique())
    }
    
    #Run bootstrap analysis
    print(f"\nRunning mixed-effects bootstrap analysis...")
    all_results = run_full_bootstrap_analysis(
        df, X, trust_types, 
        n_bootstraps, confidence_level, random_seed
    )
    
    #Calculate effect sizes (odds ratios)
    print("\nCalculating effect sizes...")
    effect_sizes = calculate_effect_sizes(all_results)
    
    #Get analysis summary
    summary = get_bootstrap_summary(all_results)
    
    #Print detailed results
    print("\n" + "="*70)
    print("DETAILED RESULTS (MIXED-EFFECTS MODEL)")
    print("="*70)
    
    for trust_type in trust_types:
        if trust_type in all_results:
            print_bootstrap_results(all_results[trust_type], trust_type, confidence_level)
    
    #Print comprehensive summary
    print_factor_summary(all_results, confidence_level)
    print_factor_interpretations()
    
    #Save results
    print(f"\n{'='*70}")
    print("SAVING RESULTS")
    print(f"{'='*70}")
    
    #Save detailed JSON results
    json_filename = f"{output_file}.json"
    save_detailed_results(
        all_results, effect_sizes, summary, 
        json_filename, bootstrap_params
    )
    
    print(f"\nMixed-effects analysis results saved to: {json_filename}")
    
    #Print key findings summary
    print(f"\nKey findings:")
    total_significant = sum(len(factors) for factors in summary.get('significant_effects', {}).values())
    print(f"  - {total_significant} significant factor effects found across all trust types")
    
    for trust_type, factors in summary.get('significant_effects', {}).items():
        if factors:
            print(f"  - {trust_type.capitalize()} trust: {len(factors)} significant factors ({', '.join(factors)})")
    
    print(f"\nDone!")


if __name__ == "__main__":
    main()