import minecraft_launcher_lib
import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import sys
import json
import platform
import re
from datetime import datetime
import zipfile
import shutil
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='launcher.log'
)

# Manejo de rutas multiplataforma
def obtener_directorio_launcher():
    """Obtener directorio del launcher de manera multiplataforma"""
    try:
        if platform.system() == "Windows":
            base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
        elif platform.system() == "Darwin":  # macOS
            base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
        else:  # Linux y otros sistemas
            base_dir = os.path.join(os.path.expanduser("~"), "RPLauncher")
        
        os.makedirs(base_dir, exist_ok=True)
        return base_dir
    except Exception as e:
        logging.error(f"Error al crear directorio del launcher: {e}")
        messagebox.showerror("Error", "No se pudo crear el directorio del launcher")
        return None

# Variables globales
LAUNCHER_DIR = obtener_directorio_launcher()
MINECRAFT_DIRECTORY = os.path.join(LAUNCHER_DIR, ".minecraft")
os.makedirs(MINECRAFT_DIRECTORY, exist_ok=True)

# Configuraciones de Minecraft
MINECRAFT_VERSION = "1.20.1"
FORGE_VERSION = "47.3.0"

# Rutas de configuración
PROFILES_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_profiles.json")
SETTINGS_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_settings.json")

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
        logging.error(f"Error en instalación de Java: {e}")
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
                r"C:\Program Files\Java\jdk-17\bin\java.exe",     # Ruta de instalación común
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
        logging.error(f"Error al detectar Java: {e}")
        messagebox.showerror("Error", f"Problema al buscar Java: {e}")
        return None


# Cross-platform path handling
def get_launcher_directory():
    """Get a cross-platform launcher directory"""
    if platform.system() == "Windows":
        base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
    elif platform.system() == "Darwin":  # macOS
        base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "RPLauncher")
    else:  # Linux and other systems
        base_dir = os.path.join(os.path.expanduser("~"), "RPLauncher")
    
    # Ensure the directory exists
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

# Global variables
LAUNCHER_DIR = get_launcher_directory()
MINECRAFT_DIRECTORY = os.path.join(LAUNCHER_DIR, ".minecraft")
os.makedirs(MINECRAFT_DIRECTORY, exist_ok=True)

# Paths for resources
def get_resource_path(filename):
    """Get path for resources, supporting bundled and development environments"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

# Minecraft and Forge configuration
MINECRAFT_VERSION = "1.18.2"
FORGE_VERSION = "40.3.0"

# Configuration file paths
PROFILES_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_profiles.json")
SETTINGS_CONFIG_PATH = os.path.join(MINECRAFT_DIRECTORY, "rp_settings.json")

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

def configurar_ram():
    """Diálogo de configuración de RAM con guardado inmediato"""
    settings = load_settings()
    
    # Crear ventana de configuración
    ram_window = ctk.CTkToplevel()
    ram_window.title("Configuración de RAM para Minecraft")
    ram_window.geometry("400x250")
    ram_window.attributes('-topmost', True)
    
    ctk.CTkLabel(ram_window, text="Configuración de RAM", font=("Arial", 16)).pack(pady=10)
    
    # Variables para almacenar valores de RAM
    ram_var = ctk.StringVar(value=settings['ram']['max'].replace('G', ''))
    
    ctk.CTkLabel(ram_window, text="RAM para Minecraft (GB):").pack(pady=5)
    ram_entry = ctk.CTkEntry(ram_window, textvariable=ram_var, placeholder_text="Ejemplo: 8")
    ram_entry.pack(pady=5)
    
    def guardar_y_ejecutar():
        try:
            # Validar entrada
            ram = ram_entry.get().strip()
            ram_numerica = int(ram)
            
            # Validaciones de RAM
            if ram_numerica < 4 or ram_numerica > 16:
                messagebox.showerror("Error", "La RAM debe estar entre 4 y 16 GB")
                return
            
            # Guardar configuración
            settings['ram']['min'] = f"{ram_numerica//2}G"  # La mitad como RAM mínima
            settings['ram']['max'] = f"{ram_numerica}G"
            save_settings(settings)
            
            # Cerrar ventana y ejecutar Minecraft
            ram_window.destroy()
            ejecutar_minecraft()
        
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido de GB")
    
    # Botón para guardar y ejecutar
    boton_guardar = ctk.CTkButton(
        ram_window, 
        text="Guardar y Iniciar Minecraft", 
        command=guardar_y_ejecutar
    )
    boton_guardar.pack(pady=10)

def iniciar_sesion():
    """Login function with profile selection."""
    profiles = load_profiles()
    
    login_window = ctk.CTkToplevel()
    login_window.title("Profile Management")
    login_window.geometry("400x400")
    login_window.attributes('-topmost', True)  # Ensure the window stays on top

    ctk.CTkLabel(login_window, text="Profile Management", font=("Arial", 20)).pack(pady=10)

    # Dropdown menu for existing profiles
    profile_names = [p['username'] for p in profiles['profiles']]
    selected_profile = ctk.StringVar(value=profile_names[0] if profile_names else "New Profile")
    ctk.CTkLabel(login_window, text="Select a Profile:").pack(pady=5)
    profile_dropdown = ctk.CTkOptionMenu(login_window, variable=selected_profile, values=profile_names + ["New Profile"])
    profile_dropdown.pack(pady=5, padx=20)

    # Username Entry
    username_entry = ctk.CTkEntry(login_window, placeholder_text="Enter username (for new profile)")
    username_entry.pack(pady=5, padx=20)

    def save_profile():
        selected = selected_profile.get()
        if selected == "New Profile":
            username = username_entry.get().strip()
            if not username:
                messagebox.showwarning("Warning", "Username cannot be empty")
                return
        else:
            username = selected
        
        # Check if profile already exists
        existing_profile = next((p for p in profiles['profiles'] if p['username'] == username), None)
        
        if existing_profile:
            # Update existing profile
            existing_profile['last_login'] = datetime.now().isoformat()
        else:
            # Create new profile
            new_profile = {
                'username': username,
                'last_login': datetime.now().isoformat()
            }
            profiles['profiles'].append(new_profile)

        # Save profiles
        save_profiles(profiles)
        
        # Update settings with last profile
        settings = load_settings()
        settings['last_profile'] = username
        save_settings(settings)
        
        messagebox.showinfo("Success", f"Profile saved for {username}")
        login_window.destroy()

    def delete_profile():
        selected = selected_profile.get()
        if selected == "New Profile":
            messagebox.showwarning("Warning", "Cannot delete 'New Profile'.")
            return
        
        # Remove selected profile
        profiles['profiles'] = [p for p in profiles['profiles'] if p['username'] != selected]
        save_profiles(profiles)

        # Update settings if the deleted profile was the last used
        settings = load_settings()
        if settings.get('last_profile') == selected:
            settings['last_profile'] = None
        save_settings(settings)

        messagebox.showinfo("Success", f"Profile '{selected}' deleted.")
        login_window.destroy()
        iniciar_sesion()  # Reopen the login window to refresh the list

    # Configure button styles
    def configurar_boton(boton):
        boton.configure(
            fg_color="black",
            text_color="white",
            font=("Arial", 12, "bold"),
            border_width=2,
            border_color="white"
        )

    save_button = ctk.CTkButton(login_window, text="Save Profile", command=save_profile)
    configurar_boton(save_button)
    save_button.pack(pady=10)

    delete_button = ctk.CTkButton(login_window, text="Delete Profile", command=delete_profile)
    configurar_boton(delete_button)
    delete_button.pack(pady=10)

    # Profile List
    ctk.CTkLabel(login_window, text="Existing Profiles:").pack(pady=5)
    profile_listbox = ctk.CTkTextbox(login_window, height=100, width=300)
    profile_listbox.pack(pady=5)
    
    # Populate profile list
    profile_text = "\n".join([f"{p['username']} (Last Login: {p.get('last_login', 'Never')})" for p in profiles.get('profiles', [])])
    profile_listbox.insert("0.0", profile_text or "No profiles saved")
    profile_listbox.configure(state="disabled")



def obtener_auth_data():
    """Generar datos de autenticación para Minecraft"""
    # Aquí deberías implementar la autenticación real.
    # Ejemplo de autenticación con datos ficticios (debes reemplazar esto):
    auth_data = {
        "username": "UsuarioEjemplo",  # Reemplazar por el nombre de usuario real
        "access_token": "TokenDeAccesoEjemplo",  # Reemplazar por el token real
        "uuid": "UUIDEjemplo"  # Opcional: agrega UUID si es necesario
    }
    return auth_data

def minecraft_set_status(text: str):
    logging.info(text)

def minecraft_set_progress(value: int):
    logging.info(value)

def minecraft_set_max(value: int):
    logging.info(value)

def ejecutar_minecraft():
    try:
        settings = load_settings()
        if not validate_ram(settings['ram']['min'], settings['ram']['max']):
            return

        java_path = detectar_java()
        if not java_path:
            return

        forge_profile = f"{MINECRAFT_VERSION}-forge-{FORGE_VERSION}"

        auth_data = obtener_auth_data()
        if not auth_data or not auth_data.get("username") or not auth_data.get("access_token"):
            messagebox.showerror("Error", "No se encontraron datos de autenticación")
            return

        data_profile = load_profiles()
        profile_names = [p['username'] for p in data_profile['profiles']]

        options = {
            "username": profile_names[0] if profile_names else "Guess",  # Reemplazar por el nombre de usuario real
            "token": "",  # Reemplazar por el token real
            "uuid": "",  # Opcional: agrega UUID si es necesario
            "gameDirectory": MINECRAFT_DIRECTORY,
            "java": java_path,
            "jvmArguments": [f"-Xmx{settings['ram']['max']}", f"-Xms{settings['ram']['min']}"] ,
            "launcherName": "RPLauncher",
            "customResolution": True,
            "resolutionHeight": "480",
            "resolutionWidth": "854",
            "launcherVersion": "1.0",
        }

        if not minecraft_launcher_lib.utils.is_minecraft_installed(MINECRAFT_DIRECTORY):
            logging.info("Minecraft no está instalado. Instalando Forge...")
            
            if not os.path.exists(os.path.join(MINECRAFT_DIRECTORY, "versions", MINECRAFT_VERSION)):
                logging.info("Descargando versión de Minecraft...")
                minecraft_launcher_lib.install.install_minecraft_version(
                    MINECRAFT_VERSION, MINECRAFT_DIRECTORY, callback={'setStatus': minecraft_set_status, 'setProgress': minecraft_set_progress, 'setMax': minecraft_set_max}
                    )

            if not os.path.exists(os.path.join(MINECRAFT_DIRECTORY, "versions", forge_profile)):
                logging.info("Descargando Forge...")
                minecraft_launcher_lib.forge.install_forge_version(
                    f"{MINECRAFT_VERSION}-{FORGE_VERSION}" , MINECRAFT_DIRECTORY, callback={'setStatus': minecraft_set_status, 'setProgress': minecraft_set_progress, 'setMax': minecraft_set_max}
                )

        command = minecraft_launcher_lib.command.get_minecraft_command(
            forge_profile, MINECRAFT_DIRECTORY, options
        )

        logging.info(f"Iniciando Minecraft: {command}")

        global app
        if app is not None:
            app.destroy()
        if platform.system() == "Windows":
            subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY, creationflags=subprocess.CREATE_NO_WINDOW)
        elif platform.system() == "Linux":
            subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)
        else:  # macOS
            subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)
    
    except Exception as e:
        logging.error(f"Error al iniciar Minecraft: {e}")
        messagebox.showerror("Error", f"No se pudo iniciar Minecraft: {e}")


def abrir_ventana_principal():
    global app
    app = ctk.CTk()
    app.title("RPLauncher")
    app.geometry("1200x700")

    # Imagen de fondo original
    background_image_path = os.path.join(LAUNCHER_DIR, "fondo.png")
    if os.path.exists(background_image_path):
        bg_image = ctk.CTkImage(
            light_image=Image.open(background_image_path),
            dark_image=Image.open(background_image_path),
            size=(1200, 700)
        )
        bg_label = ctk.CTkLabel(app, image=bg_image, text="")
        bg_label.place(relx=0.5, rely=0.5, anchor="center")

    # Configuraciones y botones originales se mantienen igual
    def configurar_boton(boton):
        boton.configure(
            fg_color="black",
            text_color="white",
            font=("Arial", 12, "bold"),
            border_width=1,
            border_color="white"
        )

    play_button = ctk.CTkButton(app, text="Play", command=configurar_ram)
    configurar_boton(play_button)
    play_button.place(relx=0.5, rely=0.9, anchor="center")

    login_button = ctk.CTkButton(app, text="Iniciar Sesión", command=iniciar_sesion)
    configurar_boton(login_button)
    login_button.place(relx=0.05, rely=0.05)

    ram_settings_button = ctk.CTkButton(app, text="Configuración RAM", command=configurar_ram)
    configurar_boton(ram_settings_button)
    ram_settings_button.place(relx=0.05, rely=0.15)

    app.mainloop()

# Entry point
if __name__ == "__main__":
    abrir_ventana_principal()
