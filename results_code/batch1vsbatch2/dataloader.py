import json
import pandas as pd

def load_data(filepath="data/results.txt"):
    data = []
    with open(filepath, "r") as file:
        for line in file:
            if line.strip():  # skip empty lines
                data.append(json.loads(line.strip()))

    records = []
    for respondent in data:
        timings = respondent.get("timings", {})
        responses = respondent.get("response", {})
        per_question = timings.get("per_question", [])

        for q in per_question:
            image_id = q["image"]
            rt = q["rt"]
            time_elapsed = q["time_elapsed"]
            question_data = respondent.get(image_id, {})

            # Use .get to safely access keys, handling missing values
            record = {
                "image": image_id,
                "rt": rt,
                "time_elapsed": time_elapsed,
                "trust": question_data.get("trust"),  # Ensure you use the correct key
                "confidence": question_data.get("confidence"),
                "correct_response": question_data.get("correct_response"),
                "trust_correct": question_data.get("trust_correct"),  # 'trust_correct' is the field name
                "label_correct": question_data.get("label_correct"),
                "ai_classification": question_data.get("ai_classification"),
                "gender": responses.get("gender"),
                "age_bracket": responses.get("age_bracket"),
                "education": responses.get("education"),
                "ai_familiarity": responses.get("ai_familiarity"),
                "total_time": timings.get("total_time"),
            }
            records.append(record)

    # Create DataFrame
    df = pd.DataFrame(records)
    
    return df
