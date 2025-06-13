import customtkinter as ctk
import os
from PIL import Image, ImageTk

from components.button_login import ButtonLogin
from components.button_play import ButtonPlay
from components.button_ram_setting import ButtonRamSetting
from components.button_update_mods import ButtonUpdateMods
from components.progress_bar_generic import ProgressBarGeneric
from controller.ram_window_controller import open_window_configurar_ram
from controller.start_session_controller import run_session_controller
from controller.update_mods_controller import run_update_mods_controller


class MainWindow(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.progressbar: ProgressBarGeneric = None
        self.update_mods_button = None
        self.login_button = None
        self.ram_settings_button = None
        self.play_button = None

        self.title("Rongocraft Launcher")
        self.geometry("1200x700")

        # Load and set background image
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
        if os.path.exists(assets_path):
            bg_image_path = os.path.join(assets_path, 'background.png')
            if os.path.exists(bg_image_path):
                self.bg_image = ctk.CTkImage(
                    light_image=Image.open(bg_image_path),
                    dark_image=Image.open(bg_image_path),
                    size=(1200, 700)
                )
                self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.bind("<Configure>", self.resize_bg)

        # Load components
        self.load_components()

    # Add components
    def load_components(self):

        self.progressbar = ProgressBarGeneric(self)

        self.play_button = ButtonPlay(
            self,
            command=lambda: open_window_configurar_ram(master=self, progressbar = self.progressbar),
            is_center=True
        )
        self.login_button = ButtonLogin(
            self,
            command=lambda: run_session_controller(master=self),
            relx=0.05,
            rely=0.05
        )
        self.ram_settings_button = ButtonRamSetting(
            self,
            command=lambda: open_window_configurar_ram(master=self, progressbar = self.progressbar),
            relx=0.05,
            rely=0.15
        )

        self.update_mods_button = ButtonUpdateMods(
            self,
            command = lambda: run_update_mods_controller(self.progressbar),
            relx=0.05,
            rely=0.25
        )

    def resize_bg(self, event):
        if self.bg_image is not None:
            self.bg_image._size = (event.width, event.height)
            self.bg_label.configure(image=self.bg_image)

        if self.progressbar is not None:
            self.progressbar.update_width(event.width)


    def run(self):
        self.mainloop()

    def close(self):
        self.destroy()