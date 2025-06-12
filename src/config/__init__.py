import os

from helpers.system_tools import get_launcher_directory

# Global variables
LAUNCHER_DIR = get_launcher_directory()
MINECRAFT_DIRECTORY = os.path.join(LAUNCHER_DIR, ".minecraft")
os.makedirs(MINECRAFT_DIRECTORY, exist_ok=True)

# Minecraft and Forge configuration
MINECRAFT_VERSION = "1.18.2"
FORGE_VERSION = "40.3.0"

# Configuration file paths
PROFILES_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_profiles.json")
SETTINGS_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_settings.json")