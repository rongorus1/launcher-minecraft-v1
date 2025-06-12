from tkinter import messagebox

import customtkinter as ctk

from components.button_save import ButtonSave
from controller.minecraft_controller import MinecraftController
from services.settings_service import load_settings, save_settings


class RamConfigurationWindow(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Configuración de RAM para Minecraft")
        self.geometry("400x250")
        self.attributes('-topmost', True)

        ctk.CTkLabel(self, text="Configuración de RAM", font=("Arial", 16)).pack(pady=10)

        settings = load_settings()
        # Variables para almacenar valores de RAM
        ram_var = ctk.StringVar(value=settings['ram']['max'].replace('G', ''))

        ctk.CTkLabel(self, text="RAM para Minecraft (GB):").pack(pady=5)
        ram_entry = ctk.CTkEntry(self, textvariable=ram_var, placeholder_text="Ejemplo: 8")
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
                settings['ram']['min'] = f"{ram_numerica // 2}G"  # La mitad como RAM mínima
                settings['ram']['max'] = f"{ram_numerica}G"
                save_settings(settings)

                # Cerrar ventana y ejecutar Minecraft
                self.destroy()
                if self.master is not None:
                    self.master.close()
                minecraft_controller = MinecraftController(self)
                minecraft_controller.ejecutar_minecraft(self)

            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido de GB")

        button_save = ButtonSave(self, command=guardar_y_ejecutar)
        button_save.pack(pady=10)