from __future__ import annotations

import tkinter.filedialog as fd
from tkinter import messagebox

def select_file_rar() -> str | None:
    file_path = fd.askopenfilename(
        title="Seleccionar archivo RAR",
        filetypes=[("Archivos RAR", "*.rar")],
        initialdir="."
    )

    if file_path:
        return file_path

    return None