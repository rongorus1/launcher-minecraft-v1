import os
import platform
import subprocess
import customtkinter as ctk
import logging
from tkinter import messagebox
import threading

import minecraft_launcher_lib

from components.progress_bar_generic import ProgressBarGeneric
from config import MINECRAFT_VERSION, FORGE_VERSION, MINECRAFT_DIRECTORY
from helpers.java_tools import detectar_java
from helpers.ram_tools import validate_ram
from services.logging_service import config_logging
from services.profile_service import load_profiles
from services.settings_service import load_settings


class MinecraftController:
    def __init__(self, root_window: ctk.CTk = None, progress_bar: ProgressBarGeneric = None):
        config_logging()
        self.logging = logging.getLogger()
        self.progress_bar = progress_bar
        self.root_window = root_window
        self.progress_bar_value_total: int = 0

    def minecraft_set_status(self, text: str):
        self.logging.info(text)


    def minecraft_set_progress(self, value: int):
        self.logging.info(value)
        self.logging.info(value / self.progress_bar_value_total)

        if self.progress_bar:
            if self.progress_bar.is_hidden:
                self.progress_bar.show_element()
            if self.progress_bar_value_total > 0 and value <= self.progress_bar_value_total:
                self.progress_bar.set(value / self.progress_bar_value_total)
            else:
                self.progress_bar.set(0.0)


    def minecraft_set_max(self, value: int):
        self.logging.info(value)
        self.progress_bar_value_total = value


    def ejecutar_minecraft(self, window: ctk.CTkToplevel = None):
        def run_install():
            try:
                settings = load_settings()
                if not validate_ram(settings['ram']['min'], settings['ram']['max']):
                    self.root_window.after(0, lambda: messagebox.showerror("Error", "La RAM debe estar entre 4 y 16 GB"))
                    return

                java_path = detectar_java()
                if not java_path:
                    self.root_window.after(0, lambda: messagebox.showerror("Error", "No se pudo encontrar Java en el PATH"))
                    return

                forge_profile = f"{MINECRAFT_VERSION}-forge-{FORGE_VERSION}"

                data_profile = load_profiles()
                profile_names = [p['username'] for p in data_profile['profiles']]

                options = {
                    "username": profile_names[0] if profile_names else "Guess",
                    "token": "",
                    "uuid": "",
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
                    self.root_window.after(0, lambda: messagebox.showinfo("Info", "Minecraft no está instalado. Instalando Forge..."))

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

                    if self.progress_bar:
                        if not self.progress_bar.is_hidden:
                            self.root_window.after(0, self.progress_bar.hidde_element)

                command = minecraft_launcher_lib.command.get_minecraft_command(
                    forge_profile, MINECRAFT_DIRECTORY, options
                )

                self.logging.info(f"Iniciando Minecraft: {command}")

                if self.root_window is not None:
                    self.root_window.after(0, self.root_window.destroy)

                if platform.system() == "Windows":
                    subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY, creationflags=subprocess.CREATE_NO_WINDOW)
                elif platform.system() == "Linux":
                    subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)
                else:  # macOS
                    subprocess.Popen(command, cwd=MINECRAFT_DIRECTORY)

            except Exception as e:
                self.logging.error(f"Error al iniciar Minecraft: {e}")
                self.root_window.after(0, lambda: messagebox.showerror("Error", f"No se pudo iniciar Minecraft: {e}"))
                if window is not None:
                    self.root_window.after(0, window.destroy)
                if self.root_window is not None:
                    self.root_window.after(0, self.root_window.destroy)

        threading.Thread(target=run_install, daemon=True).start()
