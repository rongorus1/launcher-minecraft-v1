import os
import json
from config import SETTINGS_CONFIG_PATH

def load_settings():
    """Load launcher settings"""
    try:
        if os.path.exists(SETTINGS_CONFIG_PATH):
            with open(SETTINGS_CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {
            "ram": {
                "min": "4G",
                "max": "8G"
            },
            "last_profile": None
        }
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {
            "ram": {
                "min": "4G",
                "max": "8G"
            },
            "last_profile": None
        }

def save_settings(settings):
    """Save launcher settings"""
    try:
        with open(SETTINGS_CONFIG_PATH, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")