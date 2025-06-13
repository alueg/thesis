import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_batch(file_path):
    with open(file_path, 'r') as f:
        data = []
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:  
                continue
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e}")
                print(f"Problematic line: {line}")
        return data

def analyze_label_correct(batch_files):
    participants = []
    for file in batch_files:
        participants.extend(load_batch(file))
    
    results = []
    for i, participant in enumerate(participants):
        question_keys = [k for k in participant.keys() if k not in ['timings', 'response']]
        label_correct_count = sum(1 for k in question_keys if participant[k].get("label_correct") is True)
        results.append({
            "participant_index": i,
            "label_correct_count": label_correct_count
        })
    
    return results

def create_answer_count_table(results):
    """Create a table showing how many participants had a certain number of correct answers."""
    df = pd.DataFrame(results)
    
    count_table = df['label_correct_count'].value_counts().reset_index()
    count_table.columns = ['Number of Correct Answers', 'Number of Participants']
    
    count_table = count_table.sort_values(by='Number of Correct Answers', ascending=False)
    
    count_table = count_table.reset_index(drop=True)
    
    return count_table

def save_filtered_participants(results, output_file, max_correct_answers=15):
    filtered_participants = [participant for participant in results if participant['label_correct_count'] <= max_correct_answers]
    
    with open(output_file, 'w') as f:
        for participant in filtered_participants:
            label_correct_count = 0
            for k in participant:
                if isinstance(participant[k], dict) and participant[k].get("label_correct") is True:
                    label_correct_count += 1
            
            participant['label_correct_count'] = label_correct_count
            
            json.dump(participant, f)
            f.write("\n")  

    print(f"Filtered participants saved to {output_file}")

def analyze_and_save_filtered(batch_files, output_file):
    all_results = []
    for file in batch_files:
        all_results.extend(analyze_label_correct([file]))  

    save_filtered_participants(all_results, output_file)

def visualize_combined_batches(batch1_file, batch2_file):
    batch1_results = analyze_label_correct([batch1_file])
    batch2_results = analyze_label_correct([batch2_file])

    batch1_count_table = create_answer_count_table(batch1_results)
    batch2_count_table = create_answer_count_table(batch2_results)

    print("Batch 1 - Correct Answer Count Table:")
    print(batch1_count_table.to_string(index=False))
    print("\nBatch 2 - Correct Answer Count Table:")
    print(batch2_count_table.to_string(index=False))

