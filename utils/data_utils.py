import json
import os
from datetime import datetime

# Define file paths
STUDENT_DATA_FILE = "data/student_data.json"
PARENT_OBSERVATIONS_FILE = "data/parent_observations.json"
APP_SETTINGS_FILE = "data/app_settings.json" # Already in use

def _ensure_data_directory_exists():
    """Ensures that the 'data' directory exists."""
    os.makedirs("data", exist_ok=True)

def _load_json_data(file_path):
    """Loads data from a JSON file. Returns an empty list if file doesn't exist or is empty/corrupt."""
    _ensure_data_directory_exists()
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return []
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list): # Ensure it's a list, even if file contained a single object
                return [data] if data else []
            return data
    except json.JSONDecodeError:
        print(f"Warning: JSONDecodeError in {file_path}. File might be corrupt or empty. Returning empty list.")
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def _save_json_data(file_path, data):
    """Saves data to a JSON file."""
    _ensure_data_directory_exists()
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

# --- Public API for Student Prediction Data ---

def load_student_data():
    """Loads all student prediction records."""
    return _load_json_data(STUDENT_DATA_FILE)

def save_prediction_data(new_record):
    """Appends a new student prediction record to the data file."""
    records = load_student_data()
    records.append(new_record)
    return _save_json_data(STUDENT_DATA_FILE, records)

# --- Public API for Parent Observation Data ---

def load_parent_observations():
    """Loads all parent observation records."""
    return _load_json_data(PARENT_OBSERVATIONS_FILE)

def save_parent_observation(new_observation):
    """Appends a new parent observation record to the data file."""
    observations = load_parent_observations()
    observations.append(new_observation)
    return _save_json_data(PARENT_OBSERVATIONS_FILE, observations)

# --- Public API for App Settings (Already in utils/language_utils, confirming consistency) ---
# Note: These are defined in language_utils.py, but shown here for context of data files.
# def load_app_settings():
#     return _load_json_data(APP_SETTINGS_FILE) # This would typically return a dict, not a list
# def save_app_settings(settings):
#     return _save_json_data(APP_SETTINGS_FILE, settings)