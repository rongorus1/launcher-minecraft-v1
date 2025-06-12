import os
import platform
import subprocess
import requests
import zipfile
import shutil
from tkinter import messagebox

from config import LAUNCHER_DIR


def descargar_java_17():
    """Descargar e instalar Java 17"""
    try:
        java_dir = os.path.join(LAUNCHER_DIR, "Java")
        java17_dir = os.path.join(java_dir, "java17")
        os.makedirs(java17_dir, exist_ok=True)

        # URLs de descarga por sistema operativo
        sistemas = {
            "Windows": "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_windows-x64_bin.zip",
            "Darwin": "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_macos-x64_bin.tar.gz",
            "Linux": "https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz"
        }

        sistema_actual = platform.system()
        java_url = sistemas.get(sistema_actual, sistemas["Windows"])

        messagebox.showinfo("Instalación de Java", "Descargando Java 17. Esto puede tardar unos minutos...")

        respuesta = requests.get(java_url, stream=True)
        ruta_zip = os.path.join(java_dir, "java17.zip")

        with open(ruta_zip, 'wb') as archivo:
            for fragmento in respuesta.iter_content(chunk_size=8192):
                archivo.write(fragmento)

        # Extracción
        if sistema_actual == "Windows":
            with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                zip_ref.extractall(java_dir)
            carpeta_extraida = os.path.join(java_dir, "jdk-17.0.2")
            shutil.move(carpeta_extraida, java17_dir)
        else:
            subprocess.run(['tar', '-xzf', ruta_zip, '-C', java_dir])
            carpeta_extraida = os.path.join(java_dir, "jdk-17.0.2")
            shutil.move(carpeta_extraida, java17_dir)

        os.remove(ruta_zip)
        messagebox.showinfo("Éxito", "Java 17 se ha instalado correctamente")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo instalar Java: {e}")
        return False

def detectar_java():
    """Detectar y forzar instalación de Java 17"""
    # Ruta fija de Java 17 en el directorio del launcher
    ruta_java_fija = os.path.join(LAUNCHER_DIR, "Java", "java17")

    try:
        # Definir rutas de binario de Java según el sistema operativo
        rutas_java = {
            "Windows": [
                os.path.join(ruta_java_fija, "bin", "java.exe"),  # Ruta del launcher
                os.path.join(ruta_java_fija, "jdk-17.0.2", "bin", "java.exe"),  # Ruta del launcher
                r"C:\Program Files\Java\jdk-17\bin\java.exe",  # Ruta de instalación común
                r"C:\Program Files (x86)\Java\jdk-17\bin\java.exe"  # Ruta alternativa
            ],
            "Darwin": [  # macOS
                os.path.join(ruta_java_fija, "Contents", "Home", "bin", "java"),
                "/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home/bin/java"
            ],
            "Linux": [
                os.path.join(ruta_java_fija, "bin", "java"),
                os.path.join(ruta_java_fija, "jdk-17.0.2", "bin", "java"),
                "/usr/lib/jvm/java-17-openjdk-amd64/bin/java",
                "/usr/lib/jvm/java-17/bin/java"
            ]
        }

        sistema_actual = platform.system()

        # Primero intentar con la ruta del launcher
        java_path = os.path.join(ruta_java_fija, "bin", "java.exe" if sistema_actual == "Windows" else "java")
        if os.path.exists(java_path):
            return java_path

        # Buscar en rutas predefinidas
        for path in rutas_java.get(sistema_actual, []):
            if os.path.exists(path):
                return path

        # Si no se encuentra, intentar descargar
        if descargar_java_17():
            # Verificar nuevamente después de la descarga
            java_path = os.path.join(ruta_java_fija, "bin", "java.exe" if sistema_actual == "Windows" else "java")
            if os.path.exists(java_path):
                return java_path

        # Si todo falla
        messagebox.showerror("Error de Java",
                             "No se encontró Java 17. Por favor, instálelo manualmente o asegúrese de que esté en la carpeta del launcher.")
        return None

    except Exception as e:
        messagebox.showerror("Error", f"Problema al buscar Java: {e}")
        return None