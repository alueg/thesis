import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import warnings
from sklearn.utils import resample
import statsmodels.formula.api as smf
from statsmodels.genmod.generalized_estimating_equations import GEE
from statsmodels.genmod.families import Binomial
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
import statsmodels.api as sm



warnings.filterwarnings('ignore')


def create_formula(X_columns: List[str]) -> str:
    """Create a formula for mixed-effects models"""
    predictors = " + ".join(X_columns)
    return f"outcome ~ {predictors}"


def bootstrap_mixed_effects_logistic(X: pd.DataFrame, y: pd.Series, 
                                   participant_ids: pd.Series,
                                   n_bootstrap: int = 1000, 
                                   random_state: int = 42) -> Dict[str, Dict]:
    np.random.seed(random_state)
    
    #Convert inputs to dataframe for statsmodels
    data = X.copy()
    data['outcome'] = y
    data['participant_id'] = participant_ids
    
    #Get unique participants
    unique_participants = data['participant_id'].unique()
    n_participants = len(unique_participants)
    
    #Prepare storage for bootstrap coefficients
    bootstrap_coefficients = []
    column_names = list(X.columns)
    column_names_with_intercept = ["Intercept"] + column_names
    
    
    print(f"Starting bootstrap with {n_bootstrap} iterations...")
    print(f"Resampling {n_participants} participants with replacement")
    
    #Run bootstrap samples
    for i in range(n_bootstrap):
        if i > 0 and i % 100 == 0:
            print(f"  Bootstrap iteration {i}/{n_bootstrap}")
            
        try:
            #Resample participants with replacement
            sampled_participants = np.random.choice(
                unique_participants, 
                size=n_participants, 
                replace=True
            )
            
            #Create bootstrap sample by including all observations from sampled participants
            bootstrap_indices = []
            for participant in sampled_participants:
                participant_indices = data.index[data['participant_id'] == participant].tolist()
                bootstrap_indices.extend(participant_indices)
            
            bootstrap_data = data.iloc[bootstrap_indices].copy()

            exog = sm.add_constant(bootstrap_data[column_names])
            exog_re = pd.get_dummies(bootstrap_data["participant_id"], drop_first=False)
            ident = np.zeros(exog_re.shape[1], dtype=int) 

            #Run mixed effect logistc regression
            model = BinomialBayesMixedGLM(bootstrap_data["outcome"], 
                                          exog, 
                                          exog_re, 
                                          ident=ident)
            fit_result = model.fit_vb()

            coefs = list(fit_result.params[0:len(column_names)+1])  
            bootstrap_coefficients.append(coefs)
        
        except Exception as e:
            print(f"  Warning: Bootstrap iteration {i} failed with error: {str(e)}")
            bootstrap_coefficients.append([0.0] * len(column_names))


    #Calculate bootstrap statistics
    bootstrap_coefficients = np.array(bootstrap_coefficients)
    results = {}
    
    for i, col in enumerate(column_names_with_intercept):
        coef_samples = bootstrap_coefficients[:, i]
        
        results[col] = {
            'mean': np.mean(coef_samples),
            'median': np.median(coef_samples),
            'std': np.std(coef_samples),
            'ci_lower': np.percentile(coef_samples, 2.5),
            'ci_upper': np.percentile(coef_samples, 97.5),
            'bootstrap_samples': coef_samples,
            'significant': not (np.percentile(coef_samples, 2.5) <= 0 <= np.percentile(coef_samples, 97.5))
        }
    
    return results


def run_trust_type_analysis(df: pd.DataFrame, X: pd.DataFrame, 
                           trust_type: str, n_bootstrap: int = 1000,
                           confidence_level: float = 0.95,
                           random_state: int = 42) -> Optional[Dict]:
    
    #Create binary outcome variable
    y = (df['trust_type'] == trust_type).astype(int)
    
    #Get participant IDs
    participant_ids = df['participant_id']
    
    #Check if we have enough cases
    if y.sum() < 10:
        print(f"Warning: Only {y.sum()} cases of {trust_type} - skipping analysis")
        return None
    
    #Run bootstrap analysis
    results = bootstrap_mixed_effects_logistic(
        X, y, participant_ids, 
        n_bootstrap=n_bootstrap, 
        random_state=random_state
    )
    
    return results


def run_full_bootstrap_analysis(df: pd.DataFrame, X: pd.DataFrame,
                               trust_types: List[str],
                               n_bootstrap: int = 1000,
                               confidence_level: float = 0.95,
                               random_state: int = 42) -> Dict:
    
    print(f"Running mixed-effects bootstrap analysis for {len(trust_types)} trust types...")
    print(f"Using participant-level resampling with {len(df['participant_id'].unique())} participants")
    
    all_results = {}
    
    for trust_type in trust_types:
        print(f"Analyzing {trust_type} trust...")
        
        results = run_trust_type_analysis(
            df, X, trust_type, n_bootstrap, confidence_level, random_state
        )
        
        if results:
            all_results[trust_type] = results
            significant_factors = [f for f, stats in results.items() if stats['significant']]
            print(f"  Found {len(significant_factors)} significant factors")
        else:
            print(f"  Skipped due to insufficient data")
    
    return all_results


def calculate_effect_sizes(all_results: Dict) -> Dict:
    effect_sizes = {}
    
    for trust_type, results in all_results.items():
        effect_sizes[trust_type] = {}
        
        for factor, stats in results.items():
            #Calculate odds ratio and CI
            or_mean = np.exp(stats['mean'])
            or_ci_lower = np.exp(stats['ci_lower'])
            or_ci_upper = np.exp(stats['ci_upper'])
            
            effect_sizes[trust_type][factor] = {
                'odds_ratio': or_mean,
                'or_ci_lower': or_ci_lower,
                'or_ci_upper': or_ci_upper,
                'significant': stats['significant']
            }
    
    return effect_sizes


def get_bootstrap_summary(all_results: Dict) -> Dict:
    summary = {
        'significant_effects': {},
        'largest_effects': {},
        'total_factors_tested': 0,
        'total_significant_effects': 0
    }
    
    for trust_type, results in all_results.items():
        #Get significant factors
        significant_factors = [
            factor for factor, stats in results.items() 
            if stats['significant']
        ]
        summary['significant_effects'][trust_type] = significant_factors
        
        #Find largest effect
        if results:
            largest_factor = max(results.keys(), key=lambda f: abs(results[f]['mean']))
            summary['largest_effects'][trust_type] = {
                'factor': largest_factor,
                'coefficient': results[largest_factor]['mean'],
                'significant': results[largest_factor]['significant']
            }
        
        summary['total_factors_tested'] += len(results)
        summary['total_significant_effects'] += len(significant_factors)
    
    return summary


