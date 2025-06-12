import os.path
import shutil
from tkinter import messagebox

from components.progress_bar_generic import ProgressBarGeneric
from config import MINECRAFT_DIRECTORY
from helpers.file_dialog_tools import select_file_rar
from helpers.rar_tools import extract_rar_file


def run_update_mods_controller(progress_bar: ProgressBarGeneric = None):
    file_rar_path = select_file_rar()

    if file_rar_path:

        mods_path = os.path.join(MINECRAFT_DIRECTORY, "mods")
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
        else:
            shutil.rmtree(mods_path)
            os.makedirs(mods_path)

        extract_rar_file(file_rar_path, mods_path, progress_bar)
        messagebox.showinfo("Mods actualizados", "Los mods se actualizaron correctamente")
        if progress_bar is not None:
            if not progress_bar.is_hidden:
                progress_bar.hidde_element()
            progress_bar.set(0)
        return

    messagebox.showerror("Error", "No se pudo actualizar los mods")