import os
import json
from config import PROFILES_CONFIG_PATH

def load_profiles():
    """Load saved profiles"""
    try:
        if os.path.exists(PROFILES_CONFIG_PATH):
            with open(PROFILES_CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {"profiles": []}
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return {"profiles": []}

def save_profiles(profiles):
    """Save profiles to file"""
    try:
        with open(PROFILES_CONFIG_PATH, 'w') as f:
            json.dump(profiles, f, indent=4)
    except Exception as e:
        print(f"Error saving profiles: {e}")