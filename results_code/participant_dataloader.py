import json
import pandas as pd

def categorize_trust(response_data):
    """
    Classify the trust response into Overtrust, Undertrust, Appropriate Yes, or Appropriate No.
    """
    trust_type = None
    if response_data['trust'] == "Yes" and response_data['trust_correct'] == False:
        trust_type = "Overtrust"
    elif response_data['trust'] == "No" and response_data['trust_correct'] == False:
        trust_type = "Undertrust"
    elif response_data['trust'] == "Yes" and response_data['correct_response'] == "Yes":
        trust_type = "Appropriate Yes"
    elif response_data['trust'] == "No" and response_data['correct_response'] == "No":
        trust_type = "Appropriate No"
    return trust_type

def load_data(filepath="results.txt"):
    """
    Loads the data from a JSON file and returns it as a Pandas DataFrame.
    Each participant's data is aggregated into one record.

    :param filepath: Path to the results file.
    :return: DataFrame containing the parsed data.
    """
    data = []
    with open(filepath, "r") as file:
        for line in file:
            if line.strip():  # Skip empty lines
                data.append(json.loads(line.strip()))

    records = []
    for respondent in data:
        timings = respondent.get("timings", {})
        responses = respondent.get("response", {})
        
        demographics_end = timings.get("sections", {}).get("demographics_end", None)
        questions_start = timings.get("sections", {}).get("questions_start", None)

        record = {
            "demographics_end": demographics_end,
            "questions_start": questions_start,
            "total_time": timings.get("total_time"),
            "gender": responses.get("gender"),
            "age_bracket": responses.get("age_bracket"),
            "education": responses.get("education"),
            "ai_familiarity": responses.get("ai_familiarity"),
        }

        # Updated trust classification categories
        trust_categories = ["Overtrust", "Undertrust", "Appropriate Yes", "Appropriate No"]
        trust_counts = {key: 0 for key in trust_categories}
        trust_confidences = {key: [] for key in trust_categories}

        for key, value in respondent.items():
            if key in ["timings", "response"]:
                continue
            if not isinstance(value, dict):
                continue
            if all(k in value for k in ["trust", "trust_correct", "correct_response", "confidence"]):
                trust_type = categorize_trust(value)
                if trust_type:
                    trust_counts[trust_type] += 1
                    trust_confidences[trust_type].append(value["confidence"])

        for trust_type in trust_categories:
            record[f"{trust_type.lower().replace(' ', '_')}_count"] = trust_counts[trust_type]
            confidences = trust_confidences[trust_type]
            record[f"{trust_type.lower().replace(' ', '_')}_avg_conf"] = (
                sum(confidences) / len(confidences) if confidences else None
            )

        records.append(record)

    df = pd.DataFrame(records)
    df['training_time'] = df['questions_start'] - df['demographics_end']

    return df
