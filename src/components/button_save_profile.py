import customtkinter as ctk
from helpers.ui_tools import configurer_button

class ButtonSaveProfile(ctk.CTkButton):
    def __init__(self, master, command: callable = None, **kwargs):
        super().__init__(master, text="Save Profile", command=command, **kwargs)
        configurer_button(self)
        self.pack(pady=10)