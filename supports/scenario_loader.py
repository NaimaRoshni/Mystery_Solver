# scenario_loader.py
# Loads structured case files (e.g., midnight_gala.json) from assets/cases/

import json
import os

def load_case(case_id, base_path="assets/cases"):
    """
    Load a mystery scenario from a JSON file by its case_id.

    Args:
        case_id (str): The unique ID of the case (e.g., "midnight_gala")
        base_path (str): Base directory where cases are stored

    Returns:
        dict: Dictionary containing title, description, suspects, evidence
    """
    file_path = os.path.join(base_path, f"{case_id}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Case file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        case_data = json.load(f)

    return case_data

def list_available_cases(base_path="assets/cases"):
    """
    List all available cases by scanning the JSON files in the directory.

    Args:
        base_path (str): Folder containing case JSON files

    Returns:
        list of dicts: Each dict includes {case_id, title}
    """
    cases = []
    for filename in os.listdir(base_path):
        if filename.endswith(".json"):
            path = os.path.join(base_path, filename)
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cases.append({
                    "case_id": data.get("case_id"),
                    "title": data.get("title")
                })
    return sorted(cases, key=lambda x: x['title'])
