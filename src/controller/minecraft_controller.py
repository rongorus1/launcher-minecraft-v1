import os
import platform
import subprocess
import customtkinter as ctk
import logging
from tkinter import messagebox

import minecraft_launcher_lib

from config import MINECRAFT_VERSION, FORGE_VERSION, MINECRAFT_DIRECTORY
from helpers.java_tools import detectar_java
from helpers.ram_tools import validate_ram
from services.logging_service import config_logging
from services.profile_service import load_profiles
from services.settings_service import load_settings


class MinecraftController:
    def __init__(self, main_window: ctk.CTkToplevel):
        config_logging()
        self.logging = logging.getLogger()
        self.main_window = main_window

    def minecraft_set_status(self, text: str):
        self.logging.info(text)
        messagebox.showinfo("Estado de la Instalación", f"Estado: {text}")


    def minecraft_set_progress(self, value: int):
        self.logging.info(value)


    def minecraft_set_max(self, value: int):
        self.logging.info(value)


    def ejecutar_minecraft(self, window: ctk.CTkToplevel):
        try:
            settings = load_settings()
            if not validate_ram(settings['ram']['min'], settings['ram']['max']):
                return

            java_path = detectar_java()
            if not java_path:
                return

            forge_profile = f"{MINECRAFT_VERSION}-forge-{FORGE_VERSION}"

            data_profile = load_profiles()
            profile_names = [p['username'] for p in data_profile['profiles']]

            options = {
                "username": profile_names[0] if profile_names else "Guess",  # Reemplazar por el nombre de usuario real
                "token": "",  # Reemplazar por el token real
                "uuid": "",  # Opcional: agrega UUID si es necesario
                "gameDirectory": MINECRAFT_DIRECTORY,
                "java": java_path,
                "jvmArguments": [f"-Xmx{settings['ram']['max']}", f"-Xms{settings['ram']['min']}"],
                "launcherName": "RPLauncher",
                "customResolution": True,
                "resolutionHeight": "480",
                "resolutionWidth": "854",
                "launcherVersion": "1.0",
            }

            if not minecraft_launcher_lib.utils.is_minecraft_installed(MINECRAFT_DIRECTORY):
                self.logging.info("Minecraft no está instalado. Instalando Forge...")

                if not os.path.exists(os.path.join(MINECRAFT_DIRECTORY, "versions", MINECRAFT_VERSION)):
                    self.logging.info("Descargando versión de Minecraft...")
                    minecraft_launcher_lib.install.install_minecraft_version(
                        MINECRAFT_VERSION, MINECRAFT_DIRECTORY,
                        callback={'setStatus': self.minecraft_set_status, 'setProgress': self.minecraft_set_progress,
                                  'setMax': self.minecraft_set_max}
                    )

                if not os.path.exists(os.path.join(MINECRAFT_DIRECTORY, "versions", forge_profile)):
                    self.logging.info("Descargando Forge...")
                    minecraft_launcher_lib.forge.install_forge_version(
                        f"{MINECRAFT_VERSION}-{FORGE_VERSION}", MINECRAFT_DIRECTORY,
                        callback={'setStatus': self.minecraft_set_status, 'setProgress': self.minecraft_set_progress,
                                  'setMax': self.minecraft_set_max}
                    )

            command = minecraft_launcher_lib.command.get_minecraft_command(
                forge_profile, MINECRAFT_DIRECTORY, options
            )

            self.logging.info(f"Iniciando Minecraft: {command}")

            if self.main_window is not None:
                self.main_window.destroy()

            if platform.system() == "Windows":
                subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY, creationflags=subprocess.CREATE_NO_WINDOW)
            elif platform.system() == "Linux":
                subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)
            else:  # macOS
                subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)

        except Exception as e:
            self.logging.error(f"Error al iniciar Minecraft: {e}")
            messagebox.showerror("Error", f"No se pudo iniciar Minecraft: {e}")
            window.destroy()