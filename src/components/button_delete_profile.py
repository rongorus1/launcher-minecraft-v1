import customtkinter as ctk
from helpers.ui_tools import configurer_button

class ButtonDeleteProfile(ctk.CTkButton):
    def __init__(self, master, command: callable = None, **kwargs):
        super().__init__(master, text="Delete Profile", command=command, **kwargs)
        configurer_button(self)
        self.pack(pady=10)