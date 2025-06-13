import json
import pandas as pd
import re
from typing import List, Dict, Optional


def parse_factors(image_code: str) -> Optional[Dict[str, int]]:
    #Parse factor components from image codes like A3B2C3E2
    match = re.match(r'A(\d)B(\d)C(\d)E(\d)', image_code)
    if not match:
        return None
    
    return {
        'A': int(match.group(1)),
        'B': int(match.group(2)),
        'C': int(match.group(3)),
        'D': int(match.group(4))  #E corresponds to factor D
    }


def determine_trust_type(trust_response: str, correct_response: str, ai_classification: str) -> str:
    should_trust = correct_response == "Yes"
    did_trust = trust_response == "Yes"
    
    if should_trust and did_trust:
        return "appropriate"
    elif not should_trust and not did_trust:
        return "appropriate"
    elif not should_trust and did_trust:
        return "overtrust"
    elif should_trust and not did_trust:
        return "undertrust"
    else:
        return "appropriate"


def load_jsonl_data(filepath: str) -> List[Dict]:
    data = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  
                continue
            try:
                json_obj = json.loads(line)
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse JSON on line {line_num}: {e}")
                continue
    return data


def process_participant_data(participant_data: Dict, participant_id: int) -> List[Dict]:
    processed_rows = []
    exclude_keys = ['timings', 'response']
    
    for key, value in participant_data.items():
        if key not in exclude_keys and isinstance(value, dict):
            factors = parse_factors(key)
            if factors:
                trust_type = determine_trust_type(
                    value['trust'],
                    value['correct_response'],
                    value['ai_classification']
                )
                
                row = {
                    'image': key,
                    'A': factors['A'],
                    'B': factors['B'],
                    'C': factors['C'],
                    'D': factors['D'],
                    'trust': value['trust'],
                    'confidence': value['confidence'],
                    'correct_response': value['correct_response'],
                    'ai_classification': value['ai_classification'],
                    'trust_type': trust_type,
                    'trust_binary': 1 if value['trust'] == "Yes" else 0,
                    'correct_binary': 1 if value['correct_response'] == "Yes" else 0,
                    'participant_id': participant_id  
                }
                processed_rows.append(row)
    
    return processed_rows


def process_all_data(json_data_list: List[Dict]) -> pd.DataFrame:
    all_processed_data = []
    
    for participant_idx, participant_data in enumerate(json_data_list):
        participant_rows = process_participant_data(participant_data, participant_idx)
        all_processed_data.extend(participant_rows)
    
    return pd.DataFrame(all_processed_data)


def create_design_matrix(df: pd.DataFrame) -> pd.DataFrame:
    X = pd.DataFrame()
    
    #Create dummy variables for each factor 
    #Reference categories are A3, B3, C3, D3
    X['A1'] = (df['A'] == 1).astype(int)
    X['A2'] = (df['A'] == 2).astype(int)
    X['B1'] = (df['B'] == 1).astype(int)
    X['B2'] = (df['B'] == 2).astype(int)
    X['C1'] = (df['C'] == 1).astype(int)
    X['C2'] = (df['C'] == 2).astype(int)
    X['D1'] = (df['D'] == 1).astype(int)
    X['D2'] = (df['D'] == 2).astype(int)
    
    return X


def get_data_summary(df: pd.DataFrame) -> Dict:
    summary = {
        'total_observations': len(df),
        'unique_participants': len(df['participant_id'].unique()),
        'avg_observations_per_participant': len(df) / len(df['participant_id'].unique()),
        'trust_distribution': df['trust_type'].value_counts().to_dict(),
        'factor_distributions': {
            'A': df['A'].value_counts().to_dict(),
            'B': df['B'].value_counts().to_dict(),
            'C': df['C'].value_counts().to_dict(),
            'D': df['D'].value_counts().to_dict()
        },
        'ai_classification_distribution': df['ai_classification'].value_counts().to_dict()
    }
    
    return summary


def print_data_summary(summary: Dict):
    print(f"Data Summary:")
    print(f"  Total observations: {summary['total_observations']}")
    print(f"  Unique participants: {summary['unique_participants']}")
    
    print(f"\nTrust type distribution:")
    for trust_type, count in summary['trust_distribution'].items():
        percentage = count / summary['total_observations'] * 100
        print(f"  {trust_type}: {count} ({percentage:.1f}%)")