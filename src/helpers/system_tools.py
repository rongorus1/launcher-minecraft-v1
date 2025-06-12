import os
import sys
import platform
from tkinter import messagebox

# Cross-platform path handling
def get_launcher_directory():
    """Get a cross-platform launcher directory"""
    try:
        if platform.system() == "Windows":
            base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
        elif platform.system() == "Darwin":  # macOS
            base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
        else:  # Linux and other systems
            base_dir = os.path.join(os.path.expanduser("~"), "RPLauncher")

        # Ensure the directory exists
        os.makedirs(base_dir, exist_ok=True)
        return base_dir
    except Exception as e:
        messagebox.showerror("Error", "No se pudo crear el directorio del launcher")
        return None

# Paths for resources
def get_resource_path(filename):
    """Get path for resources, supporting bundled and development environments"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)