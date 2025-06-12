import customtkinter as ctk
from helpers.ui_tools import configurer_button

class ButtonUpdateMods(ctk.CTkButton):
    def __init__(self, master, command: callable = None, relx = 0.5, rely = 0.9, is_center: bool = False, **kwargs):
        super().__init__(master, text="Actualizar Mods", command=command, **kwargs)
        configurer_button(self)
        self.pack(pady=10)
        if is_center:
            self.place(
                relx=relx,
                rely=rely,
                anchor="center"
            )
        else:
            self.place(
                relx=relx,
                rely=rely,
            )