import json
import pandas as pd

def load_data(filepath="data/results.txt"):
    """
    Loads the data from a JSON file and returns it as a Pandas DataFrame.
    Each respondent's response to each image is parsed.

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
        per_question = timings.get("per_question", [])

        # Extract demographics_end and questions_start for this participant
        demographics_end = timings.get("sections", {}).get("demographics_end", None)
        questions_start = timings.get("sections", {}).get("questions_start", None)

        # For each question in the "per_question" list, we'll add the same demographics_end and questions_start values
        for q in per_question:
            image_id = q["image"]
            rt = q["rt"]
            time_elapsed = q["time_elapsed"]
            question_data = respondent.get(image_id, {})

            # Create a record for each image/question, adding demographics_end and questions_start
            record = {
                "image": image_id,
                "rt": rt,
                "time_elapsed": time_elapsed,
                "trust": question_data.get("trust"),
                "confidence": question_data.get("confidence"),
                "correct_response": question_data.get("correct_response"),
                "correct": question_data.get("correct"),
                "gender": responses.get("gender"),
                "age_bracket": responses.get("age_bracket"),
                "education": responses.get("education"),
                "ai_familiarity": responses.get("ai_familiarity"),
                "total_time": timings.get("total_time"),
                "time_feeling": question_data.get("time_feeling"),
                "demographics_end": demographics_end,  # Participant-specific
                "questions_start": questions_start     # Participant-specific
            }
            records.append(record)

    # Convert the list of records into a DataFrame
    df = pd.DataFrame(records)
    return df
