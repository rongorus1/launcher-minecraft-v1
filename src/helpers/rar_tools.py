import os
import rarfile
from typing import Optional

from components.progress_bar_generic import ProgressBarGeneric


def extract_rar_file(rar_path: str, extract_dir: str, progress_bar: ProgressBarGeneric = None) -> Optional[str]:
    """
    Extrae un archivo RAR en el directorio especificado usando la librería rarfile.
    Requiere que 'unrar' esté instalado en el sistema.
    Si se pasa un progress_bar (CTkProgressBar), se actualiza el progreso.
    Devuelve None si todo va bien, o un mensaje de error si falla.
    """
    if not os.path.isfile(rar_path):
        return f"El archivo RAR no existe: {rar_path}"
    if not os.path.isdir(extract_dir):
        os.makedirs(extract_dir, exist_ok=True)
    try:
        with rarfile.RarFile(rar_path) as rf:
            infolist = rf.infolist()
            total = len(infolist)
            for idx, member in enumerate(infolist, 1):
                rf.extract(member, path=extract_dir)
                if progress_bar is not None:
                    if progress_bar.is_hidden:
                        progress_bar.show_element()
                    progress_bar.set(idx / total)
                    progress_bar.update_idletasks()
    except rarfile.RarCannotExec as e:
        return "No se encontró 'unrar' en el sistema. Instálalo para poder extraer archivos RAR."
    except Exception as e:
        return f"Excepción al extraer: {e}"
    return None
