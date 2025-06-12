import re
from tkinter import messagebox


def validate_ram(min_ram, max_ram):
    """Validate RAM settings"""
    try:
        # Convert to numeric values for comparison
        min_val = int(re.findall(r'\d+', min_ram)[0])
        max_val = int(re.findall(r'\d+', max_ram)[0])

        if min_val < 2 or max_val > 10:
            raise ValueError("RAM must be between 4G and 10G")

        if min_val >= max_val:
            raise ValueError("Minimum RAM must be less than maximum RAM")

        return True
    except Exception as e:
        messagebox.showerror("RAM Configuration Error", str(e))
        return False