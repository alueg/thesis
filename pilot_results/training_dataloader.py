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
