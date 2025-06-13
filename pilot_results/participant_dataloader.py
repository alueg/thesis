import json
import pandas as pd

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
        training_judgment = respondent.get("training_judgment", {})

        # Extract demographics_end and questions_start for this participant
        demographics_end = timings.get("sections", {}).get("demographics_end", None)
        questions_start = timings.get("sections", {}).get("questions_start", None)

        # Extract training judgment details
        helpful = training_judgment.get("helpful", None)
        confidence = training_judgment.get("confidence", None)
        coverage = training_judgment.get("coverage", None)

        # Create a single record for each participant
        record = {
            "demographics_end": demographics_end,
            "questions_start": questions_start,
            "total_time": timings.get("total_time"),
            "gender": responses.get("gender"),
            "age_bracket": responses.get("age_bracket"),
            "education": responses.get("education"),
            "ai_familiarity": responses.get("ai_familiarity"),
            "helpful": helpful,
            "confidence": confidence,
            "coverage": coverage
        }

        # Append the record for this participant
        records.append(record)

    # Convert the list of records into a DataFrame
    df = pd.DataFrame(records)

    # Calculate training_time for each participant
    df['training_time'] = df['questions_start'] - df['demographics_end']

    return df
